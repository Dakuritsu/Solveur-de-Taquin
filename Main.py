from Taquin import Taquin
from Strategies import Strategies
from InterfaceTaquin import InterfaceTaquin
import tkinter as tk

def mode_console():
    """Mode console."""
    taille = int(input("Entrez la taille du taquin : "))
    taquin = Taquin(taille)
    strategies = Strategies(taquin)

    print("État initial :")
    for ligne in taquin.etat_initial:
        print(ligne)

    choix_strategie = input("Choisissez une stratégie (dfs, bfs, a*) : ").strip().lower()
    voir_parcours = input("Voulez-vous voir tout le parcours ? (oui/non) : ").strip().lower() == "oui"

    if choix_strategie == "dfs":
        solution, parcours = strategies.dfs(avec_parcours=voir_parcours)
    elif choix_strategie == "bfs":
        solution, parcours = strategies.bfs(avec_parcours=voir_parcours)
    elif choix_strategie == "a*":
        solution, parcours = strategies.a_etoile(avec_parcours=voir_parcours)
    else:
        print("Stratégie inconnue.")
        return

    if voir_parcours:
        print("Parcours complet :")
        for i, etape in enumerate(parcours):
            print(f"Étape {i + 1} :")
            for ligne in etape:
                print(ligne)
            print("---")

    # Afficher la solution même si le parcours est affiché
    print("Solution :")
    for i, etape in enumerate(solution):
        print(f"Étape {i + 1} :")
        for ligne in etape:
            print(ligne)
        print("---")


if __name__ == "__main__":
    choix = input("Voulez-vous utiliser l'interface graphique ? (oui/non) : ").strip().lower()
    if choix == "oui":
        root = tk.Tk()
        app = InterfaceTaquin(root)
        root.mainloop()
    else:
        mode_console()
