import random

class Candidat:
    compteur = 0  # Compteur de candidats, utilisé pour attribuer un identifiant unique à chaque candidat
    liste_nom=['Martin','Bernard','Petit','Laurent','Dupont','LeGall','Henry','Duval','Jouve','Baron']  # Liste des noms possibles
    liste_prenom=['Louis','Gabriel','Arthur','Emma','Rose','Marceau','Tom','Iris','Chloe','Theo']  # Liste des prénoms possibles
    
    def __init__(self, nom, prenom, charisme, age, x, y):
        '''
        Initialise un objet Candidat avec les attributs spécifiés.
        
        Parameters:
            nom (str): Nom du candidat.
            prenom (str): Prénom du candidat.
            charisme (int): Niveau de charisme du candidat.
            age (int): Âge du candidat.
            x (float): Position x du candidat.
            y (float): Position y du candidat.
        '''
        self._nom = nom
        self._prenom = prenom
        self._charisme = charisme
        self._age = age
        self._x = x
        self._y = y
        Candidat.compteur += 1  # Incrémente le compteur de candidats à chaque création d'un nouveau candidat
        self.id = Candidat.compteur  # Attribue un identifiant unique à chaque candidat
    
    def __hash__(self):
        '''
        Surcharge de la méthode de hachage pour les objets Candidat.
        '''
        return hash(self.id)

    def nom(self):
        '''
        Renvoie le nom du candidat.
        '''
        return self._nom

    def prenom(self):
        '''
        Renvoie le prénom du candidat.
        '''
        return self._prenom

    def age(self):
        '''
        Renvoie l'âge du candidat.
        '''
        return self._age

    def charisme(self):
        '''
        Renvoie le niveau de charisme du candidat.
        '''
        return self._charisme
    
    def x(self):
        '''
        Renvoie la position x du candidat.
        '''
        return self._x
    
    def y(self):
        '''
        Renvoie la position y du candidat.
        '''
        return self._y
    
    @staticmethod
    def random_candidat(x, y):
        '''
        Génère un candidat aléatoire avec un nom, un prénom, un charisme, un âge et des coordonnées aléatoires.
        
        Parameters:
            x (float): Limite supérieure pour la position x.
            y (float): Limite supérieure pour la position y.
        
        Returns:
            Candidat: Un objet Candidat avec des attributs aléatoires.
        '''
        return Candidat(
            random.choice(Candidat.liste_nom),
            random.choice(Candidat.liste_prenom),
            random.randint(1, 100),
            random.randint(18, 85),
            random.random() * x,
            random.random() * y
        )
    
    @staticmethod
    def generate_candidats(n, x, y):
        '''
        Génère une liste de candidats aléatoires.
        
        Parameters:
            n (int): Nombre de candidats à générer.
            x (float): Limite supérieure pour la position x.
            y (float): Limite supérieure pour la position y.
        
        Returns:
            list: Liste d'objets Candidat avec des attributs aléatoires.
        '''
        candidats = []
        for _ in range(n):
            candidats.append(Candidat.random_candidat(x, y))
        return candidats

    @staticmethod
    def affiche_candidat(candidat):
        '''
        Affiche les informations d'un candidat.
        
        Parameters:
            candidat (Candidat): L'objet Candidat à afficher.
        '''
        print(f"{candidat.nom()} {candidat.prenom()} - Âge: {candidat.age()}, Charisme: {candidat.charisme()}") 

