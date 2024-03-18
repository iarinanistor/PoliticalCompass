import numpy as np


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler



class Individus:
    @measure_energy(handler=csv_handler)
    def __init__(self, nom=None, x=None, y=None,liste_electeur=None):
        self.nom = nom
        self.x = x
        self.y = y
        self.map = map
        self.liste_electeur = liste_electeur
    
    @measure_energy(handler=csv_handler)
    def liste_vote(self):
        liste_des_votes = [(np.linalg.norm(np.array([i.x(), i.y()]) - np.array([self.x, self.y])), i) for i in self.liste_electeur]
        l=sorted(liste_des_votes, key=lambda x: x[0])
        return [ candidat for distance,candidat in l]