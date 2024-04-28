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

import os
from icecream import ic
import copy
from itertools import permutations, product
from Back.Candidat import Candidat
from Back.Map import Map
from Front.Utilitaire import generate_unique_colors

class TreeEllipse(QGraphicsEllipseItem):
    """
    Représente un nœud dans une structure arborescente graphique, visualisé sous la forme d'une ellipse.

    Cette classe fournit une représentation graphique d'un nœud dans une structure de données arborescente. 
    Chaque instance de TreeEllipse représente un nœud dans l'arbre, affiché sous la forme d'une ellipse 
    avec des propriétés personnalisables telles que la position, la taille et la couleur.

    Attributs :
        x (float): La coordonnée x du centre de l'ellipse.
        y (float): La coordonnée y du centre de l'ellipse.
        r (float): Le rayon de l'ellipse.
        color (QColor): La couleur de l'ellipse.

    Méthodes :
        __init__(x, y, r=100, color=Qt.white):
            Initialise l'ellipse avec la position et la couleur spécifiées.

        affiche_tropher():
            Affiche une image de trophée au centre de l'ellipse pour les nœuds gagnants.

        refresh_color():
            Met à jour la couleur de l'ellipse en fonction des propriétés du candidat associé.

        refresh_victoire(root=False):
            Met à jour le texte et l'affichage pour les nœuds racines ou les feuilles de l'arbre.

        connect_ellipses(ellipse1, ellipse2, couleur=QColor(255, 255, 255), epaisseur_ligne=5, espace=None):
            Dessine une ligne connectant deux ellipses avec un espace optionnel entre elles.
    """
    def __init__(self, x, y, r=100, color=Qt.white):
        """
        Initialise l'ellipse avec la position et la couleur spécifiées.

        Args:
            x (float): La coordonnée x de la position.
            y (float): La coordonnée y de la position.
            r (float, optionnel): Le rayon de l'ellipse. Par défaut, 100.
            color (QColor, optionnel): La couleur de l'ellipse. Par défaut, Qt.white.
        """
        super().__init__(-r / 2, -r / 2, r, r)
        self.setPos(x, y)
        self.rayon = r
        self.trophee_path = "Front/Widgets/Texture/trophee.png"
        self.cand = None
        self.root = False
        self.leaf = False
        self.color_initial = color
        self.setBrush(QBrush(color))
        self.color = self.brush().color()
        self.setFlags(QGraphicsItem.ItemIsSelectable)

        # Création d'un élément de texte si un candidat est associé à l'ellipse
        if self.cand:
            self.text_item = QGraphicsTextItem(f"{self.cand.nom()} {self.cand.prenom()}", self)
            self.text_item.setDefaultTextColor(QColor("white"))
            self.text_item.setPos(r / 2, r / 2 + 10)

    def affiche_tropher(self):
        """
        Affiche une image de trophée au centre de l'ellipse pour les noeuds gagnants.
        """
        pixmap = QPixmap(self.trophee_path)
        if pixmap.isNull():
            print("Échec du chargement de l'image ,PATH = ",str(os.getcwd()))
        scaled_size = self.rayon * 0.6
        self.image_item = QGraphicsPixmapItem(pixmap.scaled(scaled_size, scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation), self)
        self.image_item.setPos((self.rayon - scaled_size) / 2 - self.rayon / 2, (self.rayon - scaled_size) / 2 - self.rayon / 2)

    def refresh_color(self):
        """
        Met à jour la couleur de l'ellipse en fonction des propriétés du candidat associé.

        Raises:
            ValueError: Si aucun candidat n'est assigné à l'ellipse.
        """
        if not self.cand:
            raise ValueError("Tentative de rafraîchir la couleur sans candidat assigné.")
        else:
            self.setBrush(QBrush(generate_unique_colors(self.cand.x(), self.cand.y())))

    def refresh_victoire(self, root=False):
        """
        Met à jour le texte et l'affichage pour les nœuds racines ou les feuilles de l'arbre.

        Args:
            root (bool): Indique si le nœud est un nœud racine. Par défaut, False.

        Raises:
            ValueError: Si aucun candidat n'est assigné au nœud.
        """
        if not self.cand:
            raise ValueError("Tentative de rafraîchir un noeud sans candidat.")
        else:
            full_name = f"{self.cand.nom()} {self.cand.prenom()}"
            self.text_item = QGraphicsTextItem(full_name, self)
            self.text_item.setDefaultTextColor(generate_unique_colors(self.cand.x(), self.cand.y()))
            if root or self.leaf:
                text_x = -self.text_item.boundingRect().width() / 2
                text_y = self.rayon / 2 + 5
                self.text_item.setPos(text_x, text_y)
                if root:
                    self.affiche_tropher()
            else:
                text_y = (self.rayon / 2) - (self.text_item.boundingRect().height() / 2)
                self.text_item.setPos(-self.rayon - 10, text_y)

    @staticmethod
    def connect_ellipses(ellipse1, ellipse2, couleur=QColor(255, 255, 255), epaisseur_ligne=5, espace=None):
        """
        Dessine une ligne connectant deux ellipses avec un espace optionnel entre elles.

        Args:
            ellipse1 (TreeEllipse): La première ellipse.
            ellipse2 (TreeEllipse): La deuxième ellipse.
            couleur (QColor, optionnel): La couleur de la ligne. Par défaut, QColor(255, 255, 255).
            epaisseur_ligne (int, optionnel): L'épaisseur de la ligne. Par défaut, 5.
            espace (float, optionnel): L'espace entre les ellipses. Par défaut, None.

        Returns:
            QGraphicsLineItem: L'élément graphique de la ligne connectant les ellipses.
        """
        centre1 = QPointF(ellipse1.rect().center().x() + ellipse1.x(), ellipse1.rect().center().y() + ellipse1.y())
        centre2 = QPointF(ellipse2.rect().center().x() + ellipse2.x(), ellipse2.rect().center().y() + ellipse2.y())
        ligne = QLineF(centre1, centre2)

        if espace is None:
            espace = ellipse1.rayon / 2
        point1 = ligne.pointAt(espace / ligne.length())
        point2 = ligne.pointAt(1 - espace / ligne.length())
        objet_ligne = QGraphicsLineItem(point1.x(), point1.y(), point2.x(), point2.y())
        objet_ligne.setPen(QPen(couleur, epaisseur_ligne))
        return objet_ligne

class TreeView(QGraphicsScene):
    """
    Représente la scène où les ellipses et leurs connexions sont organisées pour former un arbre.

    Attributes:
        nombre_noeuds (int): Le nombre de nœuds dans l'arbre.
        noeuds (list): Une liste contenant les ellipses représentant les nœuds de l'arbre.
        rayon_ellipse (int): Le rayon des ellipses représentant les nœuds.
        hauteur (int): La hauteur de l'arbre, calculée pour un arbre parfaitement équilibré.
        largeur (float): La largeur totale de la scène, calculée en fonction du nombre de niveaux de l'arbre.

    Methods:
        calculer_hauteur_arbre: Calcule la hauteur nécessaire pour un arbre parfaitement équilibré avec le nombre de nœuds donné.
        construire_arbre: Organise graphiquement les nœuds dans la scène pour créer l'arbre.
    """
    def __init__(self, nombre_noeuds, parent=None):
        """
        Initialise la scène avec le nombre de nœuds spécifié et construit l'arbre.

        Args:
            nombre_noeuds (int): Le nombre de nœuds dans l'arbre.
            parent (QObject, optional): L'objet parent de la scène. Par défaut, None.
        """
        super().__init__(parent)
        self.nombre_noeuds = nombre_noeuds
        self.noeuds = []
        self.rayon_ellipse = 100
        self.hauteur = self.calculer_hauteur_arbre()
        self.largeur = 2 ** (self.hauteur - 1) * self.rayon_ellipse + self.rayon_ellipse / 5  # Calcul pour espacer horizontalement les nœuds
        self.construire_arbre()

    def calculer_hauteur_arbre(self):
        """
        Détermine la hauteur nécessaire pour un arbre parfaitement équilibré avec le nombre de nœuds donné.

        Returns:
            int: La hauteur de l'arbre.
        """

        hauteur = 0
        total_noeuds = 0
        while total_noeuds < self.nombre_noeuds:
            total_noeuds += 2 ** hauteur
            hauteur += 1
        return hauteur

    def construire_arbre(self):
        """
        Organise les noeuds graphiquement dans la scène pour créer l'arbre.
        """
        niveau_actuel = 0
        noeuds_niveau = 1
        index_noeud = 0
        while index_noeud < self.nombre_noeuds:
            espace_x = self.largeur / noeuds_niveau
            y = 150 * niveau_actuel
            for i in range(noeuds_niveau):
                if index_noeud >= self.nombre_noeuds:
                    break
                x = i * espace_x + espace_x / 2 - self.rayon_ellipse / 2
                noeud = TreeEllipse(x, y, self.rayon_ellipse)
                self.addItem(noeud)
                if index_noeud != 0:
                    parent = self.noeuds[(index_noeud - 1) // 2]
                    ligne = TreeEllipse.connect_ellipses(parent, noeud)
                    self.addItem(ligne)
                self.noeuds.append(noeud)
                index_noeud += 1
            niveau_actuel += 1
            noeuds_niveau *= 2  # Chaque niveau contient deux fois plus de noeuds que le précédent

class Node:
    """
    Représente un nœud dans l'arbre binaire ( Arbre binaire parfait) , contenant des références aux nœuds enfants et à l'ellipse associée.

    Attributes:
        ellipse (TreeEllipse): L'ellipse associée à ce nœud.
        map (Map): la classe ou ce trouve les individus et candidats 
        victoire_defaite (dict): Un dictionnaire contenant les informations sur les victoires et défaites des candidats.
        left (Node): Le nœud enfant gauche.
        right (Node): Le nœud enfant droit.

    Methods:
        is_leaf: Vérifie si le nœud est une feuille (sans enfants).
        find_leaf: Attribue des candidats aux feuilles de l'arbre pour la visualisation des résultats.
        preferer: Détermine le candidat préféré entre deux, basé sur une certaine logique ou critères.
        match: Détermine le gagnant entre les candidats des nœuds enfants et propage le gagnant au parent.

"""
    def __init__(self, ellipse, compass,victoire_defaite):
        """
        Initialise un nœud avec une ellipse, une carte de comportement et des informations de victoire/défaite.

        Args:
            ellipse (TreeEllipse): L'ellipse associée à ce nœud.
            map (Map): la classe ou ce trouve les individus et les  candidats 
            victoire_defaite (dict): Un dictionnaire contenant les informations sur les victoires et défaites des candidats.
        """
        self.map = compass
        self.ellipse = ellipse
        self.victoire_defaite = victoire_defaite
        self.left = None
        self.right = None

    def is_leaf(self):
        """
        Vérifie si le noeud est une feuille (sans enfants).
        """
        return self.left is None and self.right is None

    def find_leaf(self, liste_candidates):
        """
        Attribue des candidats aux feuilles de l'arbre pour la visualisation des résultats.

        Args:
            liste_candidates (list): Une liste de candidats à attribuer aux feuilles de l'arbre.

        Raises:
            ValueError: Si la liste de candidats est vide lors de la recherche de feuilles.
        """
        if not self:
            return
        if self.is_leaf():
            if not liste_candidates:
                raise ValueError("Liste de candidats vide lors de la recherche de feuilles.")
            self.ellipse.cand = liste_candidates.pop(0)
            self.ellipse.refresh_color()
            self.ellipse.leaf = True
        if self.left:
            self.left.find_leaf(liste_candidates)
        if self.right:
            self.right.find_leaf(liste_candidates)

    def preferer(self, p1, p2):
        """
        Détermine le candidat préféré entre deux, basé sur une certaine logique ou critères.

        Args:
            p1 (Candidate): Le premier candidat à comparer.
            p2 (Candidate): Le deuxième candidat à comparer.

        Returns:
            Candidate: Le candidat préféré entre p1 et p2.

        Raises:
            ValueError: Si la préférence du candidat n'est pas définie dans self.victoire_defaite.
        """
        if p2.id in self.victoire_defaite[p1.id]: return p1
        elif p1.id in self.victoire_defaite[p2.id]: return p2
        
        # si il y'a un comportement non voulue
        ic(self.victoire_defaite,p1,p2);raise ValueError(" prferer candidat non definie dans self.victoire_defaite")

    def match(self, is_root=False):
        """
        Détermine le gagnant entre les candidats des nœuds enfants et propage le gagnant au parent.

        Args:
            is_root (bool): Indique si le nœud est la racine de l'arbre. Par défaut, False.

        Returns:
            Node: Le nœud gagnant.
        """
        if self.is_leaf():
            self.ellipse.refresh_victoire()
            return self
        else:
            participant1 = self.left.match()
            participant2 = self.right.match()
            winner = self.preferer(participant1.ellipse.cand, participant2.ellipse.cand)
            self.ellipse.cand = winner
            self.ellipse.refresh_color()
            self.ellipse.refresh_victoire(is_root)
            return self

def list_to_binary_tree(values, map,victoire_defaite):
    """
    Construit un arbre binaire à partir d'une liste de valeurs et l'associe à une carte de comportement.

    Args:
        values (list): Liste des valeurs pour créer les nœuds de l'arbre.
        map (Map): la classe ou ce trouve les individus et les  candidats 
        victoire_defaite (dict): Un dictionnaire contenant les informations sur les victoires et défaites des candidats.

    Returns:
        Node: Le nœud racine de l'arbre binaire construit.
    """

    if not values:
        return None

    root = Node(values[0], map,victoire_defaite)
    queue = [root]
    i = 1

    while i < len(values):
        current = queue.pop(0)

        if values[i] is not None:
            current.left = Node(values[i], map,victoire_defaite)
            queue.append(current.left)
        i += 1

        if i < len(values) and values[i] is not None:
            current.right = Node(values[i], map,victoire_defaite)
            queue.append(current.right)
        i += 1

    return root

def print_binary_tree(root):
    """
    Affiche une représentation textuelle de l'arbre binaire, niveau par niveau.
    Args:
        root (Node): Le noeud racine de l'arbre à afficher.
    """
    if not root:
        return

    queue = [root]
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            current = queue.pop(0)
            if current and current.ellipse.cand:
                print(f"{current.ellipse.cand.nom()}", end=" ")
            else:
                print("None", end=" ")
            if current:
                queue.append(current.left)
                queue.append(current.right)
        print()

class Tournoi:
    """
    Gère le déroulement d'un tournoi dans l'arbre de décision.

    Attributes:
        map (Map): La classe où se trouvent les individus et les candidats.
        liste_candidates (list): La liste des candidats participant au tournoi.
        victoire_defaite (dict): Un dictionnaire contenant les informations sur les victoires et défaites des candidats.
        nb_leaf (int): Le nombre de feuilles dans l'arbre de décision.
        nombre_noeuds (int): Le nombre total de nœuds dans l'arbre de décision.
        tree_view (TreeView): La vue de l'arbre de décision.
        view (QGraphicsView): La vue graphique de l'arbre de décision.
        values (list): Les valeurs associées aux nœuds de l'arbre de décision.
        root (Node): Le nœud racine de l'arbre de décision.

    Methods:
        genere_all_match: Génère toutes les permutations valides des candidats en respectant les contraintes spécifiées.
        dico_contraite: Génère un dictionnaire de contraintes pour une tricherie spécifique.
        fait_gagner: Simule un tournoi et détermine si le tricheur spécifié parvient à gagner.
    """
    def __init__(self, compass, liste_candidates):
        """
        Initialise un tournoi avec une carte de comportement et une liste de candidats.

        Args:
            map (Map): la classe ou ce trouve les individus et les  candidats 
            liste_candidates (list): La liste des candidats participant au tournoi.
        """
        self.map = compass
        self.map.creer_L_population()
        self.liste_candidates = copy.deepcopy(liste_candidates)
        self.victoire_defaite = self.map.contraite_tournoi()
        self.nb_leaf = len(liste_candidates)
        self.nombre_noeuds = (self.nb_leaf - 1) + self.nb_leaf  # Calcul du nombre de noeuds nécessaires pour un arbre complet
        self.tree_view = TreeView(self.nombre_noeuds)
        self.view = QGraphicsView(self.tree_view)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.resize(1000, 600)
        self.values = self.tree_view.noeuds
        self.root = list_to_binary_tree(self.values, self.map,self.victoire_defaite)
        self.root.find_leaf(copy.deepcopy(liste_candidates))
        self.root.match(True)
        #tricheur = self.liste_candidates[len(self.liste_candidates)-1]
        #print(self.dico_contraite(tricheur))
       #self.fait_gagner(tricheur)
        
    def genere_all_match(self,lst, constraints):
        """
        Génère toutes les permutations valides des candidats en respectant les contraintes spécifiées.

        Args:
            lst (list): Liste des candidats à permuter.
            constraints (dict): Dictionnaire contenant les contraintes de permutation.

        Returns:
            list: Liste de toutes les permutations valides des candidats.
        """
        def normalize_permutation(perm):
            normalized = []
            for i in range(0, len(perm), 2):
                pair = sorted(perm[i:i+2], key=lambda x: x.id)  # Utilise une clé de tri basée sur l'id
                normalized.extend(pair)
            return tuple(normalized)

        elements_to_permute = [elem for elem in lst if elem not in constraints.keys()]
        free_permutations = permutations(elements_to_permute)
        valid_permutations = set()

        for free_perm in free_permutations:
            free_perm = list(free_perm)
            for position_combination in product(*constraints.values()):
                if len(set(position_combination)) == len(position_combination):
                    try:
                        temp_perm = free_perm[:]
                        for element, position in zip(constraints.keys(), position_combination):
                            temp_perm.insert(position, element)
                        norm_perm = normalize_permutation(temp_perm)
                        flattened_perm = [item for pair in zip(norm_perm[::2], norm_perm[1::2]) for item in pair]
                        valid_permutations.add(tuple(flattened_perm))
                    except IndexError:
                        continue

        return [list(perm) for perm in valid_permutations]
     
    def dico_contraite(self,tricheur):
        """
        Génère un dictionnaire de contraintes pour une tricherie spécifique.

        Args:
            tricheur (Candidate): Le candidat qui triche.

        Returns:
            dict: Dictionnaire de contraintes pour la tricherie spécifiée.
        """
        victoire_defaite = self.victoire_defaite
        ic(victoire_defaite)
        ic(tricheur.id)
        
        for liste_contraite in victoire_defaite.values(): # verification de si il y a un vainqueur de condorsait 
            if len(liste_contraite) >=len(self.liste_candidates)-2 : return False
            
        if victoire_defaite[tricheur.id] == []:  return False # perndant de condorsait
        
        liste_position = []
        taille = len(victoire_defaite[tricheur.id])
        longeur_liste = len(self.liste_candidates)-1
        for i in range(taille):
            position = longeur_liste -2*(i+1)
            if position<0: break
            liste_position.append(position)
        contraite = { id: liste_position for id in victoire_defaite[tricheur.id]}
        contraite[tricheur.id ]= [len(self.liste_candidates)-1]
        resultat = {cand:value for id,value in contraite.items() for cand in self.liste_candidates if cand.id == id} # remet le pointeur vers l'objet comme clee
        return resultat
        
    def fait_gagner(self,tricheur):
        """
        Simule un tournoi et détermine si le tricheur spécifié parvient à gagner.

        Args:
            tricheur (Candidate): Le candidat qui triche.

        Returns:
            bool: True si le tricheur gagne, False sinon.
        """
        flag=False
        if len(self.liste_candidates)%2 == 1: tricheur = self.liste_candidates.pop(); flag=True
        contrainte = self.dico_contraite(tricheur)
        if contrainte is False : return False
        liste_match = self.genere_all_match(self.liste_candidates,contrainte)  
        i=0
        print(" entrer ")
        ic(liste_match)
        for liste_posilble in liste_match:
            print("tour ",i)
            for cand in liste_posilble:
                print("cand ",cand.id, end = " ")
            print()
            i+=1
            if flag:self.root.find_leaf(liste_posilble.append(tricheur))
            else : self.root.find_leaf(liste_posilble)
            self.root.match(True)
            print(self.root.ellipse.cand.id,"tricher id: ",tricheur.id)
            if self.root.ellipse.cand.id == tricheur.id: print("true");return True
        print("false")
        return False

def arbre_test():
    """
    Fonction de test pour créer et exécuter un tournoi avec des candidats aléatoires.

    Returns:
        Tournoi: L'instance de tournoi créée pour le test.
    """
    l = [Candidat.random_candidat(i * 10 + 10, i * 10 + 10) for i in range(8)]
    map = Map(None,"",l,[],100,100)
    map.generationAleatoire()
    tr = Tournoi(map,l)
    return tr  
    
def main():
    """
    Point d'entrée principal pour exécuter l'application.
    """
    app = QApplication([])
    # Création d'une liste de candidats aléatoires
    l = [Candidat.random_candidat(i * 10 , i * 10) for i in range(5)]
    map = Map(None,"",l,[],100,100)
    map.generationAleatoire()
    tr = Tournoi(map,l)
    tr.view.show()
    app.exec_()

