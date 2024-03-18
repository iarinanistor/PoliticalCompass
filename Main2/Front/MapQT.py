from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem,QGraphicsItem
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt


class Map_QT(QWidget):
    def __init__(self, color=Qt.white, size=500, nb_lines=10):
        super().__init__()
        """
        Constructeur de la classe Map_QT.

        Args:
            color (Qt.GlobalColor): Couleur de fond de la carte. Par défaut, Qt.white.
            size (int): Taille de la carte. Par défaut, 500.
            nb_lines (int): Nombre de lignes pour la grille. Par défaut, 10.
        """
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.scene.setSceneRect(0, 0, size, size)  # Définir la taille de la scène
        self.view.setGeometry(0, 0, size, size)

        self.color = color
        self.size = size
        self.nb_lines = nb_lines

        self.createGrid()

    def createGrid(self):# dessine la grille
        """
        Crée la grille sur la carte.
        """
        self.drawColoredBackground()
        pen = QPen(Qt.black)
        for x in range(0, self.size, self.size // self.nb_lines):
            self.scene.addLine(x, 0, x, self.size, pen)
        for y in range(0, self.size, self.size // self.nb_lines):
            self.scene.addLine(0, y, self.size, y, pen)

    def clearPoints(self):  # Efface tous les points de la scène
        """
        Efface tous les points de la scène.
        """
        for item in self.scene.items():
            if isinstance(item, QGraphicsEllipseItem):
                self.scene.removeItem(item)

    def placePoint(self, x, y, color): # pour placer un point
        """
        Place un point sur la carte.

        Args:
            x (int): Coordonnée x du point.
            y (int): Coordonnée y du point.
            color (QColor): Couleur du point.
        """
        item = self.scene.addEllipse(x, y, 10, 10, pen=QPen(color), brush=color)
        item.setFlag(QGraphicsItem.ItemIsMovable)

    def refresh_Map(self,new):
        """
        Actualise la carte avec de nouveaux points.

        Args:
            new (list): Liste des nouveaux points à afficher.
        """
        self.clearPoints()
        
        for name, color, score,(x,y) in new:
            self.placePoint(x,y,color)
        
        self.show()

    def drawColoredBackground(self):
        """
        Dessine un fond coloré sur la carte.
        """
        quarter_size = self.size // 2
        #colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow]
        colors = [QColor(255, 187, 187), QColor(187, 255, 187), QColor(187, 187, 255), QColor(255, 255, 187)] # Couleurs pastel pour chaque quart de la carte
        for i in range(2):
            for j in range(2):
                color = colors[i * 2 + j]
                self.scene.addRect(i * quarter_size, j * quarter_size, quarter_size, quarter_size,
                                   QPen(Qt.NoPen), QBrush(color))
       
class Compass(Map_QT):
    def __init__(self, size=550, nb_lines=100):
        """
        Constructeur de la classe Compass.

        Args:
            size (int): Taille de la boussole. Par défaut, 550.
            nb_lines (int): Nombre de lignes pour la grille. Par défaut, 100.
        """
        super().__init__(color=Qt.lightGray, size=size, nb_lines=nb_lines)

        # Créer un layout pour le widget Compass
        self.compass_layout = QVBoxLayout(self)
        self.setLayout(self.compass_layout)

        # Utiliser le QGraphicsView créé dans la classe parente
        self.view.setSceneRect(0, 0, size, size)  # Réutiliser la scène existante et redéfinir sa taille
        self.view.setFixedSize(size, size)  # Définir une taille fixe pour le QGraphicsView
        self.compass_layout.addWidget(self.view)  # Ajouter le QGraphicsView au layout
        self.createGrid()  # Vous pouvez supprimer cette ligne si vous ne voulez pas redessiner la grille

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    compass = Compass()
    compass.show()
    sys.exit(app.exec())