from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from MenuLateral import SideMenu
from ListeRes import ListePoint
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QColor
from MapQT import Compass


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler



class MainWindow(QMainWindow):
    @measure_energy(handler=csv_handler)
    def __init__(self,bd,tailleMap=500):
        """
        Constructeur de la classe MainWindow.

        Args:
            bd (object): Objet représentant une base de données.
            tailleMap (int): Taille de la carte. Par défaut, 500.
        """

        super().__init__()
        self.setWindowTitle("Main Window")
        self.bd=bd
        self.tailleMap = tailleMap
        #taille des boutons
        self.Blongeur = 300
        self.Bhauteur = 40
        
        self.listeResultat=[]
        # Créer les widgets
        self.compass = Compass(size=self.tailleMap, nb_lines=100)
        self.menu = SideMenu(self.bd,self.Blongeur,self.Bhauteur,self.tailleMap)
        self.listePoint = ListePoint(self.listeResultat)
        
        # Créer un widget central pour la fenêtre principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Créer un layout vertical principal pour organiser les sous-layouts horizontaux
        main_layout = QVBoxLayout(central_widget)
        
        # Créer un layout horizontal pour le menu latéral et la boussole
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.menu)
        top_layout.addWidget(self.compass, alignment=Qt.AlignTop | Qt.AlignRight)
        
        # Ajouter le layout horizontal supérieur au layout principal
        main_layout.addLayout(top_layout)
        
        # Ajouter un espace extensible pour pousser ListePoint vers la droite
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Ajouter ListePoint en bas à droite
        main_layout.addWidget(self.listePoint, alignment=Qt.AlignBottom | Qt.AlignRight)
        
        # Configurer la taille maximale de ListePoint
        self.listePoint.setMaximumWidth(500)
        
        # Configurer la géométrie de la fenêtre principale
        self.setGeometry(100, 100, 1200, 800)
    
    @measure_energy(handler=csv_handler)
    def SetBd(self, bd):
        """
        Méthode pour définir une nouvelle base de données.

        Args:
            bd (object): Objet représentant une base de données.
        """
        self.bd = bd
    
    @measure_energy(handler=csv_handler)
    def affiche_Map(self):
        """Méthode pour afficher la carte."""
        self.compass.show()
    
    @measure_energy(handler=csv_handler)
    def ajoutePoint_Map(self,element_normaliser):
        """
        Méthode pour ajouter un point sur la carte.

        Args:
            element_normaliser (tuple): Tuple représentant les informations d'un point normalisé.
        """
        _,color,_,(x,y) = element_normaliser
        self.compass.placePoint(x,y,color)
    
    @measure_energy(handler=csv_handler)
    def ajouterPoint_Liste(self,element_normaliser):
        """
        Méthode pour ajouter un point à la liste.

        Args:
            element_normaliser (tuple): Tuple représentant les informations d'un point normalisé.
        """
        nom,color,score,pos = element_normaliser
        self.listePoint.ajouter_element(nom,color,score,pos)

    @measure_energy(handler=csv_handler)  
    def afficheListe(self):
        """Méthode pour afficher la liste."""
        # Effacer tous les anciens points affichés sur la boussole
        self.compass.clearPoints()
        
        # Ajouter les nouveaux points de la liste
        for point in self.listePoint.points:
            _, color, _, (x, y) = point
            self.ajoutePoint(x, y, color)   
    
    @measure_energy(handler=csv_handler)
    def refresh(self,new):
        """
        Méthode pour actualiser la fenêtre principale avec de nouveaux points.

        Args:
            new (list): Liste des nouveaux points à afficher.
        """
        self.compass.refresh_Map(new)
        self.listePoint.refresh_ListPoint(new)
    
    @measure_energy(handler=csv_handler)
    def ajouteElement(self,element_normaliser):
        """
        Méthode pour ajouter un élément à la liste et à la carte.

        Args:
            element_normaliser (tuple): Tuple représentant les informations d'un point normalisé.
        """
        self.listeResultat.append(element_normaliser)
        self.ajoutePoint_Map(element_normaliser)
        self.ajouterPoint_Liste(element_normaliser)
    
    @measure_energy(handler=csv_handler)
    def refresh_Liste(self,l):
        """
        Méthode pour actualiser la liste de résultats.

        Args:
            l (list): Liste des résultats à afficher.
        """
        self.listePoint.refresh_MV(l)             

@measure_energy(handler=csv_handler)                  
def test_refresh_MainWindow():
    """
    Fonction de test pour vérifier le rafraîchissement de la MainWindow.
    """
    # Créer une application Qt
    app = QApplication([])

    # Créer une instance de la classe MainWindow
    window = MainWindow()

    # Afficher la fenêtre principale
    window.show()
    window.affiche_Map()

    # Attendre 2 secondes avant de rafraîchir la liste de points avec de nouveaux points
    QTimer.singleShot(2000, lambda: window.refresh([
        ("Monsieur Yellow", QColor(255, 255, 0), 6, (50, 50)),
        ("Monsieur Orange", QColor(255, 165, 0), 7, (100, 100)),
        ("Monsieur Purple", QColor(128, 0, 128), 8, (150, 150))
    ]))

    # Attendre 3 secondes avant d'ajouter un nouveau point
    QTimer.singleShot(3000, lambda: window.ajouteElement("Monsieur low", QColor(0, 255, 0), 6, (150, 50)))

    # Attendre 6 secondes avant de quitter
    QTimer.singleShot(6000, app.quit)

    # Exécuter l'application
    app.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.affiche_Map()
    window.refresh([
        ("Monsieur Yellow", QColor(255, 255, 0), 6, (50, 50)),
        ("Monsieur Orange", QColor(255, 165, 0), 7, (100, 100)),
        ("Monsieur Purple", QColor(128, 0, 128), 8, (150, 150))
    ])
    window.ajouteElement(("Monsieur low", QColor(0, 255, 0), 6, (150, 50)))
    app.exec()