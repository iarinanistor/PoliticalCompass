# en developement
import sys
import math
from PySide6.QtWidgets import QApplication, QDialog, QGraphicsView, QGraphicsScene, QGraphicsItem, QVBoxLayout, QGraphicsLineItem
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPolygonF
from PySide6.QtCore import QRectF, Qt, QPointF,QLineF

class NodeItem(QGraphicsItem):
    """
    Représente un nœud de l'arbre de tournois dans la scène graphique.
    """
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.rect = QRectF(0, 0, 100, 50)  # Taille du nœud

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        # Dessiner le rectangle du nœud
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QColor(200, 200, 255))
        painter.drawRect(self.rect)

        # Dessiner le texte au centre du nœud
        painter.setFont(QFont("Arial", 12))
        painter.drawText(self.rect, Qt.AlignCenter, self.text)

class ArrowItem(QGraphicsLineItem):
    """
    Représente une flèche entre deux nœuds de l'arbre de tournois.
    """
    def __init__(self, start_point, end_point, parent=None):
        super().__init__(parent)
        # Définir la ligne directement avec QLineF
        self.setLine(QLineF(start_point, end_point))
        self.start_point = start_point
        self.end_point = end_point

    def paint(self, painter, option, widget=None):
        # Dessiner la ligne
        painter.setPen(QPen(Qt.white, 2))
        painter.drawLine(self.line())

        # Dessiner la pointe de la flèche
        arrow_head = QPolygonF()
        line_angle = math.radians(self.line().angle())

        arrow_size = 10
        arrow_head.append(self.end_point)
        arrow_head.append(self.end_point + QPointF(-arrow_size * math.cos(line_angle + math.pi / 6), 
                                                   -arrow_size * math.sin(line_angle + math.pi / 6)))
        arrow_head.append(self.end_point + QPointF(-arrow_size * math.cos(line_angle - math.pi / 6), 
                                                   -arrow_size * math.sin(line_angle - math.pi / 6)))

        painter.setBrush(Qt.white)
        painter.drawPolygon(arrow_head)


class TournamentTreeView(QDialog):
    """
    Fenêtre de dialogue affichant l'arbre du tournoi sous forme graphique.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vue de l'Arbre du Tournoi")
        self.setGeometry(300, 300, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        layout.addWidget(self.view)
        self.build_tree()

    def build_tree(self):
        # Créer des nœuds de démonstration
        node1 = NodeItem("Participant 1")
        node2 = NodeItem("Participant 2")
        node3 = NodeItem("Finale")

        # Ajouter les nœuds à la scène
        self.scene.addItem(node1)
        self.scene.addItem(node2)
        self.scene.addItem(node3)

        # Positionner les nœuds
        node1.setPos(100, 100)
        node2.setPos(300, 100)
        node3.setPos(200, 200)

        # Ajouter des flèches entre les nœuds
        arrow1 = ArrowItem(node1.pos() + QPointF(50, 50), node3.pos() + QPointF(50, 0))
        arrow2 = ArrowItem(node2.pos() + QPointF(50, 50), node3.pos() + QPointF(50, 0))
        self.scene.addItem(arrow1)
        self.scene.addItem(arrow2)


# Code pour exécuter l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = TournamentTreeView()
    dialog.show()
    sys.exit(app.exec())
