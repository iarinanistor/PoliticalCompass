from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QLabel,QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer

class PointWidget(QWidget):
    def __init__(self, color, name, value):
        """
        Constructeur de la classe PointWidget qui descend de la classe QWidget.

        Args:
            color (str): Nom de couleur du point associée au candidat sur la map.
            name (str): Nom du candidat
            value (int): Position du candidat dans le classement.

        Returns:
            void
        """
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
        """
        Méthode setter pour changer la couleur.

        Returns:
            void
        """
        style_sheet = "background-color: {}".format(color.name())
        self.color_label.setStyleSheet(style_sheet)

class ListePoint(QWidget):
    def __init__(self, listePoints):
        """
        Constructeur de la classe ListePoint qui descend de la classe QWidget.

        Args:
            listePoints (list): Liste de tuples contenant la couleur, le nom 
                                et la position dans le classement du candidat.
        
        Returns:
            void
        """
        super().__init__()
        self.points = listePoints
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.populate_list()

    def populate_list(self):
        """
        Méthode qui ajoute les candidats à la liste list_widget.

        Returns:
            void
        """
        # Ajoutez une ligne de texte au-dessus du premier PointWidget
        self.list_widget.insertItem(0, "Color       Nom            classement")

        # Ajoutez des éléments à la liste
        if self.points != []:
            for name, color, score, _ in self.points:
                item = QListWidgetItem(self.list_widget)
                point_widget = PointWidget(color, name, score)  # Exemple de valeur
                item.setSizeHint(point_widget.sizeHint())
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, point_widget)

    def ajouter_element(self, name, color, score, position):
        """
        Méthode qui ajoute un candidat à la liste list_widget.

        Args:
            name (str): Nom du candidat
            color (str): Couleur du point du candidat sur la map
            score (int): Score du candidat
            position (int): Position du candidat dans le classement
        
        Returns:
            void
        """
        new_item = (name, color, score, position)
        self.points.append(new_item)
        item = QListWidgetItem(self.list_widget)
        point_widget = PointWidget(color, name, score)
        item.setSizeHint(point_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, point_widget)
    
    def clean(self):
        """
        Méthode qui vide la liste des points.

        Returns:
            void
        """
        # Ne pas effacer la première ligne
        for i in range(1, self.list_widget.count()):
            self.list_widget.takeItem(1)
        self.points.clear()
    
    def refresh_ListPoint(self, new):
        """
        Méthode qui rafrachit la liste des points en remplaçant les anciennes valeurs 
        par les nouvelles valeurs.

        Args:
            new (list): Liste de tuples contenant le nom, la couleur, le score
                        et la position dans le classement du candidat.
                
        Returns:
            void
        """
        # Nettoyer la liste
        self.clean()
        # Ajouter de nouveaux points à la liste
        for name, color, score, position in new:
            self.ajouter_element(name, color, score, position)

        # Afficher à nouveau le widget avec les nouveaux points
        self.show()
        
    def est_dans_list(self,e,l):
        """
        Méthode qui vérifie si le tuple e est dans la liste l.

        Args:
            e (tuple): Tuple contenant le nom, la couleur, le score
                        et la position dans le classement du candidat .
            l (list): Liste de tuples
        
        Returns:
            True si e est dans l
            False sinon
        """
        nom,color,score,position = e
        for elem in l: 
            nomE,_,_,_ = elem
            if nomE==nom: return True
        return False
    
    def refresh_MV(self, new):
        """
        Méthode qui vérifie si le tuple e est dans la liste l.

        Args:
            new (list): Liste de tuples contenant le nom, la couleur, le score
                        et la position dans le classement du candidat.

        Returns:
            void
        """
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

#Fonctions de test
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
