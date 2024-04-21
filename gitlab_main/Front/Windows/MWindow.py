import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem, QFrame
from Front.Widgets.MenuLateral import SideMenu
from PySide6.QtCore import Qt, QTimer, QSize, QRect
from PySide6.QtGui import QColor
from Front.Widgets.MapQT import Compass
from Front.Planete.Planete import Planete
from Front.Widgets.Resultat import ListeResultat
from Front.Utilitaire import generate_unique_colors
from resources_rc import *
import logging
from icecream import ic
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    def __init__(self, bd, tailleMap=500, Pl=False):
        """
        Constructeur de la classe MainWindow.

        Args:
            bd (object): Objet représentant une base de données.
            tailleMap (int): Taille de la carte. Par défaut, 500.
            Pl (bool): Indique si la planète est utilisée. Par défaut, False.
        """

        super().__init__()
        self.setWindowTitle("Main Window")
        self.bd = bd
        ic(self.bd,"Main Window")
        self.tailleMap = tailleMap
        # Taille des boutons
        self.Blongeur = 300
        self.Bhauteur = 40
        self.Planete = Pl
        self.liste_des_resultats = [] # liste de couples ( candidat , score)
        

        # Créer les widgets
        if Pl:
            self.compass = Planete()
            self.compass.setFixedSize(500,500)
        else:
            self.compass = Compass(size=self.tailleMap, nb_lines=100)

        self.menu = SideMenu(self.bd, self.Blongeur, self.Bhauteur, self.tailleMap)
        self.liste_resultats = ListeResultat(self.liste_des_resultats)

        # Créer un widget central pour la fenêtre principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Créer un layout vertical principal pour organiser les sous-layouts horizontaux
        main_layout = QVBoxLayout(central_widget)

        # Créer un layout horizontal pour le menu latéral et la boussole
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.menu)
        top_layout.addWidget(self.compass, alignment=Qt.AlignTop | Qt.AlignRight)

        self.leftMenuBg = QFrame(central_widget) 
        self.leftMenuBg.setObjectName("leftMenuBg") 
        self.leftMenuBg.setStyleSheet("""
            #leftMenuBg {
                background-color: rgb(33, 37, 43);
            }
        """)
        self.leftMenuBg.setMinimumSize(QSize(63, 48))
        self.leftMenuBg.setMaximumSize(QSize(63, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        
        # Création d'un sous-layout pour leftMenuBg
        leftMenu_layout = QVBoxLayout(self.leftMenuBg)
        leftMenu_layout.setSpacing(0)
        leftMenu_layout.setContentsMargins(0, 0, 0, 0)
        
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName("topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(25, 63))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 63))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName("topLogo")
        self.topLogo.setStyleSheet("""
            #topLogo {
                background-color: rgb(33, 37, 43);
                background-image: url(:/images/images/images/logo.png);
                background-position: centered;
                background-repeat: no-repeat;
            }
        """)
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))  # Réduire la taille du logo
        self.topLogo.setMinimumSize(QSize(42, 42))  # Définir une taille minimale pour le logo
        self.topLogo.setMaximumSize(QSize(42, 42))  # Définir une taille maximale pour le logo
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
    
        leftMenu_layout.addWidget(self.topLogoInfo)

        # Ajouter le layout horizontal supérieur au layout principal
        main_layout.addLayout(top_layout)

        # Ajouter un espace extensible pour pousser liste_resulat vers la droite
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Ajouter liste_resultat en bas à droite
        main_layout.addWidget(self.liste_resultats, alignment=Qt.AlignBottom | Qt.AlignRight)
        # Configurer la taille maximale de liste_resulat
        self.liste_resultats.setMaximumWidth(500)

        # Configurer la géométrie de la fenêtre principale
        self.setGeometry(100, 100, 1250, 900)

    def SetBd(self, bd):
        """
        Méthode pour définir une nouvelle base de données.

        Args:
            bd (object): Objet représentant une base de données.
        """
        logging.info('<MainWindow.SetBd> bd: {}'.format(bd))
        self.bd = bd

    def affiche_Map(self):
        """Méthode pour afficher la carte."""
        logging.info('<MainWindow.affiche_Map>')

        self.compass.show()


    def ajoute_point_map(self, candidat):
        """
        Méthode pour ajouter un point sur la carte.

        Args:
            element_normaliser (tuple): Tuple représentant les informations d'un point normalisé.
        """
        logging.info('<MainWindow.ajoutePoint_Map> element_normaliser: {}'.format(candidat))
        
        x = candidat.x() 
        y = candidat.y()
        
        if self.Planete:
            self.compass.add_sphere(x,y, generate_unique_colors(x,y))
        else:
            self.compass.placePoint(x,y, generate_unique_colors(x,y))

    
    def ajouter_resultat(self,candidat):
        """
        Méthode pour ajouter un cand à listeResulatat.

        Args:
            candidat (Candidat): Candidat a ajouter dans listeResultat
        """
        self.liste_resultats.ajouter_element(candidat,0)

    def afficheListe(self):
        """Méthode pour afficher la liste."""
        logging.info('<MainWindow.afficheListe>')

        # Effacer tous les anciens points affichés sur la boussole
        if self.Planete:
            self.compass.clear_spheres()
        else:
            self.compass.clearPoints()

        # Ajouter les nouveaux points de la liste
        for point in self.listePoint.points:
            _, color, _, (x, y) = point
            self.ajoutePoint(x, y, color)

    def refresh(self, new):
        """
        Méthode pour actualiser la fenêtre principale avec de nouveaux points.
        Utiliser dans base donnee (self.recharge).
        Args:
            new (list): Liste des nouveaux candidat à afficher.
        """
        logging.info('<MainWindow.refresh> new: {}'.format(new))

        self.compass.refresh_Map(new)
        self.liste_resultats.refresh_list_resultat(new)

    def ajoute_element(self,candidat):
        """
        Méthode pour ajouter un élément à la liste et à la carte.

        Args:
            element_normaliser (tuple): Tuple représentant les informations d'un point normalisé.
        """
        logging.info('<MainWindow.ajouteElement> element_normaliser: {}'.format(candidat))

        self.liste_des_resultats.append((candidat,0))
        self.ajoute_point_map(candidat)
        self.ajouter_resultat(candidat)

     # je ne sais pas elle sert a quoi , je la met de coter on sait jamais 
    """
        def refresh_Liste(self, l): 
        "
        Méthode pour actualiser la liste de résultats.
        "
        Args:
            l (list): Liste des résultats à afficher.
        logging.info('<MainWindow.refresh_Liste> l: {}'.format(l))

                self.listePoint.refresh_MV(l)
    """
                           
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
    QTimer.singleShot(3000, lambda: window.ajoute_element("Monsieur low", QColor(0, 255, 0), 6, (150, 50)))

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
    window.ajoute_element(("Monsieur low", QColor(0, 255, 0), 6, (150, 50)))
    app.exec()