from PySide6.QtWidgets import QApplication
from MWindow import MainWindow
from Back.Map import *
from Back.Candidat import *
from PySide6.QtGui import QColor
from Utilitaire import *
import sys

#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
#from codecarbon import track_emissions

from pyJoules.device import DeviceFactory
"""
from pyJoules.device.rapl_device import RaplPackageDomain, RaplDramDomain
from pyJoules.device.nvidia_device import NvidiaGPUDomain
"""
from pyJoules.energy_meter import EnergyMeter

#domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]s
#devices = DeviceFactory.create_devices(domains)

"""
devices = DeviceFactory.create_devices()
meter = EnergyMeter(devices)
"""
#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler

"""
trace = meter.get_trace()

#Début de la mesure
meter.start(tag="Début de la mesure")
"""

global bd

class Base_donnee():
    #meter.record(tag='Mesure BD : Constructeur')
    @measure_energy(handler=csv_handler)
    def __init__(self, id, window=None,tailleMap=500):
        """
        Constructeur de la classe Base_donnee.

        Args:
            id (int): Identifiant de la base de données.
            window (MainWindow): Fenêtre principale associée à la base de données. Par défaut, None.
            tailleMap (int): Taille de la carte. Par défaut, 500.
        """
        self.id = id
        self.map = Map(self, str(id), [], [], tailleMap, tailleMap)
        self.window = window
    
    #meter.stop()
    #trace += meter.get_trace()

    #meter.resume(tag='Mesure BD : Méthode refresh')
    @measure_energy(handler=csv_handler)
    def refresh(self,NormaliserCandidat):
        """
        Méthode pour rafraîchir la fenêtre principale avec des candidats normalisés.

        Args:
            NormaliserCandidat (list): Liste des candidats normalisés à afficher.
        """
        self.window.refresh(NormaliserCandidat)
    
    #meter.stop()
    #trace += meter.get_trace()

    #meter.resume(tag='Mesure BD : Méthode ajoute')
    @measure_energy(handler=csv_handler)
    def ajoute(self,new,newC):
        """
        Méthode pour ajouter un nouvel élément et un nouveau candidat à la base de données.

        Args:
            new: Nouvel élément à ajouter.
            newC: Nouveau candidat à ajouter.
        """
        bd.window.ajouteElement(new) 
        bd.map.ajoute_candidat(newC)
    
    #meter.stop()
    #trace += meter.get_trace()

    #meter.resume(tag='Mesure BD : Méthode genere_aleatoire_candidat_BM')
    @measure_energy(handler=csv_handler)
    def genere_aleatoire_candidat_BM(self): # genere aleatoirement un Candidat de la Classe Candidiat
        """
        Méthode pour générer aléatoirement un candidat de la classe Candidiat.

        Returns:
            Candidat: Nouveau candidat généré aléatoirement.
        """
        return Candidat.random_candidat(self.window.tailleMap,self.window.tailleMap)
    
    #meter.stop()
    #trace += meter.get_trace()

    #meter.resume(tag='Mesure BD : Méthode refresh_MV')
    @measure_energy(handler=csv_handler)
    def refresh_MV(self,l):
        """
        Méthode pour rafraîchir la liste de résultats.

        Args:
            l (list): Liste des résultats à afficher.
        """
        self.window.listePoint.refresh_MV(l)
    
    #meter.stop()
    #trace += meter.get_trace()

    #meter.resume(tag='Mesure BD : Méthode save')
    @measure_energy(handler=csv_handler)
    def save(self,fichier):
        """
        Méthode pour sauvegarder la carte dans un fichier.

        Args:
            fichier (str): Chemin du fichier de sauvegarde.
        """
        self.map.ecrire(fichier)
    
    #meter.stop()
    #trace += meter.get_trace()

    #meter.resume(tag='Mesure BD : Méthode recharge')
    @measure_energy(handler=csv_handler)
    def recharge(self,ficher):
        """
        Méthode pour recharger la carte à partir d'un fichier.

        Args:
            fichier (str): Chemin du fichier à charger.
        """
        self.map.chargement(ficher)
        liste = self.map.liste_electeur
        self.window.refresh(normalise_rechargement(liste))
    
    #meter.stop()
    #trace += meter.get_trace()
    
    #meter.resume(tag='Mesure BD : Méthode creer')
    @measure_energy(handler=csv_handler)
    @staticmethod
    def creer(id,tailleMap=500):
        """
        Méthode statique pour créer une nouvelle instance de Base_donnee.

        Args:
            id (int): Identifiant de la base de données.
            tailleMap (int): Taille de la carte. Par défaut, 500.

        Returns:
            Base_donnee: Nouvelle instance de Base_donnee créée.
        """
        
        global bd
        new = Base_donnee(id,tailleMap)
        bd = new
        # création de la map du Back
        new.map.generationAleatoire()
        # création de la window
        window = MainWindow(new, tailleMap*2)
        # affectation 
        new.window = window
        return new

"""
#Fin de la mesure
meter.stop()

#Affichage de la consommation énergétique
trace += meter.get_trace()
print(trace)

#Sauvegarde des données dans un fichier CSV
csv_handler.save_data()
"""

"""
# Créer une instance de QApplication

app = QApplication(sys.argv)

# Créer une instance de Base_donnee en utilisant la même instance de MainWindow
bd = Base_donnee.creer(123,250)
# Afficher la fenêtre principale
bd.window.show()
l=[("Monsieur Red", QColor(255, 0, 0),1,(25,25)), ("Monsieur Green", QColor(0, 255, 0),2,(150,150))]
#bd.refresh(l)
#bd.ajoute(("Monsieur", QColor(255, 255, 255),1,(250,250)))
# Exécuter la boucle principale de l'application
sys.exit(app.exec())
"""