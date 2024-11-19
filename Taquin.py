import random
from typing import List, Tuple

# Régler le probleme où lorsque l'on mélange on a déjà l'état final 

class Taquin:
    def __init__(self, taille: int):
        self.taille = taille
        self.etat_initial = self.generer_etat_initial()
        self.etat_final = self.generer_etat_final()

    def compter_inversions(self, etat: List[int]) -> int:
        """Compte le nombre d'inversions dans un état."""
        inversions = 0
        n = len(etat)
        for i in range(n):
            for j in range(i + 1, n):
                if etat[i] > etat[j] and etat[i] != 0 and etat[j] != 0:
                    inversions += 1
        return inversions

    def est_resolvable(self, etat: List[List[int]]) -> bool:
        """Vérifie si un état 2D donné est résolvable."""

        tab_etat = []
        for row in etat:
            for val in row:
                tab_etat.append(val)

        inversions = self.compter_inversions(tab_etat)

        case_vide_ligne = None
        for i, row in enumerate(etat):
            if 0 in row:
                case_vide_ligne = i
                break


        if self.taille % 2 == 1:  # Taille impaire
            return inversions % 2 == 0
        else:  # Taille paire
            return (case_vide_ligne % 2 == 0 and inversions % 2 == 1) or \
                   (case_vide_ligne % 2 == 1 and inversions % 2 == 0)

    def generer_etat_initial(self) -> List[List[int]]:
        """Génère un plateau mélangé de taille k x k avec une solution."""
        while True:
            etat = list(range(self.taille * self.taille))
            random.shuffle(etat)
            
            etats = []

            for i in range(0, len(etat), self.taille):
                ligne = etat[i:i + self.taille]
                etats.append(ligne)

            if self.est_resolvable(etats):
                return etats

    def generer_etat_final(self) -> List[List[int]]:
        """Renvoie l'état final attendu."""
        n = self.taille * self.taille
        etat_final = []

        for i in range(self.taille):
            ligne = []
            for j in range(self.taille):
                valeur = (i * self.taille + j + 1) % n
                ligne.append(valeur)
            etat_final.append(ligne)

        return etat_final

    def est_final(self, etat: List[List[int]]) -> bool:
        """Vérifie si l'état donné est l'état final."""
        return etat == self.etat_final

    def trouver_case_vide(self, etat: List[List[int]]) -> Tuple[int, int]:
        """Trouve la position de la case vide dans un état donné."""
        for x, row in enumerate(etat):
            for y, val in enumerate(row):
                if val == 0:
                    return x, y
        return -1, -1

    def generer_suivants(self, etat: List[List[int]]) -> List[List[List[int]]]:
        """Génère tous les états voisins possibles en déplaçant la case vide."""
        x, y = self.trouver_case_vide(etat)
        mouvements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        etats_suivants = []

        for dx, dy in mouvements:
            new_x, new_y = x + dx, y + dy
            
            if 0 <= new_x < self.taille and 0 <= new_y < self.taille:
                nouvel_etat = [row.copy() for row in etat]
                
                case_temp = nouvel_etat[new_x][new_y]
                nouvel_etat[new_x][new_y] = nouvel_etat[x][y]
                nouvel_etat[x][y] = case_temp
                
                etats_suivants.append(nouvel_etat)

        return etats_suivants
