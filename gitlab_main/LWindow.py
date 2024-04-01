import sys
from Back.Inteligent.Hand import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Front.Widgets.MapQT import PreMap
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from PySide6.QtCore import QObject, QEvent

class EventFilter(QObject):
    def eventFilter(self, watched, event):
        # Ici, vous pouvez décider de filtrer les événements en fonction de leur type.
        # Par exemple, pour ignorer les clics de souris:
        if event.type() == QEvent.MouseButtonPress:
            return True  # Événement traité, ne pas propager
        # Pour tous les autres types d'événements, retourner False permet leur propagation normale.
        return False
class StartSCVButton(QWidget):
    def __init__(self,scv):
        super().__init__()
        self.scv = scv
        self.initializeUI()
        
    def initializeUI(self):
        self.setGeometry(100, 100, 200, 100)

        # Création du bouton
        self.button = QPushButton(" Activer CV ")
        
        # Connexion du signal "clicked" du bouton à la méthode slot
        self.button.clicked.connect(self.onButtonClick)

        # Mise en place du layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def onButtonClick(self):
        self.scv.start()
            
                                    
class RayonButton(QWidget):
    def __init__(self,ellipse,coef=0.1):
        super().__init__()
        self.ellipse = ellipse
        self.coef = coef
        self.initializeUI()
        
    def initializeUI(self):
        self.setGeometry(100, 100, 200, 100)

        # Création du bouton
        self.button = QPushButton('add'+str(self.coef), self)
        
        # Connexion du signal "clicked" du bouton à la méthode slot
        self.button.clicked.connect(self.onButtonClick)

        # Mise en place du layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def onButtonClick(self):
        # Cette méthode est appelée chaque fois que le bouton est cliqué.
        self.ellipse.change_taille(500*self.coef)
        
    def changeEllipse(self,ellipse):
        self.ellipse = ellipse
        
class SuppButton(QWidget):
    def __init__(self,map,ellipse):
        super().__init__()
        self.map = map
        self.ellipse = ellipse
        self.initializeUI()
        
    def initializeUI(self):
        self.setWindowTitle('')
        self.setGeometry(100, 100, 200, 100)

        # Création du bouton
        self.button = QPushButton("delete", self)
        
        # Connexion du signal "clicked" du bouton à la méthode slot
        self.button.clicked.connect(self.onButtonClick)

        # Mise en place du layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def onButtonClick(self):
        if self.ellipse and self.ellipse.scene():
            self.ellipse.scene().removeItem(self.ellipse)
            self.map.suprime_point(self.ellipse)
            self.ellipse = None 
            
    def changeEllipse(self,ellipse):
        self.ellipse = ellipse
        
        
class ZoneButton(QWidget):  # Hérite de QWidget pour utiliser un layout
    def __init__(self,map,l=200,h=80):
        super().__init__()
        layout = QVBoxLayout()
        # Definir la taille du widget
        self.setFixedSize(l, h*2.5)
        self.map = map
        valeurs_layout = QHBoxLayout()
        self.valeur_edits = []  # Liste pour stocker les boutons de type QSpinBox
        nom_boutons = ["RAYON ", "  X", "  Y"]
        for i in range(3):  # Trois champs d'entier côte à côte
            label = QLabel(nom_boutons[i])
            edit = QSpinBox()
            # Vous pouvez définir d'autres limites si nécessaire
            edit.setMinimum(0)
            edit.setMaximum(100)
            valeurs_layout.addWidget(label)
            valeurs_layout.addWidget(edit)
            self.valeur_edits.append(edit)  # Ajouter le bouton à la liste
        
        layout.addLayout(valeurs_layout)
        
        # Bouton pour soumettre les informations
        self.submit_button = QPushButton("Soumettre")
        self.submit_button.clicked.connect(self.afficher_informations)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)
        
        # Redimensionner le widget principal
        #self.resize(h,l)  # Largeur : 600 pixels, Hauteur : 200 pixels
    def refresh_champ(self):
        for edit in self.valeur_edits:
            edit.setValue(0)
            
    def afficher_informations(self):
        self.submit_button.setEnabled(False)
        rayon = [edit.value() for edit in self.valeur_edits]
        x,y,r = rayon
        self.map.place_point(x,y,QColor(0,255,0),r)
        
        
        self.refresh_champ()
        self.submit_button.setEnabled(True)
    
      
        
class LWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.scv = SCV(self)
        self.cpt_scv = 0
        self.res_scv = []
        self.liste_points = []
        self.type_generation = "aleatoire"
        main_layout = QVBoxLayout(self)
        self.ellipse_select = None
          
        self.compass = PreMap()
        self.compass.setFixedSize(500, 500)
        
        self.zone_button = ZoneButton(self.compass)
        self.zone_button.setFixedSize(300,100)
        
        self.ellipse_up_B = RayonButton(self.ellipse_select)
        self.ellipse_down_B = RayonButton(self.ellipse_select,-0.1)
        
        self.ellipse_up_B.setFixedSize(300,100)
        self.ellipse_down_B.setFixedSize(300,100)
        
        self.sup_B = SuppButton(self.compass,self.ellipse_select)
        self.sup_B.setFixedSize(300,100)
        
        self.cam_SCV = StartSCVButton(self.scv)
        self.cam_SCV.setFixedSize(300,100)
        
        main_layout.addWidget(self.compass, alignment=Qt.AlignRight|Qt.AlignTop)
        #main_layout.addWidget(self.zone_button,alignment=Qt.AlignLeft)
        main_layout.addWidget(self.ellipse_up_B,alignment= Qt.AlignLeft)
        main_layout.addWidget(self.ellipse_down_B,alignment=Qt.AlignLeft)
        main_layout.addWidget(self.sup_B,alignment=Qt.AlignLeft)
        main_layout.addWidget(self.cam_SCV,alignment=Qt.AlignLeft)
        
        self.setGeometry(100, 100, 1250, 900)
        self.compass.clicked.connect(self.handleCompassClick)
        
    def refersh_button(self):
        self.ellipse_up_B.changeEllipse(self.ellipse_select)
        self.ellipse_down_B.changeEllipse(self.ellipse_select)
        self.sup_B.changeEllipse(self.ellipse_select)
        
    def ellipse_touched(self,ellipse):
        if ellipse == self.ellipse_select: return
        if (ellipse != self.ellipse_select) and self.ellipse_select is not None:
            self.ellipse_select.reinitialise_color()
        self.ellipse_select = ellipse
        self.ellipse_select.change_color(QColor(255,255,255))
        self.refersh_button()
        
    def handleCompassClick(self, point):
        scenePoint = self.compass.view.mapToScene(point)
        adjustedX = scenePoint.x()-15
        adjustedY = scenePoint.y()-15
        p = self.compass.place_point(adjustedX, adjustedY, QColor(0, 0, 0), 500*0.20,self.ellipse_touched)
        self.liste_points.append((p,self.type_generation))
    def fonction_SCV(self,res):
        self.cpt_scv+=1
        if self.cpt_scv >= 2:
            if self.ellipse_select is None :  return
            if res == 1: return
            self.ellipse_select.change_taille(500*res)
            self.cpt_scv=0
            self.compass.refresh()
            QApplication.processEvents()
 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LWindow()
    window.show()
    sys.exit(app.exec())
 