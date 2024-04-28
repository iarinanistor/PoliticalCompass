import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem, QFrame
from Front.Widgets.MenuLateral import SideMenu
from PySide6.QtCore import Qt, QTimer, QSize, QRect
from PySide6.QtGui import QColor
from Front.Widgets.MapQT import Compass
from Front.Planete.Planete import Planete
from Front.Widgets.Resultat import ListeResultat
from Front.Utilitaire import generate_unique_colors
import logging
from icecream import ic
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application, gérant l'affichage et les interactions avec les données de navigation et de visualisation.

    Attributs:
        bd (object): Instance de la base de données utilisée pour les opérations de données.
        tailleMap (int): Taille de la carte pour les visualisations.
        Pl (bool): Booléen pour déterminer si une représentation spéciale 'Planète' doit être utilisée.
        compass (Compass or Planete): Widget pour la visualisation de la carte.
        menu (SideMenu): Menu latéral pour les interactions supplémentaires.
        liste_resultats (ListeResultat): Widget pour afficher les résultats des calculs ou analyses.
        liste_des_resultats (list): Stockage des résultats des calculs pour utilisation dans l'interface.

    Méthodes:
        __init__: Initialise la fenêtre principale avec tous les widgets et layouts nécessaires.
        SetBd: Définit ou met à jour la base de données utilisée.
        affiche_Map: Commande l'affichage de la carte.
        ajoute_point_map: Ajoute un point sur la carte basée sur les données d'un candidat.
        ajouter_resultat: Ajoute un résultat à la liste des résultats.
        afficheListe: Gère l'affichage de la liste des points ou résultats.
        refresh: Rafraîchit les données affichées dans l'ensemble de l'interface.
        ajoute_element: Ajoute un élément à la fois à la liste et à la carte.
    """
    
    def __init__(self, bd, tailleMap=500, Pl=False):
        """
        Initialise la fenêtre principale avec des configurations spécifiques pour la base de données et la taille de la carte.
        """
        super().__init__()
        self.setWindowTitle("Sirius - Application de vote")
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
            self.compass = Compass(size=(500), nb_lines=100)

        self.menu = SideMenu(self.bd, self.Blongeur, self.Bhauteur, self.tailleMap)
        self.liste_resultats = ListeResultat(self.liste_des_resultats,self.bd)

        # Créer un widget central pour la fenêtre principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #333333;")

        # Créer un layout vertical principal pour organiser les sous-layouts horizontaux
        main_layout = QVBoxLayout(central_widget)

        # Ajouter un espace extensible pour pousser liste_resulat vers la droite
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Layout pour les autres composants
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.menu)
        content_layout.addWidget(self.compass, alignment=Qt.AlignTop | Qt.AlignRight)
        main_layout.addLayout(content_layout)

        # Ajouter les résultats et la configuration des boutons
        main_layout.addWidget(self.liste_resultats, alignment=Qt.AlignBottom | Qt.AlignRight)
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
        
        x = candidat.x()*5 # car la taille de la map fait 500x500 on re-adapte la taille
        y = candidat.y()*5 
        
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