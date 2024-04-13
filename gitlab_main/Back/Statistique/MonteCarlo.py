# Importation des bibliothèques et modules nécessaires
from Back.Map import *  # Il est préférable de spécifier exactement ce qui est nécessaire au lieu d'utiliser *
from Back.Candidat import *  # Idem que ci-dessus
import time
from PySide6.QtWidgets import QApplication  # Assurez-vous que QApplication est réellement utilisée
from Front.Widgets.MapQT import *  # Préférer des importations explicites
import multiprocessing
import sys

def generate_unique_colors(int1, int2):
    """
    Génère une couleur unique basée sur deux entiers en calculant les composantes RGB.
    
    :param int1: Premier entier pour le calcul de RGB.
    :param int2: Second entier pour le calcul de RGB.
    :return: QColor représentant la couleur unique générée.
    """
    r = int(int1) % 256
    g = int(int2) % 256
    b = int(int1 * int2) % 256
    return QColor(r, g, b)
    
def creer_sous_maps(map_carrer, k):
    """
    Crée des sous-cartes d'une carte principale en la divisant selon un pas donné.
    
    :param map_carrer: La carte principale à diviser.
    :param k: Le pas de division de la carte.
    :return: Liste des sous-cartes générées.
    """
    sous_maps = []
    taille_map = len(map_carrer)
    
    for i in range(0, taille_map, k):
        for j in range(0, taille_map, k):
            sous_map = []
            for x in range(i, min(i + k, taille_map)):
                sous_map.append(map_carrer[x][j:min(j + k, taille_map)])
            sous_maps.append(sous_map)
    
    return sous_maps

def election_multiple(map_carrer, start, end, k, type_votes):
    """
    Effectue plusieurs élections sur des sous-ensembles de la carte principale.
    
    :param map_carrer: La carte principale.
    :param start: Index de départ pour les élections.
    :param end: Index de fin pour les élections.
    :param k: Le pas pour la génération des sous-cartes.
    :param type_votes: Le type de vote utilisé pour les élections.
    :return: Liste des résultats des élections.
    """
    l = []
    for i in range(start, end, k):
        map_carrer.liste_electeur[len(map_carrer.liste_electeur)-1] = Candidat.genere_candidat(i % (map_carrer.generationX), i // (map_carrer.generationY))
        l.append(map_carrer.Copeland_MC())
    return l

def worker(map_carrer, start, end, k, type_votes, output):
    """
    Fonction travailleur pour le processus parallèle.
    
    :param map_carrer: La carte principale.
    :param start: Index de départ pour le traitement.
    :param end: Index de fin pour le traitement.
    :param k: Le pas pour la génération des sous-cartes.
    :param type_votes: Le type de vote.
    :param output: Liste partagée pour stocker les résultats.
    """
    output.append(election_multiple(map_carrer, start, end, k, type_votes))

def Monte_Carlo(map_carrer, k, type_votes):
    """
    Méthode Monte Carlo pour simuler des élections sur la carte principale.
    
    :param map_carrer: La carte principale sur laquelle exécuter la simulation.
    :param k: Le pas pour la génération des sous-cartes.
    :param type_votes: Le type de vote utilisé pour les élections.
    :return: Liste des résultats de simulation.
    """
    map_carrer.creer_L_population()
    res = []
    jobs = []
    output = multiprocessing.Manager().list()
    print("Début : des tours")
    start_time = time.time()
    
    # Création et démarrage des processus en parallèle
    for i in range(map_carrer.generationX):
        process = multiprocessing.Process(target=worker, args=(map_carrer, i * map_carrer.generationX, (i + 1) * map_carrer.generationY, k, type_votes, output))
        jobs.append(process)
        process.start()
    
    # Attente de la fin des processus
    for process in jobs:
        process.join()
    
    # Compilation des résultats
    for result in output:
        res += result
        
    print("Fin des tours", time.time() - start_time)
    return res

def moyenne_couples(l):
    """
    Calcule la moyenne des positions x et y d'une liste de couples de coordonnées.
    
    :param l: Liste des couples de coordonnées (objets ayant x et y).
    :return: Tuple représentant la moyenne des positions x et y.
    """
    X, Y, t = 0, 0, len(l)
    for ind in l:
        X += ind.x()
        Y += ind.y()
    return (X / t, Y / t)

def CreationSimulation(map, nom, k,type_votes):
    """
    Crée et exécute une simulation basée sur la méthode Monte Carlo.
    
    :param map: La carte principale pour la simulation.
    :param nom: Nom de la simulation.
    :param k: Le pas utilisé pour la simulation.
    :return: Objet HitMap résultant de la simulation.
    """
    mc = Monte_Carlo(map, k,type_votes)
    x, y = moyenne_couples(mc)
    
    # Ajout d'un candidat test basé sur la moyenne des positions
    map.liste_electeur.append(Candidat("test", "test", 100, 100, x, y))
    
    # Exécution et affichage des résultats de la méthode Copeland
    for i in range(1, 5):
        gg = map.Copeland()
        print(f"test {i}", gg.nom())
    
    # Création et placement sur la HitMap
    hitmap = HitMap(map.generationX)
    hitmap.placeALL(map, mc, (x, y))
    return hitmap

def SimulationAleatoire(ModeVotes, t, k,type_votes):
    """
    Lance une simulation aléatoire.
    
    :param ModeVotes: Type de votes pour la simulation.
    :param t: Taille de la carte.
    :param k: Le pas pour la simulation.
    :return: Résultat de la simulation.
    """
    map = Map(None, "123", Candidat.generate_candidats(5, t, t), [], t, t)
    map.liste_electeur.insert(0, Candidat("test", "test", 100, 100, 0, 0))
    map.generationTest(15, 25)
    return CreationSimulation(map, ModeVotes, k,type_votes)
