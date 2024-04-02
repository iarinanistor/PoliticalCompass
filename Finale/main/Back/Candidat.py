import random
import logging
#pour ameliorer les performence ne pas activer le log ici

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from Internet import internet
from Internet import iso_code


class Candidat:
    compteur = 0
    liste_nom=['Martin','Bernard','Petit','Laurent','Dupont','LeGall','Henry','Duval','Jouve','Baron']
    liste_prenom=['Louis','Gabriel','Arthur','Emma','Rose','Marceau','Tom','Iris','Chloe','Theo']

    def __init__(self,nom,prenom,charisme,age,x,y):
        """
        Constructeur de la classe Candidat.

        Args:
            nom (str): Nom du candidat.
            prenom (str): Prénom du candidat.
            charisme (int): Valeur du charisme du candidat.
            age (int): Âge du candidat.
            x (float): Coordonnée x du candidat.
            y (float): Coordonnée y du candidat.
        """
        logging.info('<Candidat.__init__> nom: {}, prenom: {}, charisme: {}, age: {}, x: {}, y: {}'.format(nom, prenom, charisme, age, x, y))

        self._nom = nom
        self._prenom = prenom
        self._charisme = charisme
        self._age = age
        self._x = x
        self._y = y
        Candidat.compteur += 1
        self.id = Candidat.compteur

    def __hash__(self):
        return hash(self.id)

    def nom(self):
        """
        Renvoie le nom du candidat.

        Returns:
            str: Le nom du candidat.
        """
        return self._nom

    def prenom(self):
        """
        Renvoie le prénom du candidat.

        Returns:
            str: Le prénom du candidat.
        """
        return self._prenom

    def age(self):
        """
        Renvoie l'âge du candidat.

        Returns:
            int: L'âge du candidat.
        """
        return self._age

    def charisme(self):
        """
        Renvoie la valeur du charisme du candidat.

        Returns:
            int: La valeur du charisme du candidat.
        """
        return self._charisme
    
    def x(self):
        """
        Renvoie la coordonnée x du candidat.

        Returns:
            float: La coordonnée x du candidat.
        """
        return self._x
    
    def y(self):
        """
        Renvoie la coordonnée y du candidat.

        Returns:
            float: La coordonnée y du candidat.
        """
        return self._y
    
    @staticmethod
    def random_candidat(x, y):
        """
        Crée un candidat aléatoire avec des coordonnées x et y données.

        Args:
            x (float): La coordonnée x.
            y (float): La coordonnée y.

        Returns:
            Candidat: Le candidat créé.
        """
        #logging.info('<Candidat.random_candidat> x: {}, y: {}'.format(x, y))

        return Candidat(
            random.choice(Candidat.liste_nom),
            random.choice(Candidat.liste_prenom),
            random.randint(1, 100),
            random.randint(18, 85),
            random.random() * x,
            random.random() * y
        )
    
    @staticmethod
    def genere_candidat(x, y):
        """
        Crée un candidat avec des coordonnées x et y données.

        Args:
            x (float): La coordonnée x.
            y (float): La coordonnée y.

        Returns:
            Candidat: Le candidat créé.
        """
        #logging.info('<Candidat.genere_candidat> x: {}, y: {}'.format(x, y))

        return Candidat(
            random.choice(Candidat.liste_nom),
            random.choice(Candidat.liste_prenom),
            random.randint(1, 100),
            random.randint(18, 85),
            x,
            y
        )
    
    @staticmethod
    def generate_candidats(n, x, y):
        """
        Génère une liste de candidats aléatoires avec des coordonnées x et y données.

        Args:
            n (int): Le nombre de candidats à générer.
            x (float): La coordonnée x.
            y (float): La coordonnée y.

        Returns:
            list: Liste des candidats générés.
        """
        #logging.info('<Candidat.generate_candidats> n: {}, x: {}, y: {}'.format(n, x, y)) 
        return [Candidat.random_candidat(x, y) for _ in range(n)]

    @staticmethod
    def affiche_candidat(candidat):
        '''
        Affiche les informations d'un candidat.

        Args:
            candidat (Candidat): Le candidat à afficher.
        '''
        #logging.info('<Candidat.affiche_candidat> candidat: {}'.format(candidat))

        print(candidat.nom() + " " + candidat.prenom() + " age:" + str(candidat.age()) + " charisme:" + str(candidat.charisme()))
