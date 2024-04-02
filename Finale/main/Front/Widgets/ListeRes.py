from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QLabel,QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class PointWidget(QWidget):
    def __init__(self, color, name, value):
        super().__init__()
        layout = QHBoxLayout()
        self.color_label = QLabel()
        self.color_label.setFixedSize(20, 20)
        self.set_color(color)
        self.name_label = QLabel(name)
        self.value_label = QLabel(str(value))
        layout.addWidget(self.color_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)
        layout.addStretch(1)  # Ajout d'un espace extensible pour aligner les widgets à droite
        self.setLayout(layout)

    def set_color(self, color):
        style_sheet = "background-color: {}".format(color.name())
        self.color_label.setStyleSheet(style_sheet)

class ListePoint(QWidget):
    def __init__(self, listePoints):
        super().__init__()
        self.points = listePoints
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setFixedSize(300, 200)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.populate_list()

    def populate_list(self):
        # Ajoutez une ligne de texte au-dessus du premier PointWidget
        self.list_widget.insertItem(0, "Color       Nom            classement")

        # Ajoutez des éléments à la liste
        if self.points != []:
            for name, color, score, _ in self.points:
                item = QListWidgetItem(self.list_widget)
                point_widget = PointWidget(color, name, score)
                item.setSizeHint(point_widget.sizeHint())
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, point_widget)

    def ajouter_element(self, name, color, score, position):
        logging.info("<Ajout d'element>")
        logging.info('              Element ajoute - Nom: {}, Couleur: {}, Score: {}, Position: {}.'.format(name, color.name(), score, position))
        new_item = (name, color, score, position)
        self.points.append(new_item)
        item = QListWidgetItem(self.list_widget)
        point_widget = PointWidget(color, name, score)
        item.setSizeHint(point_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, point_widget)
        logging.info("<Fin Ajout d'element>")
    
    def clean(self):
        # Ne pas effacer la première ligne
        logging.info("<Nettoyage")
        for i in range(1, self.list_widget.count()):
            self.list_widget.takeItem(1)
        logging.info('              Liste rafraichie avec les nouveaux points.')
        self.points.clear()
        logging.info("<Fin rafraichissement de liste>")
        
    def refresh_ListPoint(self, new):
    # Nettoyer la liste
        logging.info("<Rafraichissement de liste>")
        self.clean()
        # Ajouter de nouveaux points à la liste
        for name, color, score, position in new:
            self.ajouter_element(name, color, score, position)
        logging.info('              Liste rafraichie avec les nouveaux points.')
        # Afficher à nouveau le widget avec les nouveaux points
        self.show()
        logging.info("<Fin rafraichissement de liste>")
        
    def est_dans_list(self,e,l):
        nom,color,score,position = e
        for elem in l: 
            nomE,_,_,_ = elem
            if nomE==nom: return True
        return False
    
    def refresh_MV(self, new):
        oldP=self.points
        tmp = new
        for e in oldP:
            nom,color,score,position = e
            if not self.est_dans_list(e,new): 
                tmp.append((nom,color,0,position))
        self.clean()
        for e in tmp:
            nom,color,score,position = e
            self.ajouter_element(nom,color,score,position)
        self.show()
        
def test_function():
    # Créer une application Qt
    app = QApplication([])

    # Créer une instance de ListePoint
    liste_widget = ListePoint([])

    # Ajouter quelques éléments initiaux pour tester
    liste_widget.ajouter_element("Monsieur Yellow", QColor(255, 255, 0), 6, (50, 50))
    liste_widget.ajouter_element("Monsieur Purple", QColor(128, 0, 128), 7, (200, 200))
    liste_widget.ajouter_element("Monsieur Orange", QColor(255, 165, 0), 8, (350, 350))

    liste_widget.refresh_MV([("Monsieur Yellow", QColor(255, 255, 0), 6, (50, 50))])
    # Afficher le widget avec les éléments initiaux
    liste_widget.show()

    # Attendre 2 secondes avant de nettoyer la liste
    QTimer.singleShot(4000, lambda: clean_and_add_points(liste_widget))

    # Exécuter l'application
    app.exec()

def clean_and_add_points(liste_widget):
    # Nettoyer la liste
    liste_widget.clean()

    # Ajouter de nouveaux points à la liste
    liste_widget.ajouter_element("Monsieur Red", QColor(255, 0, 0), 1, (25, 25))
    liste_widget.ajouter_element("Monsieur Green", QColor(0, 255, 0), 2, (150, 150))
    liste_widget.ajouter_element("Monsieur Blue", QColor(0, 0, 255), 3, (300, 300))

    # Afficher à nouveau le widget avec les nouveaux points
    liste_widget.show()

def test_refresh_function():
    # Créer une application Qt
    app = QApplication([])

    # Créer une instance de ListePoint
    liste_widget = ListePoint()

    # Ajouter quelques éléments initiaux pour tester
    liste_widget.ajouter_element("Monsieur Yellow", QColor(255, 255, 0), 6, (50, 50))
    liste_widget.ajouter_element("Monsieur Purple", QColor(128, 0, 128), 7, (200, 200))
    liste_widget.ajouter_element("Monsieur Orange", QColor(255, 165, 0), 8, (350, 350))

    # Afficher le widget avec les éléments initiaux
    liste_widget.show()

    # Attendre 2 secondes avant de rafraîchir la liste
    QTimer.singleShot(2000, lambda: refresh_list(liste_widget))

    # Exécuter l'application
    app.exec()

def refresh_list(liste_widget):
    # Nouveaux points à ajouter à la liste
    new_points = [
        ("Monsieur Red", QColor(255, 0, 0), 1, (25, 25)),
        ("Monsieur Green", QColor(0, 255, 0), 2, (150, 150)),
        ("Monsieur Blue", QColor(0, 0, 255), 3, (300, 300))
    ]

    # Rafraîchir la liste avec de nouveaux points
    liste_widget.refresh_ListPoint(new_points)

if __name__ == "__main__":
    test_function()
