from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QLabel,QVBoxLayout
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import QTimer, Qt
import logging

from icecream import ic
from Back.Candidat import Candidat
from Front.Utilitaire import generate_unique_colors
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class BarreScore(QWidget):
    """
    Représente un widget affichant les informations d'un candidat et son score.
    
    Ce widget inclut une couleur unique générée pour le candidat, son nom, son score,
    et une image symbolique si le score atteint un certain critère (par exemple, le score est 1).
    
    Args:
        cand (Candidat): L'instance du candidat à afficher.
        score (int): Le score du candidat.
    """   
    def __init__(self, cand, score):
        super().__init__()
        if not isinstance(cand, Candidat):
            ic(cand)
            raise Exception('Barre Score: cand is not a Candidat')
        
        layout = QHBoxLayout()
        self.cand = cand
        self.score = score
        
        # Image
        self.image_label = QLabel()
        pixmap = QPixmap('Front/Widgets/Texture/trophee.png')  # Remplacer par le chemin de votre image
        self.image_label.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))  # Ajuster la taille selon les besoins
        
        self.color_label = QLabel()  
        self.color_label.setFixedSize(20, 20)
        self.set_color(generate_unique_colors(self.cand.x(), self.cand.y()))
        
        self.name_label = QLabel(self.cand.prenom() + " " + self.cand.nom())
        self.value_label = QLabel(str(score))
        self.taux_satisfaction = QLabel("-1")
        
        layout.addWidget(self.color_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.taux_satisfaction)
        if self.score == 1: layout.addWidget(self.image_label)  # Ajouter le QLabel de l'image au layout seulemnt si le cand est vainqueur donc score == 1
                  
        layout.addStretch(1)
        self.setLayout(layout)
    
    def set_color(self, color):
        """
        Applique une couleur de fond au label représentant la couleur du candidat.
        
        Args:
            color (QColor): La couleur à appliquer.
        """
        style_sheet = "background-color: {}".format(color.name())
        self.color_label.setStyleSheet(style_sheet)

class ListeResultat(QListWidget):
    """
    Affiche les scores et le coefficient de satisfaction des candidats.
    
    Permet l'affichage et la mise à jour des informations relatives aux candidats dans une liste.
    Prend en paramètre une liste de candidats et leur score respectif pour l'affichage.
    
    Args:
        liste_points (list): Liste de tuples (Candidat, score) pour l'initialisation.
    """
    
    def __init__(self,liste_points):
        super().__init__()
        self.l_points =liste_points # liste de (Candidats,score)
        self.setStyleSheet("""
    QListWidget {
        background-color: #777777;   /* Lighter grey background for the whole list */
        color: white;                /* White text color for better contrast */
        font-size: 14px;             /* Readable text size */
        font-family: 'Segoe UI', sans-serif;  /* Modern and clean font */
        border: none;                /* No border for a cleaner look */
    }
    QListWidgetItem {
        background-color: #999999;   /* Even lighter grey for item background */
        border-bottom: 1px solid #AAAAAA; /* Lighter grey for subtle separation */
        padding: 8px;                /* Sufficient padding for better text alignment */
        transition: background-color 0.2s, color 0.2s; /* Smooth transition for hover and selection */
    }
    QListWidgetItem:hover {
        background-color: #888888;  /* Slightly darker grey on hover for visual feedback */
    }
    QListWidgetItem:selected {
        background-color: #666666;  /* Darker grey for contrast on selection */
        color: #FFD700;             /* Gold color text when selected */
        border-left: 5px solid #FFD700; /* Gold left border for a clear selection indicator */
    }
    QLabel {
        background-color: transparent;  /* Fond transparent pour les labels */
    }
""")
        self.insertItem(0, " Color,  Nom Prenom, Rang, Taux Satisfaction") # insere en en-tete la description
    
    def populate_list (self):
        """
        Peuple la liste avec les informations des candidats fournies à l'initialisation.
        """
        if self.l_points is not None and self.l_points != []:
            for cand,score in self.l_points:
                barre_score = BarreScore(cand,score)
                item = QListWidgetItem(self)
                item.setSizeHint(barre_score.sizeHint())
                self.addItem(item)
                self.setItemWidget(item,barre_score)

    def ajouter_element(self,cand,score):
        """
        Ajoute un nouvel élément à la liste.
        
        Ajoute un candidat et son score à la liste d'affichage, en créant un nouveau widget `BarreScore`.
        
        Args:
            cand (Candidat): Le candidat à ajouter.
            score (int): Le score du candidat.
        """
        logging.info("<Ajout d'element>")
        logging.info('              Element ajoute - Candidat: {},Score: {}.'.format(cand, score))
        self.l_points.append((cand,score))
        item = QListWidgetItem(self)
        barre_score = BarreScore(cand,score)
        item.setSizeHint(barre_score.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, barre_score)
        logging.info("<Fin Ajout d'element>")
    
    def clean(self):
        """
        Nettoie la liste, en retirant tous les éléments sauf l'en-tête.
        
        Utilisée avant de rafraîchir la liste avec de nouveaux candidats ou après mise à jour.
        """
        # Ne pas effacer la première ligne
        logging.info("<Nettoyage")
        for i in range(1, self.count()):
            self.takeItem(1) # garde la permeiere ligne
        logging.info('              Liste rafraichie avec les nouveaux points.')
        self.l_points.clear()
        logging.info("<Fin rafraichissement de liste>")
    
    def refresh_list_resultat(self, new):
        """
        Rafraîchit la liste avec de nouveaux candidats et scores.
        utiliser dans refresh de MWindow
        
        Args:
            new (list): Candidat représentant les nouveaux candidats.
        """
        # Nettoyer la liste
        logging.info("<Rafraichissement de liste>")
        self.clean()
        # Ajouter de nouveaux points à la liste
        for cand in new:
            self.ajouter_element(cand,0)
        logging.info('              Liste rafraichie avec les nouveaux points.')
        # Afficher à nouveau le widget avec les nouveaux candidats
        self.show()
        logging.info("<Fin rafraichissement de liste>")   

    def refresh_MV(self, new_candidats):
        """
        Rafraîchit listeResultat avec de nouveaux candidats. Tous les scores des anciens candidats
        sont remis à 0, sauf si le candidat est également dans la nouvelle liste.
        
        Args:
            new_candidats (list): Liste des nouveaux candidats (candidat, score).
        """
        # Création d'un dictionnaire pour un accès rapide et pour éviter les doublons
        updated_points = {cand: score for cand, score in new_candidats}
        
        # Ajouter ou mettre à jour les candidats existants avec le score à 0 si non présents dans les nouveaux candidats
        for (cand, _ ) in self.l_points:
            if cand not in updated_points:
                updated_points[cand] = 0
        # Nettoyer la liste actuelle
        self.clean()
        
        # Ajouter les éléments mis à jour
        for cand, score in updated_points.items():
            self.ajouter_element(cand, score)
        
        self.show()
