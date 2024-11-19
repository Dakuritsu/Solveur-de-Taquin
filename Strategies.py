from collections import deque
from heapq import heappop, heappush
from typing import List, Tuple, Set

class Strategies:
    def __init__(self, taquin):
        self.taquin = taquin

    def bfs(self, avec_parcours=False) -> Tuple[List[List[int]], List[List[List[int]]]]:
        """Résout le taquin avec l'algorithme BFS."""
        queue = deque([(self.taquin.etat_initial, [])])
        visites = set()
        parcours = []

        while queue:
            etat, chemin = queue.popleft()
            if avec_parcours:
                parcours.append(etat)

            if self.taquin.est_final(etat):
                return chemin, parcours

            etat_tuple = tuple(map(tuple, etat))
            if etat_tuple in visites:
                continue

            visites.add(etat_tuple)
            for suivant in self.taquin.generer_suivants(etat):
                queue.append((suivant, chemin + [suivant]))

        return None, parcours

    def dfs(self, avec_parcours=False) -> Tuple[List[List[int]], List[List[List[int]]]]:
        """Résout le taquin avec l'algorithme DFS."""
        stack = [(self.taquin.etat_initial, [])]
        visites = set()
        parcours = []

        while stack:
            etat, chemin = stack.pop()
            if avec_parcours:
                parcours.append(etat)

            if self.taquin.est_final(etat):
                return chemin, parcours

            etat_tuple = tuple(map(tuple, etat))
            if etat_tuple in visites:
                continue

            visites.add(etat_tuple)
            for suivant in self.taquin.generer_suivants(etat):
                stack.append((suivant, chemin + [suivant]))

        return None, parcours
    
    def heuristique(self, etat: List[List[int]]) -> int:
        """Calcule la distance de Manhattan pour une heuristique A*."""
        taille = len(etat)
        distance = 0
        for i in range(taille):
            for j in range(taille):
                valeur = etat[i][j]
                if valeur != 0:
                    cible_x, cible_y = divmod(valeur - 1, taille)
                    distance += abs(i - cible_x) + abs(j - cible_y)
        return distance

    def a_etoile(self, avec_parcours=False) -> Tuple[List[List[int]], List[List[List[int]]]]:
        """Résout le taquin avec l'algorithme A*."""
        queue = [(self.heuristique(self.taquin.etat_initial), 0, self.taquin.etat_initial, [])]
        visites = set()
        parcours = []

        while queue:
            _, cout, etat, chemin = heappop(queue)
            if avec_parcours:
                parcours.append(etat)

            if self.taquin.est_final(etat):
                return chemin, parcours

            etat_tuple = tuple(map(tuple, etat))
            if etat_tuple in visites:
                continue

            visites.add(etat_tuple)
            for suivant in self.taquin.generer_suivants(etat):
                heappush(queue, (cout + 1 + self.heuristique(suivant), cout + 1, suivant, chemin + [suivant]))

        return None, parcours
