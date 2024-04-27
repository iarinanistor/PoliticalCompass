import random
from Back.Map import Map
from Back.Candidat import Candidat
from Back.Individus import Individus
from Back.votes import *

cand1 = Candidat("Martin","chloe",4,50,60,60)
cand2 = Candidat("Grand","Nathan",5,46,42,55)
cand3 = Candidat("Petit","John",3,42,15,15)
l_candidats = [cand1,cand2,cand3]
ind1 =Individus("1",10,10,l_candidats)
ind2 =Individus("2",50,50,l_candidats)
population=[[ind1,ind2]]
map=Map(None,"France",l_candidats,population,5,5)

tab = [[ind2, None, None, None],
       [None,None , ind1, None],
       [None,None , None, None]]

def selectionner_indexes_dans_zone(tab, centre_x, centre_y, rayon):
    indexes_dans_rayon = []
    for x in range(len(tab)):
        for y in range(len(tab[0])):
            # Calculer la distance entre le point actuel et le centre
            distance = ((x - centre_x) ** 2 + (y - centre_y) ** 2) ** 0.5
            # Si la distance est dans le rayon, ajouter l'index à la liste
            if distance <= rayon:
                indexes_dans_rayon.append((x, y))  # Format (ligne, colonne)
    
    return indexes_dans_rayon

def generation_uniforme(tab,zone,n):
    x,y,r=zone
    indexes = selectionner_indexes_dans_zone(tab,x,y,r)
    for _ in range(n):
        x_pivot = random.triangular(x - r, x + r)
        y_pivot = random.triangular(y - r, y + r)
        index_plus_proche = min(indexes,key=lambda idx: (idx[0] - y_pivot) ** 2 + (idx[1] - x_pivot) ** 2)
        i,j = index_plus_proche
        if tab[i][j] != None:
            ind = tab[i][j]
            ind.c.append(random.uniform(0, 1))
            ind.poids.append(1)
        else:
            tab[i][j] = Individus("no",x=i,y=j,liste_electeur=l_candidats)


centre_x = 1.5 # Exemple de coordonnée x du centre
centre_y = 1.5  # Exemple de coordonnée y du centre
rayon = 1    # Exemple de rayon

indexes = selectionner_indexes_dans_zone(tab, centre_x, centre_y, rayon)
print("Indexes dans la zone spécifiée :", indexes)