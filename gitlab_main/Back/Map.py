
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
        self.bd = bd
        self.taille_population = 2000
        
    def genere_unique_id(self,x,y):
        
        """
        peremt de genere un id unique en fonction de x en y 2 int 
        """
        
        if x==y :return chr(x)+chr(y)+chr(random.randint(0,x))
        return chr(x)+chr(y)
       
    def generation_pers(self,zone,type_generation,n):
        print('generation',type_generation,zone,n)
        if type_generation == "Triangulaire":
            self.generationPopulationTriangulaire(zone,n)
        elif type_generation == "Uniforme":
            self.generationPopulationUnif(zone,n)
        elif type_generation == "Exponentiel":
            self.generationPopulationExpo(zone,n)
        elif type_generation == "Beta":
            self.generationPopulationBeta(zone,n)
        else : raise ValueError("type_generation no trouver ")
        
        
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
                    self.genere_unique_id(i,j),
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
    
    def generationPopulationTriangulaire(self,zone,n):
        """
        Genere la population de maniere triangulaire dans une zone donne
        la zone est  de la forme (x, y, r) ou:
        x = coordonne x du centre de la zone
        y = coordonne y du centre de la zone
        r = le rayon de la zone
        """
        indexes = []
        x,y,r=zone
        for i in range(self.generationX):
            for j in range(self.generationY):
                # Calculer la distance entre le point actuel et le centre
                distance = ((i - x) ** 2 + (j - y) ** 2) ** 0.5
                # Si la distance est dans le rayon, ajouter l'index à la liste
                if distance <= r:
                    indexes.append((i, j))  # Format (ligne, colonne)

        #compteur pour les noms
        ind_nom=0
        for _ in range(n):
            x_pivot = random.triangular(x - r, x + r)
            y_pivot = random.triangular(y - r, y + r)
            #x_pivot et y_pivot sont des floats, donc on veut trouver les indexes les plus proches
            index_plus_proche = min(indexes,key=lambda idx: (idx[0] - y_pivot) ** 2 + (idx[1] - x_pivot) ** 2)
            nom = (str(ind_nom+1))
            i,j = index_plus_proche
            if self.population[i][j] != None:
                ind = self.population[i][j]
                ind.c.append(random.uniform(0, 1))
                ind.poids.append(1)
                ind.nom.append(nom)
            else:
                self.population[i][j] = Individus(nom,x=i,y=j,liste_electeur=self.liste_electeur)
            ind_nom+=1


    
    def generationPopulationBeta(self,zone,n):
        """
        Genere la population avec la loi beta dans une zone donne
        la zone est  de la forme (x, y, r) ou:
        x = coordonne x du centre de la zone
        y = coordonne y du centre de la zone
        r = le rayon de la zone
        """
        indexes = []
        x,y,r=zone
        for i in range(self.generationX):
            for j in range(self.generationY):
                # Calculer la distance entre le point actuel et le centre
                distance = ((i - x) ** 2 + (j - y) ** 2) ** 0.5
                # Si la distance est dans le rayon, ajouter l'index à la liste
                if distance <= r:
                    indexes.append((i, j))  # Format (ligne, colonne)

        #compteur pour les noms
        ind_nom=0
        for _ in range(n):
            x_pivot = random.betavariate(2, 5) * 2 * r + (x - r)
            y_pivot = random.betavariate(2, 5) * 2 * r + (y - r)
            #x_pivot et y_pivot sont des floats, donc on veut trouver les indexes les plus proches
            index_plus_proche = min(indexes,key=lambda idx: (idx[0] - y_pivot) ** 2 + (idx[1] - x_pivot) ** 2)
            nom = (str(ind_nom+1))
            i,j = index_plus_proche
            if self.population[i][j] != None:
                ind = self.population[i][j]
                ind.c.append(random.uniform(0, 1))
                ind.poids.append(1)
                ind.nom.append(nom)
            else:
                self.population[i][j] = Individus(nom,x=i,y=j,liste_electeur=self.liste_electeur)
            ind_nom+=1

    def generationPopulationExpo(self,zone,n):
        """
        Genere la population de maniere exponentielle dans une zone donne
        la zone est  de la forme (x, y, r) ou:
        x = coordonne x du centre de la zone
        y = coordonne y du centre de la zone
        r = le rayon de la zone
        """
        indexes = []
        x,y,r=zone
        for i in range(self.generationX):
            for j in range(self.generationY):
                # Calculer la distance entre le point actuel et le centre
                distance = ((i - x) ** 2 + (j - y) ** 2) ** 0.5
                # Si la distance est dans le rayon, ajouter l'index à la liste
                if distance <= r:
                    indexes.append((i, j))  # Format (ligne, colonne)

        #compteur pour les noms
        ind_nom=0
        for _ in range(n):
            x_pivot = random.expovariate(1) * 2 * r + (x - r)
            y_pivot = random.expovariate(1) * 2 * r + (y - r)
            #x_pivot et y_pivot sont des floats, donc on veut trouver les indexes les plus proches
            index_plus_proche = min(indexes,key=lambda idx: (idx[0] - y_pivot) ** 2 + (idx[1] - x_pivot) ** 2)
            nom = (str(ind_nom+1))
            i,j = index_plus_proche
            if self.population[i][j] != None:
                ind = self.population[i][j]
                ind.c.append(random.uniform(0, 1))
                ind.poids.append(1)
                ind.nom.append(nom)
            else:
                self.population[i][j] = Individus(nom,x=i,y=j,liste_electeur=self.liste_electeur)
            ind_nom+=1
        
    def generationPopulationUnif(self,zone,n):
        """
        Genere la population avec la loi beta dans une zone donne
        la zone est  de la forme (x, y, r) ou:
        x = coordonne x du centre de la zone
        y = coordonne y du centre de la zone
        r = le rayon de la zone
        """
        indexes = []
        x,y,r=zone
        for i in range(self.generationX):
            for j in range(self.generationY):
                # Calculer la distance entre le point actuel et le centre
                distance = ((i - x) ** 2 + (j - y) ** 2) ** 0.5
                # Si la distance est dans le rayon, ajouter l'index à la liste
                if distance <= r:
                    indexes.append((i, j))  # Format (ligne, colonne)

        #compteur pour les noms
        ind_nom=0
        for _ in range(n):
            x_pivot = random.uniform(x - r, x + r)
            y_pivot = random.uniform(y - r, y + r)
            #x_pivot et y_pivot sont des floats, donc on veut trouver les indexes les plus proches
            index_plus_proche = min(indexes,key=lambda idx: (idx[0] - y_pivot) ** 2 + (idx[1] - x_pivot) ** 2)
            nom = (str(ind_nom+1))
            i,j = index_plus_proche
            if self.population[i][j] != None:
                ind = self.population[i][j]
                ind.c.append(random.uniform(0, 1))
                ind.poids.append(1)
                ind.nom.append(nom)
            else:
                self.population[i][j] = Individus(nom,x=i,y=j,liste_electeur=self.liste_electeur)
            ind_nom+=1

    
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
    
    def ajoute_candidat(self,candidat):
        '''
        Ajoute un nouveau candidat à la liste des candidats.
        
        Parameters:
            candidat: nouveau candidat à ajouter.
        '''
        logging.info('<Map.ajoute_candidat> newC: {}'.format(candidat))
        self.liste_electeur.append(candidat)
        logging.info('</Map.ajoute_candidat> newC: {}'.format(candidat))
         
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

    def candidat_prefere(self,cand1,cand2):
        """
        Détermine le candidat préféré entre deux options, basé sur les votes pondérés de la population.

        Cette fonction parcourt la liste des individus et accumule les poids des votes pour chaque candidat. Le candidat
        avec le poids total le plus élevé est considéré comme le préféré.

        :param cand1: Premier candidat à comparer.
        :param cand2: Deuxième candidat à comparer.
        :return: Le candidat préféré basé sur le total des poids des votes.
        """
        if self.L_population == [] : self.creer_L_population()
        cpt1,cpt2=0,0
        for ind in self.L_population:
            for cand in ind.liste_vote():
                if cand.id == cand1.id:
                    cpt1+=sum(ind.poids); break
                elif cand.id == cand2.id:
                    cpt2+=sum(ind.poids); break
        print("p1",cpt1,"CPT2",cpt2)
        if cpt2>cpt1: return cand2
        return cand1
    
    @staticmethod
    def generate_matches(elements):
        """
        Génère des paires de tous les éléments fournis pour les comparer deux à deux.

        :param elements: Liste des éléments à appairer.
        :return: Liste des tuples contenant chaque paire possible sans répétition.
        """
        matches = []
        # Boucle sur chaque élément pour le jumeler avec chaque autre élément
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                matches.append((elements[i], elements[j]))
        return matches
    
    def contraite_tournoi(self, liste_candidat=None):
        """
        Crée un dictionnaire où chaque clé est un candidat et les valeurs associées à chaque clé sont une liste des candidats contre lesquels il a gagné.
        
        Cette méthode utilise `generate_matches` pour créer toutes les combinaisons de matchs possibles, puis utilise `candidat_prefere`
        pour déterminer le gagnant de chaque match. Les résultats sont accumulés dans un dictionnaire qui trace les victoires de chaque candidat.

        :param liste_candidat: Liste optionnelle des candidats. Si None, utilise `liste_electeur` de l'instance.
        :return: Dictionnaire avec l'ID de chaque candidat comme clé et la liste des IDs des candidats qu'ils ont battus.
        """
        if liste_candidat is None:
            liste_candidat = self.liste_electeur
        victoire_defaite = {cand.id: [] for cand in liste_candidat}  # Initialisation du dictionnaire pour suivre les victoires
        for match in Map.generate_matches(liste_candidat):
            cand1, cand2 = match
            winner = self.candidat_prefere(cand1, cand2)
            if winner.id == cand1.id:
                victoire_defaite[winner.id].append(cand2.id)
            else:
                victoire_defaite[winner.id].append(cand1.id)
        return victoire_defaite
                
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

    def Monte_carlo_vote(self,type_votes):
        if(type_votes == "Copeland"): return copeland(self.liste_electeur,self.L_population)
        elif( type_votes == "Borda"): return borda(self.liste_electeur,self.L_population)
        elif (type_votes == "STV"): return stv(self.liste_electeur,self.L_population)
        elif ( type_votes == "Pluralite"): return pluralite(self.liste_electeur,self.L_population)
        else: raise ValueError(" type_votes non reconnu Monte_carlo in map ")
        
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
    
    def affiche(self):
        for liste in self.population:
            for ind in liste:
                if ind == None : print("0 ", end='')  
                else: print("1",end = " ") 
            print("\n")
            
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
        
    def ecrire(self,nomFichier):
        '''
        Écrit les donnees de la carte dans un fichier.
        
        Parameters:
            nomFichier (str): Nom du fichier ou les donnees seront ecrites.
        
        Returns:
            void
        '''
        if nomFichier == "":
            print("Veuillez entrer le nom du fichier où enregistrer")
        else:
            logging.info('<Map.ecrire> nomFichier: {}'.format(nomFichier))
            with open(nomFichier, "w") as fichier:
                fichier.write(str(self.generationX)+"\n")
                fichier.write(str(self.generationY)+"\n")
                fichier.write("<candidat> \n")
                for cd in self.liste_electeur:
                    fichier.write(str(cd.nom()) + " " + str(cd.prenom()) + " " + str(cd.charisme()) + " " + str(cd.age()) + " " + str(cd.x()) + " " + str(cd.y()) + "\n")
                fichier.write("</candidat> \n")  # Fermez la balise candidat

                fichier.write("<population> \n")
                for liste_ind in self.population:
                    for ind in liste_ind:
                        if ind != None: 
                            # Ecriture de la liste des noms
                            fichier.write(str("["))
                            for i in range (len(ind.nom)):
                                fichier.write(str(ind.nom[i]))
                                if (i+1 < len(ind.nom)):
                                    fichier.write(str(","))
                            fichier.write(str("] "))

                            #Ecriture des coordonnees x et y
                            fichier.write(str(ind.x) + " " + str(ind.y) + " ")
                            
                            #Ecriture de la liste des poids
                            fichier.write(str("["))
                            for i in range (len(ind.poids)):
                                fichier.write(str(ind.poids[i]))
                                if (i+1 < len(ind.poids)):
                                    fichier.write(str(","))
                            fichier.write(str("] "))

                            #Ecriture de la liste des c
                            fichier.write(str("["))
                            for i in range (len(ind.c)):
                                fichier.write(str(ind.c[i]))
                                if (i+1 < len(ind.c)):
                                    fichier.write(str(","))
                            fichier.write(str("] "))

                            #Ecriture de la liste des adelegue
                            fichier.write(str("["))
                            for i in range (len(ind.adelegue)):
                                fichier.write(str(ind.adelegue[i]))
                                if (i+1 < len(ind.adelegue)):
                                    fichier.write(str(","))
                            fichier.write(str("]"))

                            fichier.write("\n")

                fichier.write("</population> \n")  # Fermez la balise population
                fichier.close()  
                logging.info('</Map.ecrire> nomFichier: {}'.format(nomFichier))


    def lire(self, nomFichier):
        '''
        Lit les données dans un fichier et retourne les candidats et la population.
        
        Parameters:
            nomFichier (str): Nom du fichier à lire.
        
        Returns:
            candidats, population: Tuple contenant une liste de candidats et une liste de populations.
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
                        candidats.append(Candidat(nom, prenom, int(charisme), int(age), int(float(x)), int(float(y))))
                        
                elif ligne.startswith("<population>"):
                    en_population = True
                elif ligne.startswith("</population>"):
                    en_population = False
                elif en_population:
                    # Diviser la ligne en éléments individuels
                    elements = ligne.split()
                    if len(elements) == 6:  # Vérifier si la ligne contient le bon nombre d'éléments
                        liste_nom, x_coord, y_coord, liste_poids, liste_c, liste_adelegue = elements
                        
                        liste_nom = liste_nom.strip('[]')
                        liste_nom = [nom.strip() for nom in liste_nom.split(',')]
                        x_coord = int(x_coord)
                        y_coord = int(y_coord)
                        liste_poids = liste_poids.strip('[]')
                        liste_poids = [int(poids.strip()) for poids in liste_poids.split(',')]
                        liste_c = liste_c.strip('[]')
                        liste_c = [float(c.strip()) for c in liste_c.split(',')]
                        liste_adelegue = liste_adelegue.strip('[]')
                        liste_adelegue = [bool(adelegue.strip()) for adelegue in liste_adelegue.split(',')]
                        new = Individus(x=x_coord,y=y_coord,liste_electeur=candidats)
                        new.nom = liste_nom
                        new.poids = liste_poids
                        new.c = liste_c
                        new.adelegue = liste_adelegue
                        population.append(new)

        logging.info('</Map.lire> nomFichier: {}'.format(nomFichier))
        # Retourner les données lues
        return candidats, population

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
  
#  Fonction supplémentaire qui ne nécessite pas d'être intégrée dans la classe.

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
    Concatenate lists or arrays in a given matrix, excluding None or empty arrays.
    
    Parameters:
        matrix (list): List containing sub-lists or arrays to concatenate.

    Returns:
        list: A list containing all non-None and non-empty elements from the sub-lists or arrays.
    '''
    return [element for sous_liste in matrix for element in sous_liste if element is not None]


