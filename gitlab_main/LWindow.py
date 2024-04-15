import sys
from Back.Inteligent.Hand import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Front.Widgets.MapQT import PreMap
from Back.Map import *
from BaseDonnee.BaseDonnee import *
import logging
from icecream import ic
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from PySide6.QtCore import QObject, QEvent

class EventFilter(QObject):
    """
    Classe destinée à filtrer certains événements pour améliorer la lisibilité de la console.
    Principalement utilisée pour ignorer les alertes générées par des clics non traités.
    """
    def eventFilter(self, watched, event):
        # Filtrer les événements de clic de souris pour ne pas les propager.
        if event.type() == QEvent.MouseButtonPress:
            return True  # Indique que l'événement est traité.
        return False  # Permet la propagation des autres types d'événements.

    
    
class StartSCVButton(QWidget):
    """
    Ce widget gère un bouton destiné à activer le processus SCV (Système de Computer vision).
    Il est responsable de l'interaction utilisateur nécessaire pour démarrer ce processus spécifique.
    
    Attributes:
        scv: Une instance ou référence à l'objet qui implémente le processus SCV, permettant de le démarrer lors de l'interaction.
    """
    
    def __init__(self, scv):
        """
        Constructeur de la classe StartSCVButton.
        
        Initialise le widget et associe l'objet SCV passé en paramètre à cet objet pour un usage ultérieur.
        
        Args:
            scv: L'objet SCV  qui sera démarré par ce bouton. Doit fournir une méthode `start`.
        """
        super().__init__()
        self.scv = scv  # Stocke la référence à l'objet SCV pour pouvoir l'appeler plus tard.
        self.initializeUI()  # Appel de la méthode d'initialisation de l'interface utilisateur.
        
    def initializeUI(self):
        """
        Prépare l'interface utilisateur du widget, en configurant les propriétés de base et en assemblant les composants UI.
        """
        # Définit les dimensions et la position du widget (largeur, hauteur, position X, position Y).
        self.setGeometry(100, 100, 200, 100)
        
        # Crée le bouton avec le texte indiqué et l'ajoute au widget.
        self.button = QPushButton("Activer CV")
        # Connecte le signal "clicked" du bouton à la méthode `onButtonClick`, qui sera appelée lorsque le bouton est cliqué.
        self.button.clicked.connect(self.onButtonClick)
        
        # Crée un layout vertical pour organiser les éléments UI à l'intérieur de ce widget.
        layout = QVBoxLayout()
        layout.addWidget(self.button)  # Ajoute le bouton au layout.
        self.setLayout(layout)  # Applique le layout au widget.
        
    def onButtonClick(self):
        """
        Méthode exécutée lorsque l'utilisateur clique sur le bouton. Elle déclenche le démarrage du processus SCV.
        
        Cette méthode fait appel à la méthode `start` de l'objet SCV associé à ce bouton, lançant ainsi le processus désigné.
        """
        self.scv.start()  # Déclenche le processus SCV en appelant sa méthode `start`.


        
class CreationButton(QWidget):
    """
    Ce widget représente un bouton permettant de lancer le processus de création de la carte.
    Il sert d'interface utilisateur pour démarrer une action spécifique liée à la génération ou la mise à jour de la carte dans l'application.
    
    Attributes:
        premap: Une référence à l'objet responsable de la gestion de la carte avant sa finalisation.
    """
    
    def __init__(self, premap):
        """
        Constructeur de la classe CreationButton.
        
        Initialise le widget avec l'objet de pré-carte fourni, le rendant prêt pour l'interaction utilisateur.
        
        Args:
            premap: L'objet responsable de la gestion de la carte avant sa création finale.
        """
        super().__init__()
        self.premap = premap  # Référence à l'objet de pré-carte pour les opérations de création.
        self.initializeUI()  # Initialisation de l'interface utilisateur.
        
    def initializeUI(self):
        """
        Configure l'interface utilisateur du bouton, incluant sa géométrie et les actions associées.
        """
        # Définit la taille et la position initiales du widget.
        self.setGeometry(100, 100, 200, 100)
        
        # Crée un nouveau bouton avec le texte indiqué.
        self.button = QPushButton("Créer Map")
        # Connecte le signal "clicked" à la méthode `onButtonClick` pour gérer le clic sur le bouton.
        self.button.clicked.connect(self.onButtonClick)
        
        # Configure le layout principal pour ce widget.
        layout = QVBoxLayout()
        layout.addWidget(self.button)  # Ajoute le bouton au layout.
        self.setLayout(layout)  # Applique le layout configuré au widget.
        
    def onButtonClick(self):
        """
        Méthode déclenchée par le clic sur le bouton, qui lance la création de la carte.
        
        Fait appel à la méthode `creation_final` de l'objet de pré-carte associé, démarrant ainsi le processus de création de la carte.
        """
        self.premap.creation_final()  # Déclenche la création finale de la carte à travers l'objet de pré-carte.


class TypeGenerationButton(QWidget):
    """
    Widget bouton qui permet de sélectionner le type de génération pour une action spécifique.
    Le type de génération est visualisé par la couleur du bouton, offrant une interface intuitive pour l'utilisateur.
    
    Attributes:
        lwindow: Référence à la fenêtre principale ou au widget parent qui contient ce bouton.
        type_generation: Un tuple contenant le nom du type de génération et la couleur associée.
    """
    
    def __init__(self, lwindow, type_generation):
        """
        Initialise le bouton de type de génération avec les paramètres spécifiés.
        
        Args:
            lwindow: La fenêtre principale ou le widget parent qui va contenir ce bouton.
            type_generation: Tuple contenant le nom du type de génération et sa couleur associée.
        """
        super().__init__()
        self.lwindow = lwindow
        self.type_generation = type_generation
        self.initializeUI()
        self.coloration(self.type_generation[1])  # Applique la couleur spécifiée au bouton.
        
    def initializeUI(self):
        """
        Configure l'interface utilisateur du bouton, y compris son apparence et ses dimensions.
        """
        self.setGeometry(100, 100, 200, 100)  # Définit la taille et la position du bouton.
        self.button = QPushButton(str(self.type_generation[0]))  # Crée le bouton avec le nom du type de génération.
        self.button.clicked.connect(self.onButtonClick)  # Connecte le signal "clicked" à la méthode de gestion.
        
        layout = QVBoxLayout()  # Crée un layout vertical pour organiser les éléments.
        layout.addWidget(self.button)  # Ajoute le bouton au layout.
        self.setLayout(layout)  # Applique le layout au widget.
        
    def onButtonClick(self):
        """
        Gestionnaire d'événements appelé lorsque le bouton est cliqué.
        
        Met à jour le type de génération sélectionné dans la fenêtre ou le widget parent.
        """
        self.lwindow.type_generation = self.type_generation  # Met à jour le type de génération dans le parent.
        
    def coloration(self, color):
        """
        Applique la couleur spécifiée au bouton, améliorant l'expérience utilisateur en offrant une indication visuelle.
        
        Args:
            color: La couleur à appliquer au bouton, spécifiée en tant que QColor.
        """
        # Créer des couleurs avec QColor
        background_color = color  # Bleu
        text_color = QColor(255, 255, 255)  # Blanc
        # Convertir QColor en chaîne de caractères pour la feuille de style
        background_color_str = background_color.name()
        text_color_str = text_color.name()

        # Appliquer les couleurs via les feuilles de style
        self.button.setStyleSheet(f"QPushButton {{background-color: {background_color_str}; color: {text_color_str};}}")
                                   
class RayonButton(QWidget):
    """
    Widget bouton pour ajuster le rayon (taille) d'une ellipse. Ce bouton permet d'incrémenter ou de décrémenter le rayon,
    offrant une interaction directe pour modifier la taille des éléments graphiques représentés sur la carte.
    
    Attributes:
        ellipse: Référence à l'objet ellipse dont le rayon doit être ajusté.
        coef: Coefficient d'ajustement qui détermine l'ampleur de la modification du rayon à chaque clic.
    """
    
    def __init__(self, ellipse, coef=0.1):
        """
        Initialise le bouton d'ajustement du rayon avec les paramètres spécifiés.
        
        Args:
            ellipse: L'objet ellipse à ajuster.
            coef: Coefficient d'ajustement du rayon (par défaut 0.1).
        """
        super().__init__()
        self.ellipse = ellipse  # Objet ellipse à ajuster.
        self.coef = coef  # Coefficient d'ajustement.
        self.initializeUI()  # Configuration de l'UI.
        
    def initializeUI(self):
        """
        Configure l'interface utilisateur du bouton, y compris son apparence, ses dimensions et l'action associée.
        """
        self.setGeometry(100, 100, 200, 100)  # Définit les dimensions et la position.
        self.button = QPushButton(f'ajouter {self.coef}', self)  # Texte du bouton reflétant le coefficient d'ajustement.
        
        self.button.clicked.connect(self.onButtonClick)  # Lie l'événement de clic à la méthode correspondante.
        
        layout = QVBoxLayout()  # Utilise un layout vertical pour organiser les éléments.
        layout.addWidget(self.button)  # Ajoute le bouton au layout.
        self.setLayout(layout)  # Applique le layout au widget.
        
    def onButtonClick(self):
        """
        Gestionnaire d'événements appelé lorsque le bouton est cliqué.
        
        Ajuste le rayon de l'ellipse associée selon le coefficient défini.
        """
        if self.ellipse is None: return  # Vérifie si l'ellipse est définie.
        self.ellipse.change_taille(500 * self.coef)  # Ajuste le rayon de l'ellipse.
        
    def changeEllipse(self, ellipse):
        """
        Permet de changer l'objet ellipse associé à ce bouton.
        
        Args:
            ellipse: La nouvelle ellipse à associer au bouton.
        """
        self.ellipse = ellipse  # Met à jour la référence à l'objet ellipse.

        
class SuppButton(QWidget):
    """
    Widget bouton pour supprimer une ellipse spécifique de la carte. Ce bouton offre une interaction directe
    pour retirer des éléments graphiques, améliorant ainsi la gestion des éléments présents sur la carte.
    
    Attributes:
        map: La carte contenant les éléments graphiques à gérer.
        ellipse: L'ellipse spécifique à supprimer lors de l'activation du bouton.
    """
    
    def __init__(self, map, ellipse):
        """
        Initialise le bouton de suppression avec les objets de carte et d'ellipse spécifiés.
        
        Args:
            map: La carte contenant l'ellipse.
            ellipse: L'ellipse à supprimer.
        """
        super().__init__()
        self.map = map  # La carte contenant l'ellipse.
        self.ellipse = ellipse  # L'ellipse à supprimer.
        self.initializeUI()  # Configuration de l'interface utilisateur.
        
    def initializeUI(self):
        """
        Configure l'interface utilisateur du bouton, y compris son apparence, ses dimensions et l'action de suppression associée.
        """
        self.setGeometry(100, 100, 200, 100)  # Dimensions et position du bouton.
        self.button = QPushButton("Supprimer", self)  # Création du bouton avec le texte "Supprimer".
        
        self.button.clicked.connect(self.onButtonClick)  # Connexion de l'événement de clic à la méthode de suppression.
        
        layout = QVBoxLayout()  # Organisation des éléments dans un layout vertical.
        layout.addWidget(self.button)  # Ajout du bouton au layout.
        self.setLayout(layout)  # Application du layout au widget.
        
    def onButtonClick(self):
        """
        Gestionnaire d'événements déclenché par le clic sur le bouton.
        
        Supprime l'ellipse spécifiée de la carte, si elle existe et appartient à la scène.
        """
        if self.ellipse is None: return  # Vérification de l'existence de l'ellipse.
        if self.ellipse and self.ellipse.scene():
            self.ellipse.scene().removeItem(self.ellipse)  # Suppression de l'ellipse de la scène.
            self.map.supprime_point(self.ellipse)  # Suppression de l'ellipse de la carte.
            self.ellipse = None  # Réinitialisation de la référence à l'ellipse.
        
    def changeEllipse(self, ellipse):
        """
        Met à jour l'ellipse associée à ce bouton pour permettre sa suppression.
        
        Args:
            ellipse: La nouvelle ellipse à associer pour une éventuelle suppression.
        """
        self.ellipse = ellipse  # Mise à jour de la référence à l'ellipse.
        
class ZoneButton(QWidget):
    """
    Widget permettant de définir des paramètres dans une zone spécifique, comme la création de points avec des caractéristiques définies par l'utilisateur.
    Cela pourrait inclure le rayon d'une ellipse, sa position, etc.
    
    Attributes:
        map: Référence à l'objet carte sur lequel les opérations seront effectuées.
        l: Largeur du widget (optionnel, valeur par défaut à 200).
        h: Hauteur du widget (optionnel, valeur par défaut à 80).
    """
    
    def __init__(self, map, l=200, h=80):
        """
        Initialise le widget ZoneButton avec les paramètres de la carte et les dimensions spécifiées.
        
        Args:
            map: L'objet carte associé à ce widget pour les opérations.
            l: Largeur du widget (par défaut 200).
            h: Hauteur du widget (par défaut 80).
        """
        super().__init__()
        self.map = map  # Référence à l'objet carte.
        self.setFixedSize(l, h * 2.5)  # Définit la taille fixe du widget basée sur les paramètres fournis.
        
        layout = QVBoxLayout()  # Crée un layout vertical.
        valeurs_layout = QHBoxLayout()  # Crée un layout horizontal pour les champs de saisie.
        
        # Initialisation des champs de saisie pour les paramètres de la zone.
        self.valeur_edits = []  # Liste pour stocker les QSpinBox correspondant à chaque paramètre.
        nom_boutons = ["RAYON", "X", "Y"]  # Noms des paramètres à définir.
        
        for nom in nom_boutons:
            label = QLabel(nom)  # Crée un label pour chaque paramètre.
            edit = QSpinBox()  # Crée un champ de saisie pour entrer la valeur du paramètre.
            edit.setMinimum(0)  # Définit la valeur minimale.
            edit.setMaximum(100)  # Définit la valeur maximale.
            valeurs_layout.addWidget(label)  # Ajoute le label au layout horizontal.
            valeurs_layout.addWidget(edit)  # Ajoute le champ de saisie au layout.
            self.valeur_edits.append(edit)  # Stocke le QSpinBox dans la liste pour un accès ultérieur.
        
        layout.addLayout(valeurs_layout)  # Ajoute le layout des champs de saisie au layout vertical principal.
        
        # Bouton pour soumettre les informations saisies par l'utilisateur.
        self.submit_button = QPushButton("Soumettre")
        self.submit_button.clicked.connect(self.afficher_informations)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)  # Applique le layout vertical au widget.
        
    def refresh_champ(self):
        """
        Réinitialise les champs de saisie après soumission pour permettre une nouvelle saisie.
        """
        for edit in self.valeur_edits:
            edit.setValue(0)  # Réinitialise la valeur de chaque QSpinBox à 0.
            
    def afficher_informations(self):
        """
        Collecte les informations des champs de saisie et les utilise pour effectuer une opération sur la carte.
        Bloque temporairement le bouton de soumission pour éviter les entrées multiples.
        """
        self.submit_button.setEnabled(False)  # Désactive le bouton de soumission.
        rayon = [edit.value() for edit in self.valeur_edits]  # Récupère les valeurs entrées par l'utilisateur.
        x, y, r = rayon  # Assigne les valeurs à des variables spécifiques.
        self.map.place_point(x, y, QColor(0, 255, 0), r)  # Utilise les valeurs pour placer un point sur la carte.
        
        self.refresh_champ()  # Réinitialise les champs de saisie pour une nouvelle saisie.
        self.submit_button.setEnabled(True)  # Réactive le bouton de soumission.

      
        
class LWindow(QWidget):
    def __init__(self):
        super().__init__()
        """
        Fenêtre principale de l'application, organisant et coordonnant les interactions entre les divers widgets et composants.
        Cette classe sert de point central pour l'affichage et la gestion de l'interface utilisateur, y compris la carte,
        les boutons d'action et la configuration des paramètres de génération des points.
        """
        
        self.setWindowTitle("Connexion")  # Titre de la fenêtre.
        
        # Initialisations des attributs principaux.
        self.coef = 1
        self.TAILLE = 100
        self.taille_population = 100
        self.cpt_scv = 0
        self.scv = SCV(self)
        self.res_scv = []
        self.liste_points = []  # Liste pour stocker les points créés par l'utilisateur.
        self.type_generation = ("Beta", QColor(0, 0, 255))  # Type de génération initial.
        
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
        Met à jour les références des ellipses sélectionnées dans les boutons qui nécessitent cette information.
        Cette méthode assure que les actions appliquées via les boutons affectent l'ellipse actuellement sélectionnée.
        """
        self.ellipse_up_B.changeEllipse(self.ellipse_select)
        self.ellipse_down_B.changeEllipse(self.ellipse_select)
        self.sup_B.changeEllipse(self.ellipse_select)
    
    def ellipse_touched(self, ellipse):
        """
        Gère l'événement de sélection (toucher) d'une ellipse sur la carte.
        Change la couleur de l'ellipse sélectionnée et met à jour la référence à l'ellipse sélectionnée pour les actions futures.
        
        Args:
            ellipse: L'ellipse qui a été touchée (sélectionnée) par l'utilisateur.
        """
        if ellipse == self.ellipse_select: return  # Ignore si l'ellipse sélectionnée est la même que celle déjà sélectionnée.
        
        # Réinitialise la couleur de l'ellipse précédemment sélectionnée si une nouvelle est sélectionnée.
        if self.ellipse_select is not None:
            self.ellipse_select.reinitialise_color()
        
        # Met à jour l'ellipse sélectionnée et change sa couleur pour indiquer la sélection.
        self.ellipse_select = ellipse
        self.ellipse_select.change_color(QColor(255, 255, 255))
        self.refersh_button()  # Met à jour les références dans les boutons concernés.
    
    def handleCompassClick(self, point):
        """
        Gère les clics sur le widget compass, permettant à l'utilisateur de placer un point sur la carte.
        Ce point peut représenter divers éléments selon le contexte de l'application.
        
        Args:
            point: Les coordonnées du point où l'utilisateur a cliqué sur le widget compass.
        """
        # Convertit le point de clic en coordonnées utilisables pour la carte et crée un point correspondant.
        scenePoint = self.compass.view.mapToScene(point)
        adjustedX = scenePoint.x() - 15
        adjustedY = scenePoint.y() - 15
        
        # Ouvre une fenêtre de dialogue pour la saisie supplémentaire de l'utilisateur, si nécessaire.
        self.openPopup()
        
        # Place le point sur la carte en utilisant les coordonnées ajustées et les informations de type de génération.
        p = self.compass.place_point(adjustedX, adjustedY, self.type_generation[1], 500*0.20, self.ellipse_touched)
        
        # Ajoute le point créé et ses informations associées à la liste des points pour une gestion future.
        self.liste_points.append((p, self.type_generation, self.taille_population))
    
    def openPopup(self):
        """
        Ouvre une boîte de dialogue permettant à l'utilisateur de saisir des informations supplémentaires, telles que la taille de la population.
        Les informations recueillies peuvent être utilisées pour des opérations ultérieures sur la carte ou les éléments qu'elle contient.
        """
        value, ok = QInputDialog.getInt(self, 'Saisie d\'un entier', 'Veuillez entrer la taille de la population :')
        if ok:
            self.taille_population = int(value)  # Met à jour la taille de la population avec la valeur saisie par l'utilisateur.
                
    def fonction_SCV(self,res):
        """
        Fonction lier avec SCV, permet de changer la taille du point en fonction de scv
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
        """
        Déclenche le processus final de création de la carte, utilisant les points et paramètres définis par l'utilisateur.
        Cette méthode peut générer une carte personnalisée basée sur les entrées utilisateurs collectées durant la session.
        """
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
        bd = Basedonnee.creer("Your Wolrd",500,True,map)
        ic(bd.window,"L window")
        bd.window.show()
        print("Fin")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LWindow()
    window.show()
    sys.exit(app.exec())
 