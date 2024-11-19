import tkinter as tk
import colorsys
from tkinter import messagebox
from Taquin import Taquin
from Strategies import Strategies

class InterfaceTaquin:
    def __init__(self, root):
        self.root = root
        self.root.title("Solveur de Taquin")
        self.taquin = None
        self.strategie = None
        self.parcours = []
        self.solution = []
        self.taille = 3
        self.choix_strategie = tk.StringVar(value="bfs")
        self.mode_parcours = tk.BooleanVar(value=False)
        self.index_parcours = 0
        self.navigation_frame = None

        self.root.configure(bg="#f5f5f5")

        # Création de  l'interface
        self.creer_grille()
        self.creer_controles()

    def creer_grille(self):
        """Créer la grille des boutons."""
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(pady=20)
        self.grille_frame = frame
        self.rafraichir_grille()

    def creer_controles(self):
        """Créer les contrôles pour les actions."""
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(pady=10)

        # Taille du Taquin
        taille_label = tk.Label(frame, text="Taille du Taquin (min 2x2) :", font=("Helvetica", 12), bg="#f5f5f5")
        taille_label.pack(side=tk.LEFT, padx=10)

        self.taille_entry = tk.Entry(frame, font=("Helvetica", 12), width=5, justify='center')
        self.taille_entry.insert(tk.END, str(self.taille))  # Insérer la taille actuelle
        self.taille_entry.pack(side=tk.LEFT, padx=10)

        # Appliquer la taille saisie
        tk.Button(frame, text="Appliquer", command=self.appliquer_taille, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)

        # Stratégie
        tk.Label(frame, text="Stratégie :", font=("Helvetica", 12), bg="#f5f5f5").pack(side=tk.LEFT, padx=10)
        tk.OptionMenu(frame, self.choix_strategie, "dfs", "bfs", "a*").pack(side=tk.LEFT, padx=10)

        # Mode parcours
        tk.Checkbutton(frame, text="Voir tout le parcours", variable=self.mode_parcours, bg="#f5f5f5", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        # Mélanger et Résoudre
        tk.Button(frame, text="Mélanger", command=self.melanger, bg="#2196F3", fg="white", font=("Helvetica", 12), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Résoudre", command=self.resoudre, bg="#FF5722", fg="white", font=("Helvetica", 12), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)

    def appliquer_taille(self):
        """Appliquer la taille du taquin saisie par l'utilisateur."""
        try:
            taille = int(self.taille_entry.get())
            if taille < 2:
                raise ValueError("La taille doit être supérieure ou égale à 2.")
            self.changer_taille(taille)
        except ValueError as e:
            messagebox.showerror("Erreur", f"Erreur de taille : {e}")

    def changer_taille(self, taille):
        """Changer la taille du taquin."""
        self.taille = taille
        self.taquin = None
        self.parcours = []
        self.solution = []
        self.index_parcours = 0
        self.rafraichir_grille()

        # Si un cadre existe, on le supprime
        if self.navigation_frame:
            self.navigation_frame.destroy()
            self.navigation_frame = None

    def rafraichir_grille(self):
        """Mettre à jour la grille des boutons."""
        for widget in self.grille_frame.winfo_children():
            widget.destroy()

        self.boutons = []
        for i in range(self.taille):
            ligne_boutons = []
            for j in range(self.taille):
                btn = tk.Button(self.grille_frame, text="", font=("Helvetica", 16), width=4, height=2, relief="raised", bg="#eeeeee", activebackground="#4CAF50")
                btn.grid(row=i, column=j, padx=2, pady=2)
                ligne_boutons.append(btn)
            self.boutons.append(ligne_boutons)

        self.melanger()

    def melanger(self):
        """Mélanger le taquin."""
        self.taquin = Taquin(self.taille)
        self.maj_grille(self.taquin.etat_initial)

    def generer_palette(self,nombre_valeurs):
        """Génère une liste de couleurs hexadécimales."""
        palette = []
        for i in range(nombre_valeurs):
            hue = i / nombre_valeurs
            lightness = 0.8
            saturation = 0.7
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            couleur_hexa = "#{:02X}{:02X}{:02X}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            palette.append(couleur_hexa)
        return palette

    def obtenir_couleur(self,valeur, palette):
        """Retourne la couleur associée à une valeur."""
        if valeur == 0:
            return "#FFFFFF"
        return palette[valeur - 1]

    def maj_grille(self, etat):
        max_valeur = self.taille * self.taille - 1
        palette = self.generer_palette(max_valeur)

        for i in range(self.taille):
            for j in range(self.taille):
                valeur = etat[i][j]
                texte = "" if valeur == 0 else str(valeur)
                couleur = self.obtenir_couleur(valeur, palette)
                self.boutons[i][j].config(
                    text=texte,
                    state="normal" if valeur != 0 else "disabled",
                    bg=couleur
                )

    def resoudre(self):
        """Résoudre le taquin."""
        if not self.taquin:
            messagebox.showerror("Erreur", "Veuillez mélanger le taquin d'abord.")
            return

        self.strategie = Strategies(self.taquin)
        algo = self.choix_strategie.get()
        avec_parcours = self.mode_parcours.get()

        if algo == "dfs":
            solution, parcours = self.strategie.dfs(avec_parcours=True)
        elif algo == "bfs":
            solution, parcours = self.strategie.bfs(avec_parcours=True)
        elif algo == "a*":
            solution, parcours = self.strategie.a_etoile(avec_parcours=True)
        else:
            messagebox.showerror("Erreur", "Stratégie inconnue.")
            return

        if avec_parcours:
            self.parcours = parcours
            self.index_parcours = 0
            self.maj_grille(self.parcours[self.index_parcours])
        else:
            self.solution = solution
            self.index_parcours = 0
            self.maj_grille(self.solution[self.index_parcours])

        # Si un cadre existe, on le supprime
        if self.navigation_frame:
            self.navigation_frame.destroy()

        # Créer le nouveau cadre
        self.creer_navigation_parcours()

    def creer_navigation_parcours(self):
        """Créer les boutons pour naviguer dans le parcours ou la solution."""
        self.navigation_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.navigation_frame.pack(pady=10)

        self.label_etape = tk.Label(self.navigation_frame, text=f"Étape : {self.index_parcours + 1}/{len(self.parcours) if self.mode_parcours.get() else len(self.solution)}", font=("Helvetica", 14), bg="#f5f5f5", fg="#333333")
        self.label_etape.pack(side=tk.LEFT, padx=10)

        self.label_etat_final = tk.Label(self.navigation_frame, text="", font=("Helvetica", 14), bg="#f5f5f5", fg="green")  # Label pour "État final"
        self.label_etat_final.pack(side=tk.LEFT, padx=10)

        tk.Button(self.navigation_frame, text="<<", command=self.precedent, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)
        tk.Button(self.navigation_frame, text=">>", command=self.suivant, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)

    def precedent(self):
        """Afficher l'état précédent."""
        if self.index_parcours > 0:
            self.index_parcours -= 1
            etat = self.parcours[self.index_parcours] if self.mode_parcours.get() else self.solution[self.index_parcours]
            self.maj_grille(etat)
            self.maj_etape()

    def suivant(self):
        """Afficher l'état suivant."""
        if self.index_parcours < (len(self.parcours) - 1 if self.mode_parcours.get() else len(self.solution) - 1):
            self.index_parcours += 1
            etat = self.parcours[self.index_parcours] if self.mode_parcours.get() else self.solution[self.index_parcours]
            self.maj_grille(etat)
            self.maj_etape()

    def maj_etape(self):
        """Mettre à jour l'affichage de l'étape actuelle."""
        total = len(self.parcours) if self.mode_parcours.get() else len(self.solution)

        self.label_etape.config(text=f"Étape : {self.index_parcours + 1}/{total}")
        
        # Vérification de l'état final
        if self.index_parcours == total - 1:
            self.label_etat_final.config(text="État final atteint !")
        else:
            self.label_etat_final.config(text="")

