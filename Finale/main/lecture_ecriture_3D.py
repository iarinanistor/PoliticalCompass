# gestion I / O 3D
    def ecrire_3D(self,nomFichier):
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
                fichier.write( str(self.generationX)+"\n")
                fichier.write( str(self.generationY)+"\n")
                fichier.write( str(self.generationZ)+"\n")
                fichier.write("<candidat> \n")   
                for cd in self.liste_electeur:
                    fichier.write(str(cd.nom()) + " " + str(cd.prenom()) + " " + str(cd.charisme()) + " " + str(cd.age()) + " " + str(cd.x()) + " " + str(cd.y()) + " " + str(cd.z()) + "\n")
                fichier.write("</candidat> \n")  # Fermez la balise candidat

                fichier.write("<population> \n")
                for liste_ind in self.population:
                    for ind in liste_ind:
                        if ind != None: 
                            fichier.write(str(ind.nom) + " " + str(ind.x) + " " + str(ind.y) + " " + str(ind.z) + "\n")

                fichier.write("</population> \n")  # Fermez la balise population
                fichier.close()  
                logging.info('</Map.ecrire_3D> nomFichier: {}'.format(nomFichier))


    def lire_3D(self, nomFichier):
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
            self.generationZ = int(fichier.readline())  # Lire la troisième ligne pour obtenir la taille z
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
                    if len(elements) == 7:  # Vérifier si la ligne contient le bon nombre d'éléments
                        # Ajouter les données des candidats à une liste
                        nom, prenom, charisme, age, x, y, z = elements
                        candidats.append(Candidat(nom, prenom, int(charisme), int(age), int(x), int(y), int(z)))
                        
                elif ligne.startswith("<population>"):
                    en_population = True
                elif ligne.startswith("</population>"):
                    en_population = False
                elif en_population:
                    # Diviser la ligne en éléments individuels
                    elements = ligne.split()
                    if len(elements) == 4:  # Vérifier si la ligne contient le bon nombre d'éléments
                        # Ajouter les données de la population à une liste
                        nom, x_coord, y_coord, z_coord = elements
                        population.append(Individus(nom, int(x_coord), int(y_coord), int(z_coord), candidats))
        logging.info('</Map.lire_3D> nomFichier: {}'.format(nomFichier))
        # Retourner les données lues
        return candidats, population



    def liste_to_liste3D(self):
        '''
        Convertit une liste de population en matrice de population.
        '''
        logging.info('<Map.liste_to_matrice>')
        self.population3D = [[[None] * self.generationZ for _ in range(self.generationZ)] * self.generationX for _ in range(self.generationY)]
        for individus in self.L_population:
            self.population[individus.x][individus.y][individus.z] = individus
        logging.info('</Map.liste_to_matrice>')
        
    def chargement(self,nomfichier):
        '''
        Charge les données à partir d'un fichier specifie.
        
        Parameters:
            nomfichier (str): Nom du fichier à charger.
        
        Returns:
            void
        '''
        if nomfichier == "":
            print("Veuillez entrer le nom du fichier a charger")
        else:
            logging.info('<Map.chargement> nomfichier: {}'.format(nomfichier))
            candidats,L_population = self.lire_3D(nomfichier)
            self.liste_electeur = candidats
            self.L_population = L_population
            self.liste_to_liste3D()
            logging.info('</Map.chargement> nomfichier: {}'.format(nomfichier))

    def zone(self, ind, r):
        """
        Permet de creer une zone autour d'un individu ind de rayon r

        Parameters:
            ind (Individus): l'individu dont on va definir la zone
            r (int): rayon de la zone
        
        Returns:
            liste (list(Individus)): liste des individus presents dans la zone
        """
        liste = []
        for x in range(max(0, ind.x - r), min(self.generationX, ind.x + r + 1)):
            for y in range(max(0, ind.y - r), min(self.generationY, ind.y + r + 1)):
                for z in range(max(0, ind.z - r), min(self.generationZ, ind.z + r + 1))
                    print(ind.nom, self.population[x][y][z].nom)
                    if (((x != ind.x or y != ind.y or z != ind.z) and (self.population[x][y][z].poids >= 1)) and (ind.nom != self.population[x][y][z].nom)):
                        liste.append(self.population[x][y][z])
        return liste