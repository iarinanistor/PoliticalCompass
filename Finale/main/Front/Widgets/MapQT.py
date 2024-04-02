import logging
from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, QApplication, QMainWindow
from PySide6.QtGui import QPen, QColor, QBrush
from PySide6.QtCore import Qt

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from Internet import internet
from Internet import iso_code


class Map_QT(QWidget):
    def __init__(self, color=Qt.white, size=500, nb_lines=10):
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.scene.setSceneRect(0, 0, size, size)
        self.view.setGeometry(0, 0, size, size)

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
    hitmap = HitMap(50)
    hitmap.placePoint(24.5, 24.5, QColor(255, 0, 0))
    hitmap.show()
    logging.info('</__main__>')
    sys.exit(app.exec())
