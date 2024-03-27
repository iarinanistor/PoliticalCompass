
import numpy as np
from Back.votes import *
from Back.Candidat import Candidat
from Back.Individus import Individus
import random
import logging 
from icecream import ic
class Map:
    def __init__ (self,bd,nom=None,liste_electeur=[],population=[],generationX=None,generationY=None):
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
        self.nom = nom
        self.liste_electeur = liste_electeur
        self.population=population
        self.L_population = None
        self.generationX = generationX
        self.generationY = generationY

        
    def generation(self): # genere la matrice des individus linéairement 
        '''
        Génère la population de manière linéaire dans une matrice.
        '''
        logging.info('<Map.generation>')
        self.population=[[Individus(((chr((ord('a')+(j%26))))*(i+1)), i, j, self.liste_electeur) for j in range(self.generationY)] for i in range(self.generationX)]
        #self.liste_electeur=Candidat.generate_candidats(10,self.generationX,self.generationY)
        logging.info('</Map.generation>')
        
    def generationAleatoire(self): 
        '''
        Génère la population de manière aléatoire dans une matrice.
        '''
        logging.info('<Map.generationAleatoire>')

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
        logging.info('</Map.generationAleatoire>')
    
    def refresh_Candidat(self):
        logging.info('<Map.refresh_Candidat>')

        for sous_liste in self.population:
            for ind in sous_liste:
                ind.liste_electeur = self.liste_electeur
        logging.info('</Map.refresh_Candidat>')

                
    def genereCand(self,nom,liste,dbt,fin):
        logging.info('<Map.genereCand> nom: {}, liste: {}, dbt: {}, fin: {}'.format(nom, liste, dbt, fin))

        if(random.random()<0.35): logging.info('</Map.genereCand>') ; return Individus(nom,int(random.uniform(0,dbt)),int(random.uniform(0,dbt)),liste)
        else: logging.info('</Map.genereCand>');  return Individus(nom,int(random.uniform(fin,self.generationX)),int(random.uniform(fin,self.generationY)),liste)
        
  
            
    def generationTest(self,dbt,fin):
        logging.info('<Map.generationTest> dbt: {}, fin: {}'.format(dbt, fin))
        self.population = [
            [ self.genereCand(
                    chr(ord('a') + (j % 26)),
                    self.liste_electeur,dbt,fin
                )
                for j in range(self.generationY)
            ]
            for i in range(self.generationX)
        ]
        logging.info('</Map.generationTest>')
        
    def refresh_Candidat(self):
        logging.info('<Map.refresh_Candidat>')
        for sous_liste in self.population:
            for ind in sous_liste:
                ind.liste_electeur = self.liste_electeur
        logging.info('</Map.refresh_Candidat>')
               
    def genere_L_Cand(self):
        logging.info('<Map.genere_L_Cand>')
        #creer une liste de cand depuis map 
        self.liste_electeur = Candidat.generate_candidats(len(self.liste_electeur),self.generationX,self.generationY)
        self.refresh_Candidat()
        logging.info('</Map.genere_L_Cand>')
        
    def creer_L_population(self):
        logging.info('<Map.creer_L_population>')
        self.L_population = concat(self.population)
        logging.info('</Map.creer_L_population>')
    
    def ajoute_candidat(self,newC):
        '''
        Ajoute un nouveau candidat à la liste des candidats.
        
        Parameters:
            newC (tuple): Tuple contenant les informations du nouveau candidat (nom, prénom, charisme, x, y).
        '''
        logging.info('<Map.ajoute_candidat> newC: {}'.format(newC))
        nom,prenom,charisme,x,y = newC
        candidat = Candidat(nom,prenom,int(charisme),20,int(x),int(y))
        self.liste_electeur.append(candidat)
        logging.info('</Map.ajoute_candidat> newC: {}'.format(newC))
         
    def listes_listes_votes(self): # genre la liste des listes des votes ordonnée de chaque indiv de la map
        '''
        Génère une liste de listes de votes ordonnée pour chaque individu de la carte.
        '''
        logging.info('<Map.listes_listes_votes>')
        l=[]
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                tmp=self.population[i][j].liste_vote()
                l.append(tmp)
        logging.info('</Map.listes_listes_votes>')
        return l

        
    def distance(self, point1, point2):
        '''
        Calcule la distance entre deux points.
        '''
        logging.info('<Map.distance> point1: {}, point2: {}'.format(point1, point2))
        distance = np.linalg.norm(point1 - point2)
        logging.info('<Map.distance> point1: {}, point2: {}'.format(point1, point2))
        return distance
    

    def Copeland(self, r=None):
        '''
        Trouve le gagnant de Copeland parmi les candidats.
        ''',
        logging.info('<Map.Copeland/>')
        if(r!=None):
            return copeland(self.liste_electeur, self.liste_poids(r))
        if(self.L_population == None): self.creer_L_population()
        return copeland(self.liste_electeur,self.L_population)

    def Copeland_MC(self):
        return copeland(self.liste_electeur,self.L_population)

    def Pluralite(self,r=None):
        '''
        Calcule le gagnant par la méthode de pluralité.
        '''
        logging.info('<Map.Pluralite/>')
        if(r!=None):
            return pluralite(self.liste_electeur,self.liste_poids(r))
        if(self.L_population == None): self.creer_L_population()
        return pluralite(self.liste_electeur,self.L_population)
        
    def Borda(self, r=None):
        '''
        Calcule le gagnant par la méthode de Borda.
        '''
        logging.info('<Map.Borda/>')
        if(r!=None):
            return borda(self.liste_electeur,self.liste_poids(r))
        if(self.L_population == None): self.creer_L_population()
        return borda(self.liste_electeur,self.L_population)
    
    def STV(self, r=None):
        '''
        Calcule le gagnant par la méthode de STV.
        '''
        logging.info('<Map.STV/>')
        if(r!=None):
            return stv(self.liste_electeur,self.liste_poids(r))
        if(self.L_population == None): self.creer_L_population()
        return stv(self.liste_electeur,self.L_population)
    
    def Approbation(self,nb_approbation, r=None):
        '''
        Calcule le gagnant par la méthode d'approbation avec un nombre spécifié de votes d'approbation.
        
        Parameters:
            nb_approbation (int): Nombre de votes d'approbation.
        '''
        logging.info('<Map.Approbation>')
        if(r!=None):
            return approbation(self.liste_electeur,self.liste_poids(r), nb_approbation)
        if(self.L_population == None): self.creer_L_population()
        return approbation(self.liste_electeur,self.L_population,nb_approbation)

    def delegation(electeurs_proximite):
        '''
        Parameters:
            electeurs_proximite : List[Individus]
        Returns:    
            Individus : L'électeur qui va recevoir le(s) vote(s)
        '''
        somme_niv = 0
        dico_proba = {}
        print(electeurs_proximite)
        # Calcul de la somme des niveaux de compétence pour la normalisation
        for electeur in electeurs_proximite:
            somme_niv += electeur.get_c()
            
        if somme_niv == 0:
            return None  # Ou lever une exception si approprié
            
        # On crée un dictionnaire qui associe un électeur et la probabilité normalisée qu'il reçoive le vote
        for electeur in electeurs_proximite:
            p = electeur.get_c() / somme_niv
            dico_proba[electeur] = p

        # Choix de l'électeur qui va recevoir le vote selon les probabilités normalisées
        choix = random.uniform(0, 1)
        proba_cumul = 0
        for electeur, proba in sorted(dico_proba.items(), key=lambda x: x[1], reverse=True):
            proba_cumul += proba
            if choix <= proba_cumul:
                return electeur
        
        # Ce point du code ne devrait normalement pas être atteint
        return None




            
    def liste_poids(self,rayon):
        """Met à jour le poids"""
        liste_individus = self.L_population
        l = liste_individus.copy()
        for ind in liste_individus:
            if random.random() < 1-(ind.c):
                #s'il delegue
                #electeurs_proximite=zone(ind,rayon)  renvoie les electeurs qui n'ont pas delegué dans la zone de l'individu
                choix = self.delegation(self.zone(ind,rayon))
                print(choix)
                print(choix.poids)
                choix.poids += ind.poids
                ind.poids = 0
                l.remove(ind)
            else : 
                continue
        return l
        
    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# gestion I / O
    def ecrire(self,nomFichier):
        '''
        Écrit les données de la carte dans un fichier.
        
        Parameters:
            nomFichier (str): Nom du fichier de sortie.
        '''
        logging.info('<Map.ecrire> nomFichier: {}'.format(nomFichier))
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
            logging.info('</Map.ecrire> nomFichier: {}'.format(nomFichier))
            
    def lire(self, nomFichier):
        '''
        Lit les données d'un fichier et retourne les candidats et la population.
        
        Parameters:
            nomFichier (str): Nom du fichier à lire.
        
        Returns:
            tuple: Tuple contenant une liste de candidats et une liste de populations.
        '''
        logging.info('<Map.lire> nomFichier: {}'.format(nomFichier))
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
        logging.info('</Map.lire> nomFichier: {}'.format(nomFichier))
        # Retourner les données lues
        return candidats, population
###############################################################################################################################
            

    def liste_to_matrice(self):
        '''
        Convertit une liste de population en matrice de population.
        '''
        logging.info('<Map.liste_to_matrice>')
        self.population = [[None] * self.generationX for _ in range(self.generationY)]
        for individus in self.L_population:
            self.population[individus.x][individus.y] = individus
        logging.info('</Map.liste_to_matrice>')  
         
    def chargement(self,nomfichier):
        '''
        Charge les données à partir d'un fichier spécifié.
        
        Parameters:
            nomfichier (str): Nom du fichier à charger.
        '''
        logging.info('<Map.chargement> nomfichier: {}'.format(nomfichier))
        candidats,L_population = self.lire(nomfichier)
        self.liste_electeur = candidats
        self.L_population = L_population
        self.liste_to_matrice()
        logging.info('</Map.chargement> nomfichier: {}'.format(nomfichier))

    def zone(self, ind, r):
        """
        permet de creer une zone autour d'un individu ind de rayon r
        """
        liste = []
        for x in range(max(0, ind.x - r), min(self.generationX, ind.x + r + 1)):
            for y in range(max(0, ind.y - r), min(self.generationY, ind.y + r + 1)):
                if (((x != ind.x and y != ind.y) and (self.population[x][y].poids >= 1)) and (ind.nom != self.population[x][y].nom)):
                    print(x,y)
                    liste.append(self.population[x][y])
        print(liste)
        return liste
    
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

