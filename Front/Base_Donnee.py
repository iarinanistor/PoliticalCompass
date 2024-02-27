from PySide6.QtWidgets import QApplication
from MWindow import MainWindow
from Back.Map import *
from Back.Candidat import *
from PySide6.QtGui import QColor
from Utilitaire import *
import sys

class Base_donnee():
    def __init__(self, id, window=None,tailleMap=500):
        self.id = id
        self.map = Map(self, str(id), [], [], tailleMap, tailleMap)
        self.window = window
    
    def refresh(self,NormaliserCandidat):
            self.window.refresh(NormaliserCandidat)
    
    def ajoute(self,new,newC):
        bd.window.ajouteElement(new) 
        bd.map.ajoute_candidat(newC)
    
    def genere_aleatoire_candidat_BM(self): # genere aleatoirement un Candidat de la Classe Candidiat
        return Candidat.random_candidat(self.window.tailleMap,self.window.tailleMap)
    
    def refresh_MV(self,l):
        self.window.listePoint.refresh_MV(l)
        
    def save(self,fichier):
        self.map.ecrire(fichier)
    
    def recharge(self,ficher):
        self.map.chargement(ficher)
        liste = self.map.liste_electeur
        self.window.refresh(normalise_rechargement(liste))
        
    @staticmethod
    def creer(id,tailleMap=500):
        new = Base_donnee(id,tailleMap)
        # création de la map du Back
        new.map.generationAleatoire()
        # création de la window
        window = MainWindow(new, tailleMap*2)
        # affectation 
        new.window = window
        return new

    
    
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
