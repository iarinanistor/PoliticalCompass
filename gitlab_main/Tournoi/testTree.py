from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, QApplication, QMainWindow
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import QRectF, QPointF,Qt


from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PySide6.QtCore import QPointF
from PySide6.QtGui import QBrush, QColor

import math
from PySide6.QtCore import QPointF, QLineF
from PySide6.QtGui import QPen, QPainter
from PySide6.QtWidgets import QGraphicsLineItem

class TreeEllipse(QGraphicsEllipseItem):
    def __init__(self, x, y, r=100, color=Qt.white):
        super().__init__(-r / 2, -r / 2, r, r)
        self.setPos(x, y)
        self.rayon = r
        self.color_initial = color
        self.setBrush(QBrush(color))
        self.setFlags(QGraphicsItem.ItemIsSelectable)


def connect_ellipses(ellipse1, ellipse2, couleur=QColor(0,255,0), epaisseur_ligne=5, espace=None):
    """
    Trace une ligne entre les bords de deux objets QGraphicsEllipseItem avec un espace spécifié de chaque bord.
    
    Args:
    ellipse1 (QGraphicsEllipseItem): Le premier objet ellipse.
    ellipse2 (QGraphicsEllipseItem): Le deuxième objet ellipse.
    couleur (Qt.Color): La couleur de la ligne.
    epaisseur_ligne (int): L'épaisseur de la ligne.
    espace (int): L'espace entre la fin de la ligne et le bord de l'ellipse.
    
    Returns:
    QGraphicsLineItem: L'objet de ligne connectant les bords des deux ellipses avec un espace.
    """
    # Calculer les centres des ellipses
    centre1 = QPointF(ellipse1.rect().center().x() + ellipse1.x(),
                      ellipse1.rect().center().y() + ellipse1.y())
    centre2 = QPointF(ellipse2.rect().center().x() + ellipse2.x(),
                      ellipse2.rect().center().y() + ellipse2.y())
    
    # Créer la ligne du centre à centre
    ligne = QLineF(centre1, centre2)
    
    # Calculer la ligne réduite avec les espaces
    if espace is None: espace = ellipse1.rayon/2 # les deux ellipses ont le meme rayon 
    point1 = ligne.pointAt(espace / ligne.length())  # Calculer le point avec l'espace sur la première ellipse
    point2 = ligne.pointAt(1 - espace / ligne.length())  # Calculer le point avec l'espace sur la deuxième ellipse

    # Créer un objet ligne à partir des points ajustés
    objet_ligne = QGraphicsLineItem(point1.x(), point1.y(), point2.x(), point2.y())
    objet_ligne.setPen(QPen(couleur, epaisseur_ligne))  # Définir la couleur et l'épaisseur de la ligne
    
    return objet_ligne

class TreeView(QGraphicsScene):
    def __init__(self, nombre_noeuds, parent=None):
        super().__init__(parent)
        self.nombre_noeuds = nombre_noeuds
        self.noeuds = []
        self.rayon_ellipse = 100
        self.hauteur = self.calculer_hauteur_arbre()
        self.largeur = 2 ** (self.hauteur - 1) * self.rayon_ellipse+self.rayon_ellipse/5  # Augmenter l'espace horizontal entre les nœuds
    
    def ajouet_feuille_arbre(self,candidat):
        
