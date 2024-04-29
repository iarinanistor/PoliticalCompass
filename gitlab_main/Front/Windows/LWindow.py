from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QMainWindow
from PySide6.QtGui import QColor
from PySide6.QtCore import  Qt

from BaseDonnee.BaseDonnee import Basedonnee
from Back.Map import Map
from Back.Inteligent.Hand import SCV
from Front.Widgets.MapQT import PreMap
from Front.Widgets.ButonLWindow import StartSCVButton, SuppButton,ZoneButton,TypeGenerationButton,RayonButton,CreationButton,CustomInputDialog

#Importation de la consommation des fonctions utilisées
from calculs_emissions import emission_moyen_Map_3D, emission_moyen_Map_2D


class LWindow(QMainWindow):
    """
    Fenêtre principale de l'application, organisant et coordonnant les interactions entre les divers widgets et composants.
    Cette classe sert de point central pour l'affichage et la gestion de l'interface utilisateur, y compris la carte,
    les boutons d'action et la configuration des paramètres de génération des points.

    Attributes:
        coef (int): Coefficient pour l'ajustement de la taille des points.
        TAILLE (int): Dimension de la grille sur la carte.
        taille_population (int): Taille de la population pour certains calculs.
        cpt_scv (int): Compteur pour le SCV.
        res_scv (list): Résultats des interactions SCV.
        liste_points (list): Liste des points créés par l'utilisateur.
        type_generation (tuple): Type de génération initiale et couleur associée.
        ellipse_select (InteractiveEllipse, optional): Ellipse actuellement sélectionnée.
        compass (PreMap): Widget pour la visualisation de la carte.
        zone_button (ZoneButton): Bouton pour les paramètres de zone.
        ellipse_up_B, ellipse_down_B (RayonButton): Boutons pour ajuster le rayon de l'ellipse.
        sup_B (SuppButton): Bouton pour supprimer l'ellipse sélectionnée.
        cam_SCV (StartSCVButton): Bouton pour démarrer le SCV.
        beta, uniforme, expontiel, triangulaire (TypeGenerationButton): Boutons pour le type de génération.
        creebutton (CreationButton): Bouton pour la création de la carte.

    Méthodes:
        mousePressEvent: Émet un signal lorsque l'ellipse est cliquée, utile pour l'interaction avec l'interface.
        change_taille: Ajuste la taille de l'ellipse d'un delta spécifié, influençant la visualisation sur la carte.
        change_color: Modifie la couleur de l'ellipse pour visualiser différents états ou catégories.
        reinitialise_color: Réinitialise la couleur de l'ellipse à son état original, généralement après une sélection ou modification.
        handleCompassClick: Gère les clics sur le widget compass, permettant de placer un point sur la carte à l'emplacement cliqué.
        refersh_button: Met à jour les références des ellipses dans les boutons qui manipulent les ellipses pour assurer la cohérence des actions.
        ellipse_touched: Gère la sélection d'une ellipse, changeant sa couleur pour indiquer la sélection et mettant à jour la référence globale.
        openPopup: Ouvre un dialogue pour la saisie d'informations additionnelles, ajustant les paramètres basés sur les entrées utilisateur.
        creation_map: Génère la carte basée sur les entrées utilisateur accumulées pendant la session, incluant les points et configurations.
        creation_final_3D: Prépare et affiche la carte en mode 3D basée sur les configurations définies.
        creation_final_2D: Prépare et affiche la carte en mode 2D, ajustée selon les besoins spécifiques de l'utilisateur.

    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Connexion")  # Titre de la fenêtre.

        self.setStyleSheet("background-color: #333333;")
        
        # Initialisations des attributs principaux.
        self.coef = 1
        self.TAILLE = 100
        self.taille_population = 100
        self.cpt_scv = 0
        self.res_scv = []
        self.liste_points = []  # Liste pour stocker les points créés par l'utilisateur.
        self.type_generation = ("Beta", QColor(0, 0, 255))  # Type de génération initial.
        
        main_layout = QHBoxLayout()
        self.ellipse_select = None
        self.scv = SCV(self)

        self.main_content_layout = QVBoxLayout()

        self.main_content_layout_2 = QVBoxLayout()

        # Widget pour contenir les éléments du contenu principal
        self.main_content_widget = QWidget()
        self.main_content_widget.setLayout(self.main_content_layout)
        self.main_content_widget.setFixedHeight(450)
        main_layout.addWidget(self.main_content_widget, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=0)

        self.main_content_widget_2 = QWidget()
        self.main_content_widget_2.setLayout(self.main_content_layout_2)
        self.main_content_widget_2.setFixedSize(550, 925)
        main_layout.addWidget(self.main_content_widget_2, alignment=Qt.AlignTop | Qt.AlignRight, stretch=0)
          
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
        
        self.main_content_layout_2.addWidget(self.compass, alignment=Qt.AlignRight|Qt.AlignTop)
        self.main_content_layout.addWidget(self.zone_button,alignment=Qt.AlignRight)
        self.main_content_layout.addWidget(self.ellipse_up_B,alignment= Qt.AlignRight)
        self.main_content_layout.addWidget(self.ellipse_down_B,alignment=Qt.AlignRight)
        self.main_content_layout.addWidget(self.sup_B,alignment=Qt.AlignLeft)
        self.main_content_layout.addWidget(self.cam_SCV,alignment=Qt.AlignLeft)
        self.main_content_layout_2.addWidget(self.uniforme,alignment=Qt.AlignRight)
        self.main_content_layout_2.addWidget(self.beta,alignment=Qt.AlignRight)
        self.main_content_layout_2.addWidget(self.expontiel,alignment= Qt.AlignRight)
        self.main_content_layout_2.addWidget(self.triangulaire,alignment= Qt.AlignRight) 
        self.main_content_layout.addWidget(self.creebutton,alignment=Qt.AlignLeft)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.setGeometry(100, 100, 1250, 900)
        self.compass.clicked.connect(self.handleCompassClick)
        
    def refersh_button(self):
        """
        Actualise les références des ellipses sélectionnées dans les boutons qui nécessitent cette information.
        Cette méthode assure que les actions réalisées via les boutons concernent l'ellipse actuellement sélectionnée.
        """
        self.ellipse_up_B.changeEllipse(self.ellipse_select)
        self.ellipse_down_B.changeEllipse(self.ellipse_select)
        self.sup_B.changeEllipse(self.ellipse_select)
    
    def ellipse_touched(self, ellipse):
        """
        Gère la sélection d'une ellipse sur la carte. Cette méthode modifie la couleur de l'ellipse sélectionnée
        pour indiquer qu'elle est l'objet de l'interaction utilisateur et met à jour la référence interne pour les actions futures.

        Args:
            ellipse (InteractiveEllipse): L'ellipse qui a été sélectionnée par l'utilisateur.
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
        Traite les clics sur le widget compass, permettant à l'utilisateur de placer un point sur la carte à l'emplacement cliqué.
        Convertit le point de clic en coordonnées réelles sur la carte et crée un point correspondant.

        Args:
            point (QPoint): Le point où l'utilisateur a cliqué sur le widget compass.
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
        Ouvre une boîte de dialogue permettant à l'utilisateur de saisir des informations supplémentaires,
        telles que la taille de la population.
        Les informations recueillies peuvent être utilisées pour des opérations ultérieures sur la carte
        ou les éléments qu'elle contient.
        """
        # Création de la boîte de dialogue
        dialog = CustomInputDialog(self)

        # Paramètres nécessaires pour obtenir un entier via une boîte de dialogue
        value, ok = dialog.getInt()

        if ok:
            self.taille_population = value  # Met à jour la taille de la population avec la valeur saisie par l'utilisateur.


    def fonction_SCV(self,res):
        """
        Répond à l'interaction avec le SCV pour modifier la taille du point selon le résultat du SCV.
        Cette fonction permet d'ajuster dynamiquement les propriétés des points en fonction de leur
        performance ou pertinence évaluée par le SCV.

        Args:
            res (float): Le résultat de l'évaluation SCV, influençant le coefficient de taille du point.
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
        Génère la Map personnalisée en fonction des zone cree par l'utilisateur

        Returns:
            Map: L'objet généré avec tous les zones  des generations appliqués.
        """
        pop = [[None] * self.TAILLE for _ in range(self.TAILLE)]
        map = Map(None," personalisée ",[],pop,self.TAILLE ,self.TAILLE )
        print("l",self.liste_points)
        if(self.liste_points is None): raise ValueError(" il faut creer au moins une zone")
        for (p,type_generation,taille_population) in self.liste_points:
            x=int(p.get_x()/(500/self.TAILLE ))# met les coordonées dans une map de taille " self.taille"
            y=int(p.get_y()/(500/self.TAILLE ))
            r=int(p.get_rayon()/(500/self.TAILLE ))
            print(x,y,r,type_generation[0],taille_population, end = " ")
            map.generation_pers((x,y,r),type_generation[0],taille_population)
        return map 
    
    def creation_final_3D(self):
        """
        Prépare et affiche la carte finale en mode 3D. Cette méthode fait appel à `creation_map` pour générer
        la carte et la ferme pour passer à la visualisation 3D dans une nouvelle fenêtre de l'application.
        la visualisation 3D du compass peremet une meilleur visualisation des extremes.

        Utilise également base de données(BaseDonne) pour stocker et gérer les configurations de la carte.
        """
        map = self.creation_map()
        self.close()
        bd = Basedonnee.creer("Your Wolrd",100,True,map)
        bd.window.show()

        #Ajout de la consommation
        bd.ajoute_conso(emission_moyen_Map_3D)
    
    def creation_final_2D(self):
        """
        Prépare et affiche la carte finale en mode 2D. Cette méthode fait appel à `creation_map` pour générer
        la carte et la ferme pour passer à la visualisation 2D dans une nouvelle fenêtre de l'application.

        Utilise également base de données(BaseDonne) pour stocker et gérer les configurations de la carte.
        """
        map = self.creation_map()
        self.close()
        bd = Basedonnee.creer("Your Wolrd",100,False,map)
        bd.window.show()

        #Ajout de la consommation
        bd.ajoute_conso(emission_moyen_Map_2D)
