import logging
from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, QApplication, QMainWindow
from PySide6.QtGui import QPen, QColor, QBrush,QTransform
from PySide6.QtCore import Qt,Signal,QObject
from icecream import ic
from PySide6.QtCore import Signal,QPoint

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class NotFoundException(Exception):
    def __init__(self,x,y, message="Point not found"):
        self.message = message
        super().__init__(self.message+" x :",x," y:",y)
        
class ValException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class ExistException(Exception):
    def __init__(self, message="Il exist deja un point ans cette position"):
        self.message = message
        super().__init__(self.message)

class InteractiveEllipse(QGraphicsEllipseItem):
    pass

# Classe d'assistance pour gérer les signaux
class SignalHelper(QObject):
    touched_point = Signal(InteractiveEllipse)

# Modification de votre classe InteractiveEllipse
class InteractiveEllipse(QGraphicsEllipseItem):
    def __init__(self, x, y, r, color, signal_helper):
        super().__init__(-r / 2, -r / 2, r, r)
        self.setPos(x, y)
        self.color_initial = color
        self.setBrush(QBrush(color))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.signal_helper = signal_helper  # Stocke la référence au helper de signal

    def mousePressEvent(self, event):
        self.signal_helper.touched_point.emit(self)  # Utilise le helper pour émettre le signal
        super().mousePressEvent(event)

    def change_taille(self, delta_r):
        # Obtenez les dimensions actuelles de l'ellipse.
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
        self.setBrush(QBrush(color))

    def reinitialise_color(self):
        self.change_color(self.color_initial)


class Map_QT(QWidget):
    def __init__(self, color=Qt.white, size=500, nb_lines=10):
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
            new (list): Liste des nouveaux points à afficher.
        """
        logging.info('<Map_QT.refresh_Map>')
        self.clearPoints()
        for name, color, score, (x, y) in new:
            self.placePoint(x, y, color)
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
    def __init__(self, size=550, nb_lines=100):
        super().__init__(color=Qt.lightGray, size=size, nb_lines=nb_lines)

        self.compass_layout = QVBoxLayout(self)
        self.setLayout(self.compass_layout)

        self.view.setSceneRect(0, 0, size, size)
        self.view.setFixedSize(size, size)
        self.compass_layout.addWidget(self.view)

        self.createGrid()
        

class PreMap(Compass):
    clicked = Signal(QPoint)
    
    def __init__(self):
        super().__init__(500, 100)
        self.signal_helper = SignalHelper()
        self.liste_points=[]
          
    def find_mouss(self, scenePoint):
        # Retourne l'item à la position de la souris si c'est une ellipse.
        item = self.scene.itemAt(scenePoint, QTransform())
        if item and isinstance(item, InteractiveEllipse):
            return item
        return None
        
    def place_point(self, x, y, color, r,fonction):
        # Utilise InteractiveEllipse pour ajouter des ellipses interactives à la scène.
        ellipse = InteractiveEllipse(x, y, r, color,self.signal_helper)
        self.signal_helper.touched_point.connect(fonction)
        self.liste_points.append(ellipse)
        self.scene.addItem(ellipse)
        return ellipse

    def change_color_p(self, p, color):
        # Directement sur l'ellipse, si p est une référence à une InteractiveEllipse.
        if isinstance(p, InteractiveEllipse):
            p.setBrush(QColor(color))
                
    def mousePressEvent(self, event):
        # Émet le signal clicked avec la position du clic convertie en coordonnées de la scène.
        scenePoint = self.view.mapToScene(event.pos())
        self.clicked.emit(scenePoint.toPoint())
        event.accept()
    
    def suprime_point(self, point_a_supprimer):
        if point_a_supprimer in self.liste_points: self.liste_points.remove(point_a_supprimer) 
        
    def affiche_point(self):
        print("\n")
        for point in self.liste_points:
            print("           ",point)
        print("\n")
    
    def refresh(self):
        self.scene.update()
        self.view.update()


                
                 
class HitMap(Compass):
    def __init__(self, taille, taille_grille=550, nbLigne=100):
        super().__init__(taille_grille, nbLigne)

        self.coef = taille_grille / taille
        self.taille = taille

    def placePoint(self, x, y, color):
        """
        Place un point sur la carte.

        Args:
            x (int): Coordonnée x du point.
            y (int): Coordonnée y du point.
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
        Place tous les points sur la carte.

        Args:
            map (object): Objet carte.
            mc (list): Liste des points.
            prefect (tuple): Coordonnées du point préfet.
        """
        logging.info('<HitMap.placeALL>')
        for pop in map.L_population:
            self.placePoint(pop.x, pop.y, QColor(255, 0, 0))
        for ind in mc:
            self.placePoint(ind.x(), ind.y(), QColor(0, 0, 0))
        for cand in map.liste_electeur:
            self.placePoint(cand.x(), cand.y(), QColor(255, 100, 200))
        x, y = prefect
        self.placePoint(x, y, QColor(255, 255, 255))
        logging.info('</HitMap.placeALL>')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    logging.info('<__main__>')
    map = PreMap()
    x,y = 250,250
    map.place_point(x,y, QColor(255, 0, 0),30)
    for item in map.scene.items():
        if isinstance(item, QGraphicsEllipseItem):
            print(f"Élément à x={item.pos().x()}, y={item.pos().y()}, rect={item.rect()}")
    #map.change_rayon(x,y,10)
    map.show()
    logging.info('</__main__>')
    sys.exit(app.exec())
