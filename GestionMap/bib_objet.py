import numpy as np
import Condorsait as Cond
import random

class Individus:
    def __init__(self, nom=None, x=None, y=None,liste_electeur=None):
        self.nom = nom
        self.x = x
        self.y = y
        self.map = map
        self.liste_electeur = liste_electeur
        
    def liste_vote(self):
        liste_des_votes = [(np.linalg.norm(np.array([i.x, i.y]) - np.array([self.x, self.y])), i.nom) for i in self.liste_electeur]
        l=sorted(liste_des_votes, key=lambda x: x[0])
        return [ nom for distance,nom in l]

class Map:
    def __init__ (self,nom=None,liste_electeur=[],population=[],generationX=None,generationY=None):
        self.nom = nom
        self.liste_electeur = liste_electeur
        self.population=population 
        self.generationX = generationX
        self.generationY = generationY
        
    def generation(self): # genere la matrice des individus linéairement 
        
        self.population=[[Individus(((chr((ord('a')+(j%26))))*(i+1)), i, j, self.liste_electeur) for j in range(self.generationY)] for i in range(self.generationX)]
    
    def generationAleatoire(self): 
    # Génère la matrice des individus aléatoirement
        self.population = [
            [
                Individus(
                    chr(ord('a') + (j % 26)) * (i + 1),
                    int(random.random() * self.generationX),
                    int(random.random() * self.generationY),
                    self.liste_electeur
                )
                for j in range(self.generationY)
            ]
            for i in range(self.generationX)
        ]

        
    def listes_listes_votes(self): # genre la liste des listes des votes ordonnée de chaque indiv de la map
        l=[]
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                tmp=self.population[i][j].liste_vote()
                l.append(tmp)
        return l
    
    def distance(self, point1, point2):
        distance = np.linalg.norm(point1- point2)
        return distance
    
    def condorsait(self):
        from Condorsait import all_combat
        return Cond.all_combat(self.listes_listes_votes())

#Pour tester
l=["MOI","PAS TOI","UN AUTRE","BERNARD","MICHELLE"]
electeur=[Individus("victor",-10,10),Individus("Isaac",0,0),Individus("Lyna",-5,-25),Individus("chaby",-30,-30)]
population=[[Individus("1",10,10,electeur),Individus("2",0,0,electeur)],[Individus("3",-5,-5,electeur),Individus("quatre",-10,-10,electeur)]]
map=Map("France",electeur,population)
print(map.condorsait())
map2=Map("France",[],[],5,6)
map2.generationAleatoire()
for i in range(len(map2.population)):
    for ind in (map2.population[i]):
        print(ind.nom,ind.x,ind.y,"\n")