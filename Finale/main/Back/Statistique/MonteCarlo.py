from Back.Map import *
from Back.Candidat import *
import time
from PySide6.QtWidgets import QApplication
from Front.Widgets.MapQT import *
import multiprocessing
import time
import sys

def generate_unique_colors(int1, int2):
        # Utilisation des entiers pour calculer les composantes RGB
        r =  int(int1) % 256
        g =  int(int2) % 256
        b = int(int1 * int2) % 256
        return QColor(r, g, b)
    
def creer_sous_maps(map_carrer, k):
    sous_maps = []
    taille_map = len(map_carrer)
    
    # Parcourir les lignes de la carte carrée avec un pas de k
    for i in range(0, taille_map, k):
        # Parcourir les colonnes de la carte carrée avec un pas de k
        for j in range(0, taille_map, k):
            sous_map = []
            # Extraire une sous-carte de taille k
            for x in range(i, min(i + k, taille_map)):
                sous_map.append(map_carrer[x][j:min(j + k, taille_map)])
            # Ajouter la sous-carte à la liste
            sous_maps.append(sous_map)
    
    return sous_maps

def election_multiple(map_carrer, start, end, k):
    l=[]
    for i in range(start, end, k):
        #map_carrer.genere_L_Cand()
        map_carrer.liste_electeur[0] = Candidat.genere_candidat(i % (map_carrer.generationX), i // (map_carrer.generationY))
        l.append( map_carrer.Copeland_MC())
        
    return l

def worker(map_carrer, start, end, k, output):
    output.append(election_multiple(map_carrer, start, end, k))

def Monte_Carlo(map_carrer, k):
    map_carrer.creer_L_population()
    res = []
    jobs = []
    output = multiprocessing.Manager().list()
    print("Début : des tours")
    start_time = time.time()
    for i in range(map_carrer.generationX):
        process = multiprocessing.Process(target=worker, args=(map_carrer, i * map_carrer.generationX, (i + 1) * map_carrer.generationY, k, output))
        jobs.append(process)
        process.start()

    for process in jobs:
        process.join()

    for result in output:
        res+=result
        
    print("Fin des tours ", time.time() - start_time)
    return res

def moyenne_couples(l):
    # Aplatir la liste de listes
    X=0
    Y=0
    t=len(l)
    for ind in l:
        X+=ind.x()
        Y+=ind.y()
    return (X/t, Y/t)

def CreationSimulation(map,nom,k):
    mc = Monte_Carlo(map,k)
    x,y=moyenne_couples(mc)
    
    map.liste_electeur.append(Candidat("test","test",100,100,x,y))
    
    gg = map.Copeland()
    print("test 1",gg.nom())
    
    gg = map.Copeland()
    print("test 2",gg.nom())
    
    gg = map.Copeland()
    print("test 3",gg.nom())
    
    gg = map.Copeland()
    print("test 4",gg.nom())
    hitmap = HitMap(map.generationX)
    hitmap.placeALL(map,mc,(x,y))
    return hitmap

def SimulationAleatoire(ModeVotes,t,k):
    """ t int:  taille de la map
        ModeVotes str: dtype de votes
        k iny : le pas 
    """
    map = Map(None,"123",Candidat.generate_candidats(5,t,t),[],t,t)
    map.liste_electeur.insert(0,Candidat("test","test",100,100,0,0))
    map.generationTest(15,25)
    return CreationSimulation(map,ModeVotes,k)
