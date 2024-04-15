from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, QApplication, QMainWindow, QGraphicsTextItem
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import QRectF, QPointF,Qt


from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem,QGraphicsPixmapItem
from PySide6.QtCore import QPointF
from PySide6.QtGui import QBrush, QColor

from PySide6.QtCore import QPointF, QLineF
from PySide6.QtGui import QPen, QPainter,QPixmap
from PySide6.QtWidgets import QGraphicsLineItem

import random
from Back.Candidat import Candidat
from Front.Utilitaire import generate_unique_colors
class TreeEllipse(QGraphicsEllipseItem):
    def __init__(self, x, y, r=100, color=Qt.white,):
        super().__init__(-r / 2, -r / 2, r, r)
        self.setPos(x, y)
        self.rayon = r
        self.trophee_path = "Front/Widgets/Texture/trophee.png"
        self.cand=None
        self.root=False
        self.leaf=False
        self.color_initial = color
        self.setBrush(QBrush(color))
        self.color = self.brush().color()
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        
        if self.cand is not None: 
            self.text_item = QGraphicsTextItem(self.cand.nom()+" "+self.cand.prenom(), self)
            self.text_item.setDefaultTextColor(QColor("white"))
            self.text_item.setPos(r/2, r / 2 + 10)  # Positionner juste sous l'ellipse

    def affiche_tropher(self):
         # Créer une pixmap à partir du chemin de l'image
            pixmap = QPixmap(self.trophee_path)
            # Réduire l'image de 60% de la taille de l'ellipse
            scaled_size = self.rayon * 0.6
            self.image_item = QGraphicsPixmapItem(pixmap.scaled(scaled_size, scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation), self)
            # Centrer l'image dans l'ellipse
            self.image_item.setPos((self.rayon - scaled_size) / 2 - self.rayon / 2, (self.rayon - scaled_size) / 2 - self.rayon / 2)
            
    def refresh_color(self):
        """
        change la couleur d'un point
        """
        if self.cand is None : raise ValueError(" refresh color avec une cand qui est None")
        else : self.setBrush(QBrush(generate_unique_colors(self.cand.x(), self.cand.y())))
        
    def refresh_victoire(self,root=False):
        if self.cand is None:
            raise ValueError("refresh avec un cand None")
        else:
            # Créer un texte avec le nom et le prénom du candidat
            full_name = self.cand.nom() + " " + self.cand.prenom()
            self.text_item = QGraphicsTextItem(full_name, self)
            self.text_item.setDefaultTextColor(generate_unique_colors(self.cand.x(), self.cand.y()))

            # Ajuster la position du texte
            # (self.rayon / 2) - (self.text_item.boundingRect().height() / 2) centre verticalement le texte par rapport à l'ellipse
            if root or self.leaf: # Ajuster la position du texte pour le centrer horizontalement et le placer en bas
                # Le texte est centré horizontalement en ajustant sa position x avec :
                # (largeur de l'ellipse / 2) - (largeur du texte / 2)
                # Le texte est positionné en bas en ajustant sa position y avec :
                # (hauteur de l'ellipse / 2) + un petit décalage pour l'espacement
                text_x = -self.text_item.boundingRect().width() / 2
                text_y = self.rayon / 2 + 5  # 5 est l'espacement entre le bord inférieur de l'ellipse et le texte
                self.text_item.setPos(text_x, text_y)
                if root:
                    self.affiche_tropher()
            else:   
                text_y = (self.rayon / 2) - (self.text_item.boundingRect().height() / 2)
                self.text_item.setPos(-self.rayon - 10, text_y)

    def connect_ellipses(ellipse1, ellipse2, couleur=QColor(255,255,255), epaisseur_ligne=5, espace=None):
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
        self.construire_arbre()

    
    def calculer_hauteur_arbre(self):
        """
        Calcule la hauteur nécessaire de l'arbre pour le nombre de nœuds donné,
        en supposant un arbre parfaitement équilibré.
        """
        hauteur = 0
        total_noeuds = 0
        while total_noeuds < self.nombre_noeuds:
            total_noeuds += 2 ** hauteur
            hauteur += 1
        return hauteur

    def construire_arbre(self):
        """
        Construit et ajoute des nœuds à la scène en positionnant chaque nœud de manière appropriée.
        """
        niveau_actuel = 0
        noeuds_niveau = 1
        index_noeud = 0
        
        while index_noeud < self.nombre_noeuds:
            espace_x = self.largeur / noeuds_niveau
            y = 150 * niveau_actuel  # Augmenter le décalage vertical entre les niveaux
            
            for i in range(noeuds_niveau):
                if index_noeud >= self.nombre_noeuds:
                    break
                x = i * espace_x + espace_x / 2 - self.rayon_ellipse/2  # pour centrer le nœud
                noeud = TreeEllipse(x, y, self.rayon_ellipse) 
                self.addItem(noeud)
                if index_noeud != 0:
                    # Connecter le nœud au parent
                    parent = self.noeuds[(index_noeud - 1) // 2]
                    ligne = TreeEllipse.connect_ellipses(parent, noeud)
                    self.addItem(ligne)
                self.noeuds.append(noeud)
                index_noeud += 1
            
            niveau_actuel += 1
            noeuds_niveau *= 2  # Chaque niveau a deux fois plus de nœuds que le précédent
        
class Node:
    def __init__(self, ellipse):
        self.ellipse = ellipse
        self.left = None
        self.right = None
    
    def is_leaf(self):
        if self.left is None and self.right is None:return True
        return False
    
    def find_leaf(self,liste_candidates):
        if self is None:
            return
        if self.is_leaf():
            if liste_candidates == []: raise ValueError("liste vide dans find_leaf")
            self.ellipse.cand = liste_candidates.pop(0)
            self.ellipse.refresh_color()
            self.ellipse.leaf = True
        if self.left:
            self.left.find_leaf(liste_candidates)
        if self.right:
            self.right.find_leaf(liste_candidates)
    
    def preferer(p1,p2): # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # A definir doit choisir le candidat le plus preferer d'apprer la population
        return random.choice([p1, p2])
    
    def match(self,is_root=False):
        if self.is_leaf():
            self.ellipse.refresh_victoire()
            return self    
        else: 
            participant1 = self.left.match()
            participant2 = self.right.match()
            candidat1 = participant1.ellipse.cand
            candidat2 = participant2.ellipse.cand
            winner = Node.preferer(candidat1,candidat2) # utliser ici pour trouver le gagnant 
            self.ellipse.cand = winner
            self.ellipse.refresh_color()
            self.ellipse.refresh_victoire(is_root)
            return self
            
def list_to_binary_tree(values):
    if not values:
        return None
    
    root = Node(values[0])
    queue = [root]
    i = 1
    
    while i < len(values):
        current = queue.pop(0)
        
        if values[i] is not None:
            current.left = Node(values[i])
            queue.append(current.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            current.right = Node(values[i])
            queue.append(current.right)
        i += 1
    
    return root

def print_binary_tree(root):
    if not root:
        return
    
    queue = [root]
    
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            current = queue.pop(0)
            if current:
                if current.ellipse.cand is None: print(current.ellipse.cand, end=" ")
                else: print(current.ellipse.cand.nom(), end=" ")
            else:
                print("None", end=" ")
            if current:
                queue.append(current.left)
                queue.append(current.right)
        print()

class Tournoi():
    def __init__(self,liste_candidates):
        self.liste_candidates = liste_candidates
        self.nb_leaf = len(liste_candidates)
        self.nombre_noeuds = abs((self.nb_leaf-1)) + self.nb_leaf # formule pour obteneir le nombre de noeud minimal pour un arbre parfait en fonction du nomnbre de feuille
        self.tree_view = TreeView(self.nombre_noeuds)
        self.view = QGraphicsView(self.tree_view)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.resize(1000, 600)
        values = self.tree_view.noeuds
        root = list_to_binary_tree(values)
        root.find_leaf(self.liste_candidates)
        print(root.match(True))
        print_binary_tree(root)
        
def main():
    app = QApplication([])
    l = [ Candidat.random_candidat(i*100+100,i*100+100) for i in range(8)]
    tr = Tournoi(l)
    tr.view.show()
    app.exec()
