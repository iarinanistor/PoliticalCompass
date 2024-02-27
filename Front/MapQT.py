from PySide6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsEllipseItem,QGraphicsItem
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt



class Map_QT(QWidget):
    def __init__(self, color=Qt.white, size=500, nb_lines=10):
        super().__init__()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.scene.setSceneRect(0, 0, size, size)  # Définir la taille de la scène
        self.view.setGeometry(0, 0, size, size)

        self.color = color
        self.size = size
        self.nb_lines = nb_lines

        self.createGrid()

    def createGrid(self):# dessine la grille
        pen = QPen(Qt.black)
        for x in range(0, self.size, self.size // self.nb_lines):
            self.scene.addLine(x, 0, x, self.size, pen)
        for y in range(0, self.size, self.size // self.nb_lines):
            self.scene.addLine(0, y, self.size, y, pen)
            
            
    def clearPoints(self):  # Efface tous les points de la scène
        for item in self.scene.items():
            if isinstance(item, QGraphicsEllipseItem):
                self.scene.removeItem(item)
                
    def placePoint(self, x, y, color): # pour placer un point
        item = self.scene.addEllipse(x, y, 10, 10, pen=QPen(color), brush=color)
        item.setFlag(QGraphicsItem.ItemIsMovable)
    
    def refresh_Map(self,new):
        self.clearPoints()
        
        for name, color, score,(x,y) in new:
            self.placePoint(x,y,color)
        
        self.show()
       
class Compass(Map_QT):
    def __init__(self, size=550, nb_lines=100):
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
    app = QApplication([])

    # Créer une instance de la classe Compass
    compass_widget = Compass()

    # Ajouter quelques points pour tester
    compass_widget.placePoint(100, 100, QColor(Qt.red))
    compass_widget.placePoint(300, 300, QColor(Qt.blue))
    compass_widget.placePoint(500, 200, QColor(Qt.green))
    
    # Afficher le widget
    compass_widget.show()

    # Nouveaux points à afficher après rafraîchissement
    new_points = [("Monsieur Yellow", QColor(255, 255, 0), 6, (50, 50))]

    # Attendre 2 secondes avant de rafraîchir la carte avec de nouveaux points
    QTimer.singleShot(2000, lambda: compass_widget.refresh_Map(new_points))

    # Attendre 6 secondes avant de quitter
    QTimer.singleShot(6000, app.quit)

    # Exécuter l'application
    app.exec()
