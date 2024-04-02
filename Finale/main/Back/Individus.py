import numpy as np
from random import uniform


from Internet import internet
from Internet import iso_code


""" Pas de log pour les performences """
class Individus:
    def __init__(self, nom=None, x=None, y=None,liste_electeur=None):
        self.nom = nom
        self.x = x
        self.y = y
        self.map = map
        self.liste_electeur = liste_electeur
        self.poids = 1
        self.competence = uniform(0,10)
        self.adelegue = False

    #Getter pour obtenir le niveau de compétence de l'électeur
    def get_c(self):
        return self.c

    #Getter pour obtenir le poids du vote de l'électeur
    def get_poids(self):
        return self.poids
    
    def liste_vote(self):
        liste_des_votes = [(np.linalg.norm(np.array([i.x(), i.y()]) - np.array([self.x, self.y])), i) for i in self.liste_electeur]
        l=sorted(liste_des_votes, key=lambda x: x[0])
        return [ candidat for distance,candidat in l]