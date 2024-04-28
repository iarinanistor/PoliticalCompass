import logging
from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, QApplication, QMainWindow
from PySide6.QtGui import QPen, QColor, QBrush,QTransform
from PySide6.QtCore import Qt,Signal,QObject
from icecream import ic
from PySide6.QtCore import Signal,QPoint
from Front.Utilitaire import generate_unique_colors

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class NotFoundException(Exception):
    """
    Exception levée lorsqu'un point attendu n'est pas trouvé aux coordonnées spécifiées.
    
    Attributs:
        x (int) : La coordonnée x du point non trouvé.
        y (int) : La coordonnée y du point non trouvé.
        message (str) : Explication de l'erreur.
    """
    def __init__(self, x, y, message="Point non trouvé"):
        self.message = message
        super().__init__(f"{self.message} - x : {x}, y : {y}")
        
class ValException(Exception):
    """
    Exception générale pour les erreurs de validation au sein de l'application.
    
    Attributs:
        message (str) : Explication de l'erreur.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class ExistException(Exception):
    """
    Exception levée lors de la tentative d'ajout d'un point qui existe déjà à une position spécifiée.
    
    Attributs:
        message (str) : Explication de l'erreur.
    """
    def __init__(self, message="Il existe déjà un point à cette position"):
        self.message = message
        super().__init__(self.message)


class InteractiveEllipse(QGraphicsEllipseItem):
    pass

# Classe d'assistance pour gérer les signaux
class SignalHelper(QObject):
    touched_point = Signal(InteractiveEllipse)

# Modification de votre classe InteractiveEllipse
class InteractiveEllipse(QGraphicsEllipseItem):
    """
    Sous-classe de QGraphicsEllipseItem améliorée avec interactivité, rendant l'ellipse réactive aux événements de la souris et capable de changer ses propriétés dynamiquement.
    
    Méthodes:
        mousePressEvent : Émet un signal lorsque l'ellipse est cliquée, utile pour l'interaction.
        change_taille : Ajuste la taille de l'ellipse d'un delta spécifié.
        change_color : Change la couleur de l'ellipse.
        reinitialise_color : Réinitialise la couleur de l'ellipse à son état initial.
    """
    def __init__(self, x, y, r, color, signal_helper):
        super().__init__(-r / 2, -r / 2, r, r)
        self.setPos(x, y)
        self.color_initial = color
        self.setBrush(QBrush(color))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.signal_helper = signal_helper  # Stocke la référence au helper de signal

    def get_x(self):

        return self.pos().x()

    def get_y(self):
        return self.pos().y()

    def get_rayon(self):
        return self.rect().width() / 2
    
    def mousePressEvent(self, event):
        """
        permet de detecter la un clicuqe sur la surface du point
        """
        self.signal_helper.touched_point.emit(self)  # Utilise le helper pour émettre le signal
        super().mousePressEvent(event)

    def change_taille(self, delta_r):
        """
        augment la taille d'un point de 'delta_r' , si le rayon du point devient plus petit que 1 alors la fonction ne faire rien.
        """
        # Obtenez les dimensions actuelles de l'ellipse.
        print("chnage_taille")
        rect = self.rect()
        current_width = rect.width()
        current_height = rect.height()

        # Calculez les nouvelles dimensions en ajoutant delta_r à la largeur et à la hauteur actuelles.
        new_width = current_width + delta_r
        new_height = current_height + delta_r
        if(new_width <= 1) and (new_height <= 1): 
            self.setRect(-5/ 2, -5 / 2,5,5)
            return  
        # Mettez à jour le rectangle de l'ellipse pour utiliser les nouvelles dimensions.
        # Ajustez également la position pour que le centre de l'ellipse ne change pas.
        self.setRect(-new_width / 2, -new_height / 2, new_width, new_height)
        # Aucun ajustement de setPos n'est nécessaire ici car le rectangle est ajusté relativement à son centre.
        
    def change_color(self,color):
        """
        change la couleur d'un point
        """
        self.setBrush(QBrush(color))

    def reinitialise_color(self):
        """
        reintialise la couleur d'un point
        """
        self.change_color(self.color_initial)


class Map_QT(QWidget):
    """
    Widget pour afficher et interagir avec une carte graphique 2D utilisant QGraphicsScene et QGraphicsView.

    Attributs:
        color (Qt.Color): Couleur de fond par défaut de la scène.
        size (int): Taille du côté de la scène carrée.
        nb_lines (int): Nombre de lignes de la grille à dessiner sur la carte.
        scene (QGraphicsScene): La scène où tous les éléments graphiques sont ajoutés.
        view (QGraphicsView): Le widget de vue qui affiche la scène.
    
    Méthodes:
        createGrid: Dessine une grille sur la carte pour aider à visualiser les coordonnées.
        clearPoints: Supprime tous les points (ellipses) présents dans la scène.
        placePoint: Ajoute un point sur la carte aux coordonnées et avec la couleur spécifiée.
        refresh_Map: Met à jour la carte avec une nouvelle liste de points.
        drawColoredBackground: Dessine un fond coloré pour la carte, divisé en quatre.
    """
    
    def __init__(self, color=Qt.white, size=500, nb_lines=10):
        """
        Initialise le widget avec une scène et une vue, définit la taille de la scène et de la vue,
        et crée une grille de base.
        """
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.scene.setSceneRect(0, 0, size, size)
        self.view.setGeometry(0, 0, size, size)
        self.view.setSceneRect(0, 0, size, size)
        # Assurez-vous que la scène est bien alignée et visualisée dans la vue.
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.color = color
        self.size = size
        self.nb_lines = nb_lines

        self.createGrid()

    def createGrid(self):
        """
        Crée la grille sur la carte.
        """
        logging.info('<Map_QT.createGrid>')
        self.drawColoredBackground()
        pen = QPen(Qt.black)
        for x in range(0, self.size, self.size // self.nb_lines):
            self.scene.addLine(x, 0, x, self.size, pen)
        for y in range(0, self.size, self.size // self.nb_lines):
            self.scene.addLine(0, y, self.size, y, pen)
        logging.info('</Map_QT.createGrid>')

    def clearPoints(self):
        """
        Efface tous les points de la scène.
        """
        logging.info('<Map_QT.clearPoints>')
        for item in self.scene.items():
            if isinstance(item, QGraphicsEllipseItem):
                self.scene.removeItem(item)
        logging.info('</Map_QT.clearPoints>')

    def placePoint(self, x, y, color, taille=10):
        """
        Place un point sur la carte.

        Args:
            x (int): Coordonnée x du point.
            y (int): Coordonnée y du point.
            color (QColor): Couleur du point.
            taille (int): Taille du point.
        """
        logging.info('<Map_QT.placePoint>')
        logging.info('<Map_QT.placePoint.INFO> x: %s, y: %s, color: %s, taille: %s', x, y, color.name(), taille)
        logging.info('Point placé aux coordonnées ({}, {}) avec la couleur {}.'.format(x, y, color.name()))
        logging.info('</Map_QT.placePoint.INFO>')
        item = self.scene.addEllipse(x, y, 10, 10, pen=QPen(color), brush=color)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        logging.info('</Map_QT.placePoint>')

    def refresh_Map(self, new):
        """
        Actualise la carte avec de nouveaux points.

        Args:
            new (list): Liste des nouveaux Candidat à afficher.
        """
        logging.info('<Map_QT.refresh_Map>')
        self.clearPoints()
        for cand in new:
            x = cand.x()
            y = cand.y()
            self.placePoint(x, y, generate_unique_colors(x,y))
        self.show()
        logging.info('</Map_QT.refresh_Map>')

    def drawColoredBackground(self):
        """
        Dessine un fond coloré sur la carte.
        """
        logging.info('<Map_QT.drawColoredBackground>')
        quarter_size = self.size // 2
        colors = [QColor(255, 187, 187), QColor(187, 255, 187), QColor(187, 187, 255), QColor(255, 255, 187)]
        for i in range(2):
            for j in range(2):
                color = colors[i * 2 + j]
                self.scene.addRect(i * quarter_size, j * quarter_size, quarter_size, quarter_size,
                                   QPen(Qt.NoPen), QBrush(color))
        logging.info('</Map_QT.drawColoredBackground>')

class Compass(Map_QT):
    """
    Classe spécialisée de Map_QT destinée à l'affichage d'une carte avec une échelle proportionnelle ou d'autres adaptations spécifiques.

    Attributs:
        size (int): Taille du côté de la vue de la carte.
        nb_lines (int): Nombre de lignes dans la grille de la carte.
        compass_layout (QVBoxLayout): Layout pour gérer la position des widgets dans cette vue.

    Méthodes:
        refresh_Map: Met à jour la carte avec de nouveaux points ajustés proportionnellement.
    """

    def __init__(self, size=550, nb_lines=100):
        """
        Initialise la carte avec une couleur de fond légèrement grise, une taille et un nombre de lignes spécifiques.
        Configure également la mise en page et la taille fixe de la vue pour un affichage correct.
        """

        super().__init__(color=Qt.lightGray, size=size, nb_lines=nb_lines)

        self.compass_layout = QVBoxLayout(self)
        self.setLayout(self.compass_layout)

        self.view.setSceneRect(0, 0, size, size)
        self.view.setFixedSize(size, size)
        self.compass_layout.addWidget(self.view)

        self.createGrid()
    
    def refresh_Map(self, new):
        """
        Actualise la carte avec de nouveaux points.

        Args:
            new (list): Liste des nouveaux Candidat à afficher.
        """
        logging.info('<Map_QT.refresh_Map>')
        self.clearPoints()
        for cand in new:
            x = cand.x()*5 # on re adapte pour que ce soit proportionelle 
            y = cand.y()*5
            self.placePoint(x, y, generate_unique_colors(x,y))
        self.show()
        logging.info('</Map_QT.refresh_Map>')  

class PreMap(Compass):
    """
    Classe dérivée de Compass pour une carte préparatoire avec des fonctionnalités interactives.
    Gère les points interactifs (InteractiveEllipse)  et les interactions utilisateur telles que les clics sur la carte.

    Attributs:
        signal_helper (SignalHelper): Assistant de signal pour gérer les interactions avec les points.
        liste_points (list): Liste des points interactifs présents sur la carte.
    
    Méthodes:
        place_point: Ajoute un point interactif sur la carte.
        mousePressEvent: Gère les événements de clic de souris sur la carte.
        suprime_point: Supprime un point spécifique de la carte.
        affiche_point: Affiche les points actuellement sur la carte pour le débogage.
        refresh: Rafraîchit la scène pour mettre à jour l'affichage.
        refresh_Map: Met à jour la carte avec de nouveaux points en utilisant des données fournies.
    """
    clicked = Signal(QPoint)
    
    def __init__(self):
        """
        Initialise la carte avec une taille et un nombre de lignes spécifiques, prépare pour l'interaction.
        """
        super().__init__(500, 100)
        self.signal_helper = SignalHelper()
        self.liste_points=[]
        
    def place_point(self, x, y, color, r,fonction):
        """
        Place un point interactif (InteractiveEllipse) sur la carte et connecte un signal à une fonction de gestion de clic.

        Args:
            x, y (int): Coordonnées du point à placer.
            color (QColor): Couleur du point.
            r (double): Rayon du point.
            fonction (callable): Fonction à appeler lorsque le point est cliqué.
        """
        # Utilise InteractiveEllipse pour ajouter des ellipses interactives à la scène.
        ellipse = InteractiveEllipse(x, y, r, color,self.signal_helper)
        self.signal_helper.touched_point.connect(fonction)
        self.liste_points.append(ellipse)
        self.scene.addItem(ellipse)
        return ellipse
                
    def mousePressEvent(self, event):
        """
        Détecte un clic sur la carte et émet un signal avec la position du clic.
        """
        # Émet le signal clicked avec la position du clic convertie en coordonnées de la scène.
        scenePoint = self.view.mapToScene(event.pos())
        self.clicked.emit(scenePoint.toPoint())
        event.accept()
    
    def suprime_point(self, point_a_supprimer):
        """
        Supprime un point spécifié de la liste des points et de la scène.

        Args:
            point_a_supprimer (InteractiveEllipse): Point à supprimer.
        """
        if point_a_supprimer in self.liste_points:
            self.liste_points.remove(point_a_supprimer) 
        
    def affiche_point(self):
        """
        Affiche dans la console les points actuellement présents sur la carte.
        """
        print("\n")
        for point in self.liste_points:
            print(" ",point)
        print("\n")
    
    def refresh(self):
        """
        Rafraîchit la scène graphique pour mettre à jour l'affichage visuel.
        """
        self.scene.update()
        self.view.update()
        
    def refresh_Map(self, new):
        """
        Actualise la carte avec une nouvelle liste de points en effaçant les anciens et en plaçant les nouveaux.

        Args:
            new (list): Liste des nouveaux points à afficher, spécifiés comme des objets avec des attributs x et y.
        """
        logging.info('<Map_QT.refresh_Map>')
        self.clearPoints()
        for cand in new:
            x = cand.x()
            y = cand.y()
            self.placePoint(x, y, generate_unique_colors(x,y))
        self.show()
        logging.info('</Map_QT.refresh_Map>')       
                 
class HitMap(Compass):
    """
    Classe spécialisée de Compass destinée à la représentations de densité de données, utilisé pour ma methode de Monte-Carlo

    Attributs:
        coef (float): Coefficient de mise à l'échelle pour ajuster les points à la taille de la grille.
        taille (int): Taille originale des données qui sera mise à l'échelle.

    Méthodes:
        refresh_Map: Rafraîchit la carte avec de nouveaux points, ajustés selon le coefficient de mise à l'échelle.
        placePoint: Place un point sur la carte à des coordonnées ajustées.
        placeALL: Place tous les types de points sur la carte pour différentes catégories de données.
    """
    def __init__(self, taille, taille_grille=550, nbLigne=100):
        """
        Initialise la HitMap avec une taille spécifique et prépare les coefficients pour l'échelle de mise à jour des points.

        Args:
            taille (int): Dimension de base des données.
            taille_grille (int): Taille de la grille de la carte.
            nbLigne (int): Nombre de lignes de la grille.
        """
        super().__init__(taille_grille, nbLigne)

        self.coef = taille_grille / taille
        self.taille = taille

    def refresh_Map(self, new):
        """
        Actualise la carte avec une liste de nouveaux points, en ajustant leur position selon le coefficient de mise à l'échelle.

        Args:
            new (list): Liste des nouveaux Candidat à afficher, prévus pour être mis à l'échelle.
        """
        logging.info('<Map_QT.refresh_Map>')
        self.clearPoints()
        for cand in new:
            x = cand.x()
            y = cand.y()
            self.placePoint(x, y, generate_unique_colors(x,y))
        self.show()
        logging.info('</Map_QT.refresh_Map>')
        
    def placePoint(self, x, y, color):
        """
        Place un point sur la carte avec ajustement selon le coefficient de mise à l'échelle pour adapter les points à la taille de la grille.

        Args:
            x (int): Coordonnée x du point, avant ajustement.
            y (int): Coordonnée y du point, avant ajustement.
            color (QColor): Couleur du point.
        """
        logging.info('<HitMap.placePoint>')
        logging.info('<HitMap.placePoint.INFO> x: %s, y: %s, color: %s', x, y, color.name())
        logging.info('Point placé aux coordonnées ({}, {}) avec la couleur {}.'.format(x, y, color.name()))
        logging.info('</HitMap.placePoint.INFO>')
        super().placePoint(x * self.coef, y * self.coef, color, (10 / 50) * self.taille)
        logging.info('</HitMap.placePoint>')

    def placeALL(self, map, mc, prefect):
        """
        Place différents types de points sur la carte, utilisés pour visualiser des populations, des points d'intérêt, et d'autres données.

        Args:
            map (object): Objet carte avec la population à visualiser.
            mc (list): Liste des points pour les candidats ou autres marqueurs.
            prefect (tuple): Coordonnées du point optimal pour gagner
        """
        logging.info('<HitMap.placeALL>')
        for pop in map.L_population:
            coef = sum(pop.poids)/map.taille_population
            color = 255*coef
            self.placePoint(pop.x, pop.y, QColor(color, color, color))
        for ind in mc:
            self.placePoint(ind.x(), ind.y(), QColor(0, 0, 0))
        for cand in map.liste_electeur:
            self.placePoint(cand.x(), cand.y(), QColor(255, 100, 200))
        x, y = prefect
        self.placePoint(x, y, QColor(255, 255, 255))
        logging.info('</HitMap.placeALL>')

