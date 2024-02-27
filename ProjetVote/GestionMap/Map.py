import numpy as np
from Back.votes import all_combat, borda, approbation, pluralite, stv
from Back.Candidat import Candidat
from Back.Individus import Individus
import random

class Map:
    def __init__ (self, bd, nom=None, liste_electeur=[], population=[], generationX=None, generationY=None):
        '''
        Initialise un objet Map avec les attributs spécifiés.
        
        Parameters:
            bd: Inconnu, utilisé dans le code mais non défini dans les arguments.
            nom (str): Nom de la carte.
            liste_electeur (list): Liste des candidats.
            population (list): Liste des individus.
            generationX (int): Nombre de colonnes dans la génération de la carte.
            generationY (int): Nombre de lignes dans la génération de la carte.
        '''
        self.nom = nom  # Nom de la carte
        self.liste_electeur = liste_electeur  # Liste des candidats
        self.population = population  # Liste des individus
        self.L_population = None  # Liste temporaire pour la population
        self.generationX = generationX  # Nombre de colonnes dans la génération de la carte
        self.generationY = generationY  # Nombre de lignes dans la génération de la carte
        
    def generation(self): # genere la matrice des individus linéairement 
        '''
        Génère la population de manière linéaire dans une matrice.
        '''
        self.population = [[Individus(((chr((ord('a')+(j%26))))*(i+1)), i, j, self.liste_electeur) for j in range(self.generationY)] for i in range(self.generationX)]
    
    def generationAleatoire(self): 
        '''
        Génère la population de manière aléatoire dans une matrice.
        '''
        self.population = [[Individus(chr(ord('a') + (j % 26)) * (i + 1), int(random.random() * self.generationX), int(random.random() * self.generationY), self.liste_electeur) for j in range(self.generationY)] for i in range(self.generationX)]
        
    def ajoute_candidat(self,newC):
        '''
        Ajoute un nouveau candidat à la liste des candidats.
        
        Parameters:
            newC (tuple): Tuple contenant les informations du nouveau candidat (nom, prénom, charisme, x, y).
        '''
        nom, prenom, charisme, x, y = newC
        candidat = Candidat(nom, prenom, int(charisme), 20, int(x), int(y))
        self.liste_electeur.append(candidat)
        
    def listes_listes_votes(self): 
        '''
        Génère une liste de listes de votes ordonnée pour chaque individu de la carte.
        '''
        l=[]
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                tmp=self.population[i][j].liste_vote()
                l.append(tmp)
        return l
    
    def distance(self, point1, point2):
        '''
        Calcule la distance entre deux points.
        '''
        distance = np.linalg.norm(point1- point2)
        return distance
    
    def condorcet(self):
        '''
        Trouve le gagnant de Condorcet parmi les candidats.
        '''
        l=all_combat(self.listes_listes_votes())
        return list(l.keys())[0]
    
    def Pluralite(self):
        '''
        Calcule le gagnant par la méthode de pluralité.
        '''
        return pluralite(self.liste_electeur, concat(self.population))
        
    def Borda(self):
        '''
        Calcule le gagnant par la méthode de Borda.
        '''
        return borda(self.liste_electeur, concat(self.population))
    
    def STV(self):
        '''
        Calcule le gagnant par la méthode de STV.
        '''
        return stv(self.liste_electeur, concat(self.population))
    
    def Approbation(self, nb_approbation):
        '''
        Calcule le gagnant par la méthode d'approbation avec un nombre spécifié de votes d'approbation.
        
        Parameters:
            nb_approbation (int): Nombre de votes d'approbation.
        '''
        return approbation(self.liste_electeur, concat(self.population), nb_approbation)
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    # gestion I / O
    def ecrire(self,nomFichier):
        '''
        Écrit les données de la carte dans un fichier.
        
        Parameters:
            nomFichier (str): Nom du fichier de sortie.
        '''
        with open(nomFichier, "w") as fichier:
            fichier.write( str(self.generationX)+"\n")
            fichier.write( str(self.generationY)+"\n")
            fichier.write("<candidat> \n")   
            for cd in self.liste_electeur:
                fichier.write(str(cd.nom()) + " " + str(cd.prenom()) + " " + str(cd.charisme()) + " " + str(cd.age()) + " " + str(cd.x()) + " " + str(cd.y()) + "\n")
            fichier.write("</candidat> \n")  

            fichier.write("<population> \n")
            for liste_ind in self.population:
                for ind in liste_ind:
                    if ind != None: fichier.write(str(ind.nom) + " " + str(ind.x) + " " + str(ind.y) + "\n")
            fichier.write("</population> \n")  
            fichier.close()  
    
    def lire(self, nomFichier):
        '''
        Lit les données d'un fichier et retourne les candidats et la population.
        
        Parameters:
            nomFichier (str): Nom du fichier à lire.
        
        Returns:
            tuple: Tuple contenant une liste de candidats et une liste de populations.
        '''
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
        '''
        Convertit une liste de population en matrice de population.
        '''
        self.population = [[None] * self.generationX for _ in range(self.generationY)]
        for individus in self.L_population:
            self.population[individus.x][individus.y] = individus
            
    def chargement(self,nomfichier):
        '''
        Charge les données à partir d'un fichier spécifié.
        
        Parameters:
            nomfichier (str): Nom du fichier à charger.
        '''
        candidats, L_population = self.lire(nomfichier)
        self.liste_electeur = candidats
        self.L_population = L_population
        self.liste_to_matrice()  # Convertit la liste de population en matrice de population



    

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
