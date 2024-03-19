import numpy as np
""" Pas de log pour les performences """
class Individus:
    def __init__(self, nom=None, x=None, y=None,liste_electeur=None):
        self.nom = nom
        self.x = x
        self.y = y
        self.map = map
        self.liste_electeur = liste_electeur
        
    def liste_vote(self):
        liste_des_votes = [(np.linalg.norm(np.array([i.x(), i.y()]) - np.array([self.x, self.y])), i) for i in self.liste_electeur]
        l=sorted(liste_des_votes, key=lambda x: x[0])
        return [ candidat for distance,candidat in l]