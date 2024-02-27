import numpy as np
from Back.votes import  copeland,borda,approbation,pluralite,stv
from Back.Candidat import Candidat
from Back.Individus import Individus
import random

class Map:
    def __init__ (self,bd,nom=None,liste_electeur=[],population=[],generationX=None,generationY=None):
        self.nom = nom
        self.liste_electeur = liste_electeur
        self.population=population
        self.L_population = None 
        self.generationX = generationX
        self.generationY = generationY

        
    def generation(self): # genere la matrice des individus linéairement 
        
        self.population=[[Individus(((chr((ord('a')+(j%26))))*(i+1)), i, j, self.liste_electeur) for j in range(self.generationY)] for i in range(self.generationX)]
        #self.liste_electeur=Candidat.generate_candidats(10,self.generationX,self.generationY)
    
    def generationAleatoire(self): 
    # Génère la matrice des individus aléatoirement
        self.population = [
            [
                Individus(
                    chr(ord('a') + (j % 26)),
                    int(random.random() * self.generationX),
                    int(random.random() * self.generationY),
                    self.liste_electeur
                )
                for j in range(self.generationY)
            ]
            for i in range(self.generationX)
        ]
        #self.liste_electeur=Candidat.generate_candidats(10,self.generationX,self.generationY)

    def ajoute_candidat(self,newC):
        nom,prenom,charisme,x,y = newC
        candidat = Candidat(nom,prenom,int(charisme),20,int(x),int(y))
        self.liste_electeur.append(candidat)
        
         
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
    

    def Copeland(self):
        return copeland(self.liste_electeur,concat(self.population))
    
    def Pluralite(self):
        print("MAP",self.liste_electeur,concat(self.population)[0])
        return pluralite(self.liste_electeur,concat(self.population))
        
    def Borda(self):
        return borda(self.liste_electeur,concat(self.population))
    def STV(self):
        return stv(self.liste_electeur,concat(self.population))
    
    def Approbation(self,nb_approbation):
        return approbation(self.liste_electeur,concat(self.population),nb_approbation)
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# gestion I / O
    def ecrire(self,nomFichier):
        with open(nomFichier, "w") as fichier:
            fichier.write( str(self.generationX)+"\n")
            fichier.write( str(self.generationY)+"\n")
            fichier.write("<candidat> \n")   
            for cd in self.liste_electeur:
                fichier.write(str(cd.nom()) + " " + str(cd.prenom()) + " " + str(cd.charisme()) + " " + str(cd.age()) + " " + str(cd.x()) + " " + str(cd.y()) + "\n")
            fichier.write("</candidat> \n")  # Fermez la balise candidat

            fichier.write("<population> \n")
            for liste_ind in self.population:
                for ind in liste_ind:
                    if ind != None: fichier.write(str(ind.nom) + " " + str(ind.x) + " " + str(ind.y) + "\n")
            fichier.write("</population> \n")  # Fermez la balise population
            fichier.close()  
    
    def lire(self, nomFichier):
        with open(nomFichier, "r") as fichier:
            self.generationX = int(fichier.readline())  # Lire la première ligne pour obtenir la taille x
            self.generationY = int(fichier.readline())  # Lire la deuxième ligne pour obtenir la taille y
            candidats = []
            population = []

            en_candidats = False
            en_population = False

            for ligne in fichier:
                ligne = ligne.strip()  # Supprimer les espaces en début et fin de ligne
                
                if ligne.startswith("<candidat>"):
                    en_candidats = True
                elif ligne.startswith("</candidat>"):
                    en_candidats = False
                elif en_candidats:
                    # Diviser la ligne en éléments individuels
                    elements = ligne.split()
                    if len(elements) == 6:  # Vérifier si la ligne contient le bon nombre d'éléments
                        # Ajouter les données des candidats à une liste
                        nom, prenom, charisme, age, x, y = elements
                        candidats.append(Candidat(nom, prenom, int(charisme), int(age), int(x), int(y)))
                        
                elif ligne.startswith("<population>"):
                    en_population = True
                elif ligne.startswith("</population>"):
                    en_population = False
                elif en_population:
                    # Diviser la ligne en éléments individuels
                    elements = ligne.split()
                    if len(elements) == 3:  # Vérifier si la ligne contient le bon nombre d'éléments
                        # Ajouter les données de la population à une liste
                        nom, x_coord, y_coord = elements
                        population.append(Individus(nom, int(x_coord), int(y_coord), candidats))

        # Retourner les données lues
        return candidats, population
    
    def liste_to_matrice(self):
        self.population = [[None] * self.generationX for _ in range(self.generationY)]
        for individus in self.L_population:
            self.population[individus.x][individus.y] = individus
            
    def chargement(self,nomfichier):
        candidats,L_population = self.lire(nomfichier)
        self.liste_electeur = candidats
        self.L_population = L_population
        self.liste_to_matrice()

    

def concat(matrix):
    '''
    Parameters:
        matrix : list[liste[x]]
    Returns:
        liste[x] : la concatenation des listes dans la matrice
    '''
    l = []
    for i in range(len(matrix)):
        if matrix[i] != None: l+=matrix[i]
    return list(filter(lambda x: x is not None, l))
