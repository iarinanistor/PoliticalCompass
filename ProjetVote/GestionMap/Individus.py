import numpy as np

class Individus:
    def __init__(self, nom=None, x=None, y=None, liste_electeur=None):
        '''
        Initialise un objet Individus avec les attributs spécifiés.
        
        Parameters:
            nom (str): Nom de l'individu.
            x (float): Position x de l'individu.
            y (float): Position y de l'individu.
            liste_electeur (list): Liste des électeurs.
        '''
        self.nom = nom  # Nom de l'individu
        self.x = x  # Position x de l'individu
        self.y = y  # Position y de l'individu
        self.liste_electeur = liste_electeur  # Liste des électeurs

    def liste_vote(self):
        '''
        Classe les électeurs en fonction de leur proximité avec cet individu.
        
        Returns:
            list: Liste des électeurs triés par proximité.
        '''
        # Calcul des distances entre cet individu et chaque électeur dans la liste
        liste_des_votes = [(np.linalg.norm(np.array([i.x(), i.y()]) - np.array([self.x, self.y])), i) for i in self.liste_electeur]
        
        # Tri de la liste des votes en fonction de la distance
        sorted_votes = sorted(liste_des_votes, key=lambda x: x[0])
        
        # Renvoie de la liste des candidats dans l'ordre de proximité croissante
        return [candidat for distance, candidat in sorted_votes]
