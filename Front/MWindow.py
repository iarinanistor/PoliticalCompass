from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from MenuLateral import SideMenu
from ListeRes import ListePoint
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QColor
from MapQT import Compass


class MainWindow(QMainWindow):
    def __init__(self,bd,tailleMap=500):
        """
        Constructeur de la classe SideMenu.

        Args:
            bd (object): Objet représentant une base de données.
            Blongeur (int): Longueur des boutons. Par défaut, 300.
            Bhauteur (int): Hauteur des boutons. Par défaut, 40.
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
    
    def SetBd(self, bd):
        self.bd = bd
        
    def affiche_Map(self):
        self.compass.show()
    
    def ajoutePoint_Map(self,element_normaliser):
        _,color,_,(x,y) = element_normaliser
        self.compass.placePoint(x,y,color)
    
    def ajouterPoint_Liste(self,element_normaliser):
        nom,color,score,pos = element_normaliser
        self.listePoint.ajouter_element(nom,color,score,pos)
        
    def afficheListe(self):
        # Effacer tous les anciens points affichés sur la boussole
        self.compass.clearPoints()
        
        # Ajouter les nouveaux points de la liste
        for point in self.listePoint.points:
            _, color, _, (x, y) = point
            self.ajoutePoint(x, y, color)   
         
    def refresh(self,new):
        self.compass.refresh_Map(new)
        self.listePoint.refresh_ListPoint(new)
    
    def ajouteElement(self,element_normaliser):
        self.listeResultat.append(element_normaliser)
        self.ajoutePoint_Map(element_normaliser)
        self.ajouterPoint_Liste(element_normaliser)
    
    def refresh_Liste(self,l):
        
        self.listePoint.refresh_MV(l)             
                           
def test_refresh_MainWindow():
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