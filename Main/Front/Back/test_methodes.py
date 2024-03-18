from Map import Map
from Candidat import Candidat
from Individus import Individus
from votes import *


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler



#Methode qui affiche un candidat
@measure_energy(handler=csv_handler)
def affiche_candidat(candidat):
    '''
    Parameters:
        candidat : Candidat
    Returns:
        void : l'affichage d'un candidat
    '''
    print(candidat.nom()+" "+candidat.prenom()+" age:"+str(candidat.age())+" charisme:"+str(candidat.charisme()))

#Test des differentes methodes de vote

#Les candidats
candidat1 = ('Martin','Louis',3,42,3,4)
candidat2 =Candidat('Petit','Arthur',2.8,40,4,7)
candidat3 = Candidat('Laurent','Marie',3.2,48,1,3)
candidat4 = Candidat('Duval','Gabriel',3.2,52,3,0)

#Liste des Candidats
l_cand=[candidat1,candidat2,candidat3,candidat4]

#Liste des electeurs
l_electeur=[Individus("victor",-10,10,l_cand),  Individus("Isaac",0,0,l_cand),Individus("Lyna",-5,-25,l_cand),Individus("chaby",-30,-30,l_cand)]

#Test d'un vote a la Pluralité et affichage du vainqueur
gagnantP = pluralite(l_cand,l_electeur)
print("Pluralite : ") 
affiche_candidat(gagnantP)
print()

#Test de la methode Borda et affichage du vainqueur
gagnantB = borda(l_cand,l_electeur)
print("Borda : ") 
affiche_candidat(gagnantB)
print()

#Test de la methode STV et affichage du vainqueur
gagnantS = stv(l_cand,l_electeur)
print("STV :")
affiche_candidat(gagnantS)
print()

#Test de la methode d'approbation et affichage du vainqueur
gagnantA = approbation(l_cand,l_electeur,2)
print("Approbation :")
affiche_candidat(gagnantA)
print()