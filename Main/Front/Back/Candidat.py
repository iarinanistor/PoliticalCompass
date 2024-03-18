import random


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler



class Candidat:
    compteur = 0
    liste_nom=['Martin','Bernard','Petit','Laurent','Dupont','LeGall','Henry','Duval','Jouve','Baron']
    liste_prenom=['Louis','Gabriel','Arthur','Emma','Rose','Marceau','Tom','Iris','Chloe','Theo']

    @measure_energy(handler=csv_handler)
    def __init__(self,nom,prenom,charisme,age,x,y):
        self._nom = nom
        self._prenom = prenom
        self._charisme = charisme
        self._age = age
        self._x = x
        self._y = y
        Candidat.compteur+=1
        self.id = Candidat.compteur

    @measure_energy(handler=csv_handler)
    def __hash__(self):
        return hash(self.id)

    @measure_energy(handler=csv_handler)
    def nom(self):
        return self._nom

    @measure_energy(handler=csv_handler)
    def prenom(self):
        return self._prenom

    @measure_energy(handler=csv_handler)
    def age(self):
        return self._age

    @measure_energy(handler=csv_handler)
    def charisme(self):
        return self._charisme
    
    @measure_energy(handler=csv_handler)
    def x(self):
        return self._x
    
    @measure_energy(handler=csv_handler)
    def y(self):
        return self._y
    
    @measure_energy(handler=csv_handler)
    def random_candidat(x,y):
        return Candidat( random.choice(Candidat.liste_nom),
                    random.choice(Candidat.liste_prenom),
                    random.randint(1,100),
                    random.randint(18,85),
                    random.random()*x,
                    random.random()*y
                    )
    
    @measure_energy(handler=csv_handler)
    def generate_candidats(n,x,y):
        l=[]
        for i in range(n):
            l.append(Candidat.random_candidat(x,y))
        return l

    #Methode qui affiche un candidat
    @measure_energy(handler=csv_handler)
    def affiche_candidat(candidat):
        '''
        Parameters:
            candidat : Candidat
        Returns:
            void : l'affichage d'un candidat
        '''
        return print(candidat.nom()+" "+candidat.prenom()+" age:"+str(candidat.age())+" charisme:"+str(candidat.charisme()))
