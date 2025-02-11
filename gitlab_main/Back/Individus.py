import numpy as np
from random import uniform
from icecream import ic 
from Back.votes import F
class Individus:
    def __init__(self, nom=None, x=None, y=None, liste_electeur=None):
        self.nom = [nom]
        self.x = x
        self.y = y
        self.liste_electeur = liste_electeur
        self.poids = [1]
        self.c = [uniform(0, 1)]
        self.adelegue = [False]

    # Getter pour obtenir le niveau de compétence de l'électeur
    def get_c(self):
        return self.c

    """def liste_vote(self):
        '''
        Retourne une liste des électeurs classés par leur proximité par rapport au candidat courant.

        Returns:
        list: Liste des électeurs classés.
        '''
        try:
            liste_des_votes = [(np.linalg.norm(np.array([i.x(), i.y()]) - np.array([self.x, self.y])), i) for i in self.liste_electeur]
            sorted_votes = sorted(liste_des_votes, key=lambda x: x[0])
            return [candidat for distance, candidat in sorted_votes]
        except TypeError:
            ic(self.liste_electeur)"""

    def liste_vote(self):
        """
        Retourne une liste des électeurs classés par leur proximité et charisme par rapport au candidat courant.

        Returns:
            list: Liste des électeurs classés.
        """
        try:
            liste_des_votes = [(F(self.x, self.y , i.x(),i.y(), i.charisme()), i) for i in self.liste_electeur]
            sorted_votes = sorted(liste_des_votes, key=lambda x: x[0])
            return [candidat for distance, candidat in sorted_votes]
        except TypeError:
            ic(self.liste_electeur)