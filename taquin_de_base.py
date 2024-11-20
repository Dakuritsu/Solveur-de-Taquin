import random
import time
from collections import deque
import heapq

# Générer un plateau de taille k x k mélangé
def generer_etat_initial(k):
    etat = list(range(0, k * k))
    random.shuffle(etat)
    return [etat[i:i + k] for i in range(0, len(etat), k)] # on retourne un tableau de k lignes et de k éléments

def est_etat_final(etat):
    k = len(etat)
    n = k * k

    etat_final = []
    for i in range(k): 
        ligne = []
        for j in range(k): 
            val = (i * k + j + 1) % n
            ligne.append(val)
        etat_final.append(ligne)

    return etat == etat_final

def trouver_case_vide(etat):
    for ix, row in enumerate(etat):
        for iy, val in enumerate(row):
            if val == 0:
                return ix, iy
    return None

def generer_etats_suivants(etat):
    k = len(etat)
    etats_suivants = []
    x, y = trouver_case_vide(etat)
    
    mouvements = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
    
    for dx, dy in mouvements:
        newX, newY = x + dx, y + dy
        
        if 0 <= newX < k and 0 <= newY < k:
            nouvel_etat = []
            for row in etat:
                nouvel_etat.append(row[:])
            
            case_temp = nouvel_etat[newX][newY]
            nouvel_etat[newX][newY] = nouvel_etat[x][y]
            nouvel_etat[x][y] = case_temp
            
            etats_suivants.append(nouvel_etat)
    
    return etats_suivants


def afficher_etat(etat):
    for line in etat:
        newLine = " ".join(f"{valeur:2}" for valeur in line)
        print(newLine)
    print()


def dfs(etat_initial):
    stack = [(etat_initial, [])]
    visites = set()
    
    while stack:
        etat, chemin = stack.pop()
        
        if est_etat_final(etat):
            return chemin
        
        etat_tuple = tuple(map(tuple, etat))
        if etat_tuple in visites:
            continue
        
        visites.add(etat_tuple)
        for suivant in generer_etats_suivants(etat):
            stack.append((suivant, chemin + [suivant]))
    
    return None


def bfs(etat_initial):
    queue = deque([(etat_initial, [])])
    visites = set()
    
    while queue:
        etat, chemin = queue.popleft()
        
        if est_etat_final(etat):
            return chemin
        
        etat_tuple = tuple(map(tuple, etat))
        if etat_tuple in visites:
            continue
        
        visites.add(etat_tuple)
        for suivant in generer_etats_suivants(etat):
            queue.append((suivant, chemin + [suivant]))
    
    return None

def heuristique(etat):
    k = len(etat)
    distance = 0
    for i in range(k):
        for j in range(k):
            valeur = etat[i][j]
            if valeur != 0:
                cible_x, cible_y = divmod(valeur - 1, k)
                distance += abs(i - cible_x) + abs(j - cible_y)
    return distance

def a_star(etat_initial):
    queue = [(heuristique(etat_initial), 0, etat_initial, [])]
    visites = set()
    
    while queue:
        _, cout, etat, chemin = heapq.heappop(queue)
        
        if est_etat_final(etat):
            return chemin
        
        etat_tuple = tuple(map(tuple, etat))
        if etat_tuple in visites:
            continue
        
        visites.add(etat_tuple)
        for suivant in generer_etats_suivants(etat):
            heapq.heappush(queue, (cout + 1 + heuristique(suivant), cout + 1, suivant, chemin + [suivant]))
    
    return None

# Nouvelles fonctions pour afficher le parcours complet
def dfs_avec_parcours(etat_initial):
    stack = [(etat_initial, [])]
    visites = set()
    parcours = []
    
    while stack:
        etat, chemin = stack.pop()
        parcours.append(etat)  # Ajoute l'état actuel au parcours
        
        if est_etat_final(etat):
            return chemin, parcours
        
        etat_tuple = tuple(map(tuple, etat))
        if etat_tuple in visites:
            continue
        
        visites.add(etat_tuple)
        for suivant in generer_etats_suivants(etat):
            stack.append((suivant, chemin + [suivant]))
    
    return None, parcours

def bfs_avec_parcours(etat_initial):
    queue = deque([(etat_initial, [])])
    visites = set()
    parcours = []
    
    while queue:
        etat, chemin = queue.popleft()
        parcours.append(etat)  # Ajoute l'état actuel au parcours
        
        if est_etat_final(etat):
            return chemin, parcours
        
        etat_tuple = tuple(map(tuple, etat))
        if etat_tuple in visites:
            continue
        
        visites.add(etat_tuple)
        for suivant in generer_etats_suivants(etat):
            queue.append((suivant, chemin + [suivant]))
    
    return None, parcours

def a_star_avec_parcours(etat_initial):
    queue = [(heuristique(etat_initial), 0, etat_initial, [])]
    visites = set()
    parcours = []
    
    while queue:
        _, cout, etat, chemin = heapq.heappop(queue)
        parcours.append(etat)  # Ajoute l'état actuel au parcours
        
        if est_etat_final(etat):
            return chemin, parcours
        
        etat_tuple = tuple(map(tuple, etat))
        if etat_tuple in visites:
            continue
        
        visites.add(etat_tuple)
        for suivant in generer_etats_suivants(etat):
            heapq.heappush(queue, (cout + 1 + heuristique(suivant), cout + 1, suivant, chemin + [suivant]))
    
    return None, parcours

def main():
    print("Bienvenue dans le solveur de Taquin!")
    k = int(input("Entrez la taille du puzzle (k): "))
    strategie = input("Choisissez la stratégie (dfs, bfs, a*): ").lower()
    avec_parcours = input("Souhaitez-vous afficher tout le parcours ? (oui/non): ").lower()
    
    # Générer un état initial
    etat_initial = generer_etat_initial(k)
    print("État initial :")
    afficher_etat(etat_initial)
    
    # Choisir l'algorithme avec ou sans parcours
    if strategie == "dfs":
        algorithme = dfs_avec_parcours if avec_parcours == "oui" else dfs
    elif strategie == "bfs":
        algorithme = bfs_avec_parcours if avec_parcours == "oui" else bfs
    elif strategie == "a*":
        algorithme = a_star_avec_parcours if avec_parcours == "oui" else a_star
    else:
        print("Stratégie non reconnue.")
        return
    
    # Lancer la résolution et mesurer le temps
    start_time = time.time()
    if avec_parcours == "oui":
        solution, parcours = algorithme(etat_initial)
    else:
        solution = algorithme(etat_initial)
    end_time = time.time()
    
    # Affichage des résultats
    if solution:
        print(f"Solution trouvée en {len(solution)} étapes et en {end_time - start_time:.2f} secondes!")
        print("\nÉtapes de la solution :")
        for i, etat in enumerate(solution, 1):
            print(f"Étape {i}:")
            afficher_etat(etat)
        
        # Si l'utilisateur veut afficher le parcours complet
        if avec_parcours == "oui":
            print("\nParcours complet :")
            for i, etat in enumerate(parcours, 1):
                print(f"État {i}:")
                afficher_etat(etat)
    else:
        print("Aucune solution trouvée.")

if __name__ == "__main__":
    main()
