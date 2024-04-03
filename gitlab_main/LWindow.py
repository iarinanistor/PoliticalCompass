import sys
from Back.Inteligent.Hand import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Front.Widgets.MapQT import PreMap
from Back.Map import *
from BaseDonnee.Base_Donnee import *
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from PySide6.QtCore import QObject, QEvent

class EventFilter(QObject):
    def eventFilter(self, watched, event):
        """
        Permet de rendre la console plus lisibles , car la Windo renvoie des alerte sur des clique non traiter.
        """
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
        
class CreationButton(QWidget):
    def __init__(self,premap):
        super().__init__()
        self.premap =premap
        self.initializeUI()
        
    def initializeUI(self):
        self.setGeometry(100, 100, 200, 100)

        # Création du bouton
        self.button = QPushButton("Creer Map")
        
        # Connexion du signal "clicked" du bouton à la méthode slot
        self.button.clicked.connect(self.onButtonClick)

        # Mise en place du layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def onButtonClick(self):
        self.premap.creation_final()

class TypeGenerationButton(QWidget):
    def __init__(self,lwindow,type_generation):
        super().__init__()
        self.lwindow = lwindow
        self.type_generation = type_generation
        self.initializeUI()
        self.coloration(self.type_generation[1])
        
    def initializeUI(self):
        self.setGeometry(100, 100, 200, 100)

        # Création du bouton
        self.button = QPushButton(str(self.type_generation[0]))
        
        # Connexion du signal "clicked" du bouton à la méthode slot
        self.button.clicked.connect(self.onButtonClick)

        # Mise en place du layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def onButtonClick(self):
        self.lwindow.type_generation = self.type_generation
        
    def coloration(self, color):
        # Créer des couleurs avec QColor
        background_color = color  # Bleu
        text_color = QColor(255, 255, 255)  # Blanc
        # Convertir QColor en chaîne de caractères pour la feuille de style
        background_color_str = background_color.name()
        text_color_str = text_color.name()

        # Appliquer les couleurs via les feuilles de style
        self.button.setStyleSheet(f"QPushButton {{background-color: {background_color_str}; color: {text_color_str};}}")

              
                                    
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
        if self.ellipse is None : return
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
        if self.ellipse is None : return
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
        self.coef=1
        self.TAILLE =100
        self.taille_population = 100
        self.cpt_scv = 0
        self.res_scv = []
        self.liste_points = []
        self.type_generation = ("Beta",QColor(0,0,255))
        
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
        
        self.beta = TypeGenerationButton(self,("Beta",QColor(255,0,0)))
        self.beta.setFixedSize(300,100)
        
        self.uniforme = TypeGenerationButton(self,("Uniforme",QColor(0,0,255)))
        self.uniforme.setFixedSize(300,100)
        
        self.expontiel = TypeGenerationButton(self,("Exponentiel",QColor(0,255,0)))
        self.expontiel.setFixedSize(300,100)
        
        self.triangulaire = TypeGenerationButton(self,("Triangulaire",QColor(255,0,255)))
        self.triangulaire.setFixedSize(300,100)
        
        
        self.creebutton = CreationButton(self)
        self.creebutton.setFixedSize(300,100)
        
        main_layout.addWidget(self.compass, alignment=Qt.AlignRight|Qt.AlignTop)
        #main_layout.addWidget(self.zone_button,alignment=Qt.AlignLeft)
        #main_layout.addWidget(self.ellipse_up_B,alignment= Qt.AlignLeft)
        #main_layout.addWidget(self.ellipse_down_B,alignment=Qt.AlignLeft)
        #main_layout.addWidget(self.sup_B,alignment=Qt.AlignLeft)
        main_layout.addWidget(self.cam_SCV,alignment=Qt.AlignLeft)
        main_layout.addWidget(self.uniforme,alignment=Qt.AlignRight)
        #main_layout.addWidget(self.beta,alignment=Qt.AlignRight)
        #main_layout.addWidget(self.expontiel,alignment= Qt.AlignTop)
        main_layout.addWidget(self.triangulaire,alignment= Qt.AlignTop) 
        main_layout.addWidget(self.creebutton,alignment=Qt.AlignLeft)
        
        self.setGeometry(100, 100, 1250, 900)
        self.compass.clicked.connect(self.handleCompassClick)
        
    def refersh_button(self):
        """
         Permet de changer l'ellipse selectionner dans les differents bouttons ou cela est nécessaire
        """
        self.ellipse_up_B.changeEllipse(self.ellipse_select)
        self.ellipse_down_B.changeEllipse(self.ellipse_select)
        self.sup_B.changeEllipse(self.ellipse_select)
        
    def ellipse_touched(self,ellipse):
        """
        Fonction lier avec la classe InteractiveEllipse permet de traiter le siganle recus en changenat la couleur et l'ellipse selectioner 
        """
        if ellipse == self.ellipse_select: return
        if (ellipse != self.ellipse_select) and self.ellipse_select is not None:
            self.ellipse_select.reinitialise_color()
        self.ellipse_select = ellipse
        self.ellipse_select.change_color(QColor(255,255,255))
        self.refersh_button()
        
    def handleCompassClick(self, point):
        """
        point : object natif de Pyside6
        
        Fonction que est lier avec PreMap cette fonction recupper le signal d'un clique sur le compass et place un point
        """
        
        scenePoint = self.compass.view.mapToScene(point)
        adjustedX = scenePoint.x()-15
        adjustedY = scenePoint.y()-15
        self.openPopup()
        p = self.compass.place_point(adjustedX, adjustedY, self.type_generation[1], 500*0.20,self.ellipse_touched)
        self.liste_points.append((p,self.type_generation,self.taille_population))
    
    def openPopup(self):
        # Fonction pour ouvrir la popup de saisie d'un entier
        value, ok = QInputDialog.getInt(self, 'Saisie d\'un entier', 'Veuillez entrer la taille de la population :')
        if ok:
            self.taille_population = int(value)
                
    def fonction_SCV(self,res):
        """
        Fonction lier avec SCV, permet de chnager la taille du point en fonction de scv
        """
        self.cpt_scv+=1
        if self.cpt_scv >= 2:
            if self.ellipse_select is None :  return
            if res == -1: self.coef = -1; return 
            if res == 0 : self.coef = 1; return 
            self.ellipse_select.change_taille(500*res*self.coef)
            self.cpt_scv=0
            self.compass.refresh()
            QApplication.processEvents()
            
    def creation_map(self):
        pop = [[None] * self.TAILLE for _ in range(self.TAILLE)]
        map = Map(None," personalisée ",[],pop,self.TAILLE ,self.TAILLE )
        print("l",self.liste_points)
        for (p,type_generation,taille_population) in self.liste_points:
            x=int(p.get_x()/(500/self.TAILLE ))# met les coordonées dans un map de taille " self.taille"
            y=int(p.get_y()/(500/self.TAILLE ))
            r=int(p.get_rayon()/(500/self.TAILLE ))
            print(x,y,r,type_generation[0],taille_population, end = " ")
            map.generation_pers((x,y,r),type_generation[0],taille_population)
        return map 
    
    def creation_final(self):
        print("Creation")
        map = self.creation_map()
        self.close()
        bd = Base_donnee.creer("Your Wolrd",Pl=True,map=map)
        bd.window.show()
        print("Fin")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LWindow()
    window.show()
    sys.exit(app.exec())
 