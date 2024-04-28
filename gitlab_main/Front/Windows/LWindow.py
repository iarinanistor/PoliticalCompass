import sys
from Back.Inteligent.Hand import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Front.Widgets.MapQT import PreMap
from Back.Map import *
from Back.Inteligent.Hand import SCV
from BaseDonnee.BaseDonnee import *
import logging
from icecream import ic
import time
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from PySide6.QtCore import QObject, QEvent

style_spinbox = """
            QSpinBox {
        color: #ffffff;  /* Texte blanc pour le contraste */
        background-color: #555555;  /* Fond légèrement plus clair que celui de l'application */
        border: 1px solid #777777;  /* Bordure subtile */
        font-family: 'Arial';  /* Assortir la police avec celle du QLabel */
        font-size: 14px;  /* Taille de police correspondante */
        padding: 4px;  /* Marge interne */
        }
        QSpinBox::up-button, QSpinBox::down-button {
            width: 20px;  /* Largeur des boutons */
            background-color: #666666;  /* Fond des boutons */
        }
        QSpinBox::up-arrow {
            width: 10px;  /* Largeur de la flèche */
            height: 10px;  /* Hauteur de la flèche */
            image: url('images/icons/cil-arrow-circle-top.png');  /* Image de la flèche */
        }
        QSpinBox::down-arrow {
            width: 10px;  /* Largeur de la flèche */
            height: 10px;  /* Hauteur de la flèche */
            image: url('images/icons/cil-arrow-circle-bottom.png');
        }
        """

class EventFilter(QObject):
    """
    Filtre d'événements personnalisé, principalement utilisé pour intercepter et gérer des événements de clic de souris
    spécifiques afin de contrôler le flux d'événements dans l'application.

    Cette classe est souvent utilisée pour éviter que des clics de souris non désirés ne déclenchent des actions inattendues
    ou pour limiter l'interaction avec certains composants de l'interface utilisateur.

    Méthodes:
        eventFilter: Surcharge la méthode eventFilter pour personnaliser le traitement des événements.
    """

    def eventFilter(self, watched, event):
        """
        Filtre les événements passant à travers le filtre d'événements. Les événements de clic de souris sont interceptés
        et ne sont pas propagés plus loin pour éviter des actions non désirées.

        Args:
            watched (QObject): L'objet sur lequel l'événement est observé.
            event (QEvent): L'événement qui est filtré.

        Returns:
            bool: True si l'événement doit être bloqué (ne pas être propagé), False pour permettre sa propagation.
        """
        # Filtrer les événements de clic de souris pour ne pas les propager.
        if event.type() == QEvent.MouseButtonPress:
            return True  # Indique que l'événement est traité.
        return False  # Permet la propagation des autres types d'événements.

    
    
class StartSCVButton(QWidget):
    """
    Widget responsable de l'activation d'un processus de vision par ordinateur (SCV) à travers un bouton interactif.

    Attributs:
        scv (object): Instance ou référence à l'objet qui implémente le processus SCV.
    
    Méthodes:
        initializeUI: Configure l'interface utilisateur du bouton, y compris ses propriétés esthétiques et fonctionnelles.
        eventFilter: Filtre les événements pour créer des animations et afficher des info-bulles.
        onButtonClick: Déclenche le processus SCV lorsque le bouton est cliqué.
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
        self.button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50; /* Green */
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
        
        # Ajout du tooltip
        self.button.setToolTip("Cliquez pour activer le système de vision par ordinateur.")

        # Connecte le signal "clicked" du bouton à la méthode `onButtonClick`, qui sera appelée lorsque le bouton est cliqué.
        self.button.clicked.connect(self.onButtonClick)
        
        # Crée un layout vertical pour organiser les éléments UI à l'intérieur de ce widget.
        layout = QVBoxLayout()
        layout.addWidget(self.button)  # Ajoute le bouton au layout.

        # Animation setup
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.button.installEventFilter(self)

        self.setLayout(layout)  # Applique le layout au widget.
        self.setFixedSize(100, 50)

    def eventFilter(self, obj, event):
        """
        Filtre et traite les événements pour créer des animations dynamiques et des interactions enrichies avec l'interface.
        """
        if obj is self.button:
            if event.type() == QEvent.Enter:
                QToolTip.showText(QCursor.pos(), self.button.toolTip(), self.button)
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    -1, 15,
                    max(282, currentGeometry.width() + 20), max(60, currentGeometry.height() + 10)))
                self.anim.start()
            elif event.type() == QEvent.Leave:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    9, 20,
                    max(282, currentGeometry.width() - 20), max(60, currentGeometry.height() - 10)))
                self.anim.start()
        return super().eventFilter(obj, event)
        
    def onButtonClick(self):
        """
        Méthode exécutée lorsque l'utilisateur clique sur le bouton. Elle déclenche le démarrage du processus SCV.
        
        Cette méthode fait appel à la méthode `start` de l'objet SCV associé à ce bouton.
        """
        self.scv.start()  # Déclenche le processus SCV en appelant sa méthode `start`.

class MapTypeDialog(QDialog):
    """
    Boîte de dialogue pour sélectionner le type de carte à afficher, soit en 3D soit en 2D.
    
    Attributs:
        mapType (str): Type de carte sélectionné par l'utilisateur ('3D' ou '2D').
    
    Méthodes:
        setupUI: Configure l'interface utilisateur de la boîte de dialogue, incluant les boutons et leurs styles.
        selectMapType: Définit le type de carte sélectionné et ferme la boîte de dialogue.
    """

    def __init__(self, parent=None):
        """
        Initialise la boîte de dialogue avec un titre et une taille fixe, et prépare l'interface utilisateur.
        
        Args:
            parent (QWidget): Widget parent de la boîte de dialogue.
        """

        super().__init__(parent)
        self.setWindowTitle("Choix du type de map")
        self.setFixedSize(400, 200)  # Taille fixe pour la boîte de dialogue
        self.mapType = None
        self.setupUI()

    def setupUI(self):
        """
        Prépare et organise les composants de l'interface utilisateur, notamment les boutons pour choisir le type de carte.
        """
        layout = QVBoxLayout()
        self.map3DButton = QPushButton("Map 3D")
        self.map2DButton = QPushButton("Map 2D")
        self.loadingLabel_3d = QLabel("Chargement de la planète...", self)  # Message temporaire
        self.loadingLabel_3d.setFixedSize(400,200)
        self.loadingLabel_2d = QLabel("Chargement de la carte...", self)  # Message temporaire
        self.loadingLabel_2d.setFixedSize(400,200)

        # Appliquer des styles CSS aux boutons
        button_style = """
        QPushButton {
            font-size: 18px;
            font-weight: bold;
            color: white;
            border: 2px solid #5F9EA0;
            border-radius: 15px;
            padding: 15px 32px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #2193b0, stop:1 #6dd5ed);
            margin: 10px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #6dd5ed, stop:1 #2193b0);
        }
        QPushButton:pressed {
            background-color: #1E90FF;
        }
        """

        self.map3DButton.setStyleSheet(button_style)
        self.map2DButton.setStyleSheet(button_style)

        layout.addWidget(self.map3DButton)
        layout.addWidget(self.map2DButton)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        # Style pour la boîte de dialogue
        self.setStyleSheet("""
        QDialog {
            background-color: #333333;
            border: 2px solid #444444;
            border-radius: 10px;
        }
        """)

        self.map3DButton.clicked.connect(lambda: self.selectMapType("3D"))
        self.map2DButton.clicked.connect(lambda: self.selectMapType("2D"))

        # Configuration du QLabel pour le GIF
        self.loadingLabel_3d.setAlignment(Qt.AlignCenter)
        movie_3d = QMovie("images/icons/gif_planete.gif")
        movie_3d.setScaledSize(self.loadingLabel_3d.size())  # Adapter la taille du GIF
        self.loadingLabel_3d.setMovie(movie_3d)
        if not movie_3d.isValid():
            print("Erreur de chargement du GIF")  # Affiche un message d'erreur si le GIF ne peut pas être chargé
        else:
            movie_3d.start()
        self.loadingLabel_3d.hide()  # Cacher le QLabel jusqu'au clic sur le bouton

        # Configuration du QLabel pour le GIF
        self.loadingLabel_2d.setAlignment(Qt.AlignCenter)
        movie_2d = QMovie("images/icons/gif_carte.gif")
        movie_2d.setScaledSize(self.loadingLabel_2d.size())  # Adapter la taille du GIF
        self.loadingLabel_2d.setMovie(movie_2d)
        if not movie_2d.isValid():
            print("Erreur de chargement du GIF")  # Affiche un message d'erreur si le GIF ne peut pas être chargé
        else:
            movie_2d.start()
        self.loadingLabel_2d.hide()  # Cacher le QLabel jusqu'au clic sur le bouton

    def selectMapType(self, type):
        """
        Enregistre le type de carte sélectionné et ferme la boîte de dialogue en affichant un gif.
        
        Args:
            type (str): Type de carte sélectionné ('3D' ou '2D').
        """
        self.mapType = type
        if type == "3D":
            self.map2DButton.hide()
            self.map3DButton.hide()
            self.setWindowTitle("Préparation de la planète...")
            self.loadingLabel_3d.show()  # Afficher le GIF
            QTimer.singleShot(4000, self.accept)  # Simuler un chargement et fermer la dialogue après 4 secondes
        else:
            self.map2DButton.hide()
            self.map3DButton.hide()
            self.loadingLabel_2d.show()  # Afficher le GIF
            self.setWindowTitle("Préparation de la carte...")
            QTimer.singleShot(4000, self.accept)  # Simuler un chargement et fermer la dialogue après 4 secondes

        
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
        self.button.setStyleSheet("""
    QPushButton {
        background-color: #008CBA; /* Blue */
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
    }
    QPushButton:hover {
        background-color: #007ba7;
    }
""")
        # Connecte le signal "clicked" à la méthode `onButtonClick` pour gérer le clic sur le bouton.
        self.button.clicked.connect(self.onButtonClick)
        
        # Configure le layout principal pour ce widget.
        layout = QVBoxLayout()
        layout.addWidget(self.button)  # Ajoute le bouton au layout.

        # Animation setup
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.button.installEventFilter(self)

        self.setLayout(layout)  # Applique le layout configuré au widget.

    def eventFilter(self, obj, event):
        if obj is self.button:
            if event.type() == QEvent.Enter:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    -1, 15,
                    max(282, currentGeometry.width() + 20), max(60, currentGeometry.height() + 10)))
                self.anim.start()
            elif event.type() == QEvent.Leave:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    9, 20,
                    max(282, currentGeometry.width() - 20), max(60, currentGeometry.height() - 10)))
                self.anim.start()
        return super().eventFilter(obj, event)
        
    def onButtonClick(self):
        """
        Méthode appelée lors du clic sur le bouton. Ouvre une boîte de dialogue pour sélectionner le type de carte,
        puis initie le processus de création de la carte sélectionnée.
        """
        if not self.premap.liste_points:  # Vérifie si la liste des points est vide
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Aucun point n'a été ajouté sur la carte. Veuillez ajouter des points avant de continuer.")
            msgBox.setWindowTitle("Erreur")
            msgBox.setStyleSheet("""
        QMessageBox {
            background-color: #333333;
            color: #000000;  /* Couleur du texte noir pour une lecture facile */
            font-family: 'Calibri', 'Arial';
            font-size: 15px;
            font-weight: bold;
        }
        QLabel {
            color: white;
        }
        QPushButton {
            color: #ffffff;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00adee, stop:1 #0078d4); /* Dégradé bleu vif */
            border: 2px solid #aaaaaa;
            border-radius: 5px;
            padding: 6px 24px;
            font-size: 13px;
            min-width: 80px;
            text-align: center;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1ab2ff, stop:1 #008ae6); /* Bleu plus clair au survol */
            border-color: #cccccc;
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #006ac1, stop:1 #005ba1); /* Bleu foncé lorsqu'appuyé */
            border-color: #bbbbbb;
        }
    """)
            msgBox.exec()
            return  # Arrête la fonction ici, donc ne continue pas à exécuter le dialogue ou la création de la map
        

        dialog = MapTypeDialog(self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            mapType = dialog.mapType  # Récupère le type de map sélectionné
            # Lancer la barre de progression ici
            progressDialog = QProgressDialog(f"Création de la carte {mapType} en cours...", "Annuler", 0, 100, self)
            progressDialog.setAutoClose(True)
            progressDialog.setMinimumDuration(0)
            progressDialog.setWindowModality(Qt.WindowModal)
            progressDialog.setWindowTitle("Progression de la création de la carte")
        
            progressDialog.setStyleSheet("""
                QProgressDialog {
                    border: 2px solid grey;
                    border-radius: 5px;
                    background-color: #333333; /* Dark Grey Background */
                }
                QProgressDialog QLabel {
                    color: white; /* Green-Yellow text */
                }
                QProgressBar {
                    border: 1px solid #006400; /* Dark Green */
                    border-radius: 5px;
                    background-color: #555555;
                    height: 20px;
                    text-align: center;
                    color: white;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #98FB98, stop:1 #008000);
                    border-radius: 5px;
                }
                QPushButton {
                    background-color: #FF6347; /* Tomato Red */
                    color: white;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #FF4500; /* OrangeRed */
                }
            """)
            
            for i in range(0, 101):
                progressDialog.setValue(i)
                QCoreApplication.processEvents()
                if progressDialog.wasCanceled():
                    break
                time.sleep(0.05)

            if progressDialog.wasCanceled():
                print("Création de la carte annulée.")
                return  # Ne lance pas l'application si annulé.

            progressDialog.setValue(100)  # S'assure que la barre atteint 100% si non annulé.

            if not progressDialog.wasCanceled():
                if mapType == "3D":
                    self.premap.creation_final_3D()  # Lance la création de la carte si non annulé.
                else: self.premap.creation_final_2D()


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

        # Animation setup
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.button.installEventFilter(self)

        self.setLayout(layout)  # Applique le layout au widget.

    def eventFilter(self, obj, event):
        """
        Filtre les événements pour le bouton pour animer à l'entrée et à la sortie de la souris.
        """
        if obj is self.button:
            if event.type() == QEvent.Enter:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    -1, 15,
                    max(282, currentGeometry.width() + 20), max(60, currentGeometry.height() + 10)))
                self.anim.start()
            elif event.type() == QEvent.Leave:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    9, 18,
                    max(282, currentGeometry.width() - 20), max(60, currentGeometry.height() - 10)))
                self.anim.start()
        return super().eventFilter(obj, event)
        
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
        base_color = color.name()
        gradient_start = base_color
        gradient_end = QColor(base_color).lighter(120).name()
        
        self.button.setStyleSheet(f"""
        QPushButton {{
            background-color: {base_color};
            color: white;
            border: 2px solid {QColor(base_color).darker(150).name()};
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {gradient_start}, stop:1 {gradient_end});
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {gradient_end}, stop:1 {gradient_start});
        }}
        QPushButton:pressed {{
            border-style: inset;
        }}
        """)
                                   
class RayonButton(QWidget):
    """
    Widget bouton pour ajuster le rayon (taille) d'une ellipse. Ce bouton permet d'incrémenter ou de décrémenter le rayon,
    offrant une interaction directe pour modifier la taille des éléments graphiques représentés sur une carte ou autre interface graphique.
    
    Attributes:
        ellipse (InteractiveEllipse): Référence à l'objet ellipse dont le rayon doit être ajusté.
        coef (float): Coefficient d'ajustement qui détermine l'ampleur de la modification du rayon à chaque clic.
    """
    
    def __init__(self, ellipse, coef=0.1):
        """
        Initialise le bouton d'ajustement du rayon avec les paramètres spécifiés.
        
        Args:
            ellipse (InteractiveEllipse): L'objet ellipse à ajuster.
            coef (float): Coefficient d'ajustement du rayon, spécifiant combien le rayon est modifié à chaque clic (par défaut 0.1).
        """
        super().__init__()
        self.ellipse = ellipse  # Objet ellipse à ajuster.
        self.coef = coef  # Coefficient d'ajustement.
        self.initializeUI()  # Configuration de l'UI.
        
    def initializeUI(self):
        """
        Configure l'interface utilisateur du bouton, y compris son apparence, ses dimensions et l'action associée à un clic.
        Définit également des styles et des animations pour améliorer l'interactivité visuelle.
        """
        self.setGeometry(100, 100, 200, 100)  # Définit les dimensions et la position.
        self.button = QPushButton(f'ajouter {self.coef}', self)  # Texte du bouton reflétant le coefficient d'ajustement.

        self.button.setStyleSheet("""
    QPushButton {
        background-color: #f44336; /* Red */
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
    }
    QPushButton:hover {
        background-color: #da190b;
    }
""")
        
        self.button.clicked.connect(self.onButtonClick)  # Lie l'événement de clic à la méthode correspondante.
        
        layout = QVBoxLayout()  # Utilise un layout vertical pour organiser les éléments.
        layout.addWidget(self.button)  # Ajoute le bouton au layout.

        # Animation setup
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.button.installEventFilter(self)
        self.setLayout(layout)  # Applique le layout au widget.

    def eventFilter(self, obj, event):
        """
        Filtre les événements pour appliquer des animations sur le bouton lors de l'interaction utilisateur.
        
        Args:
            obj (QObject): L'objet qui reçoit l'événement.
            event (QEvent): L'événement qui est traité.
        
        Returns:
            bool: True si l'événement est traité, False sinon.
        """
        # Animation pour agrandir et rétrécir le bouton lors du survol.
        if obj is self.button:
            if event.type() == QEvent.Enter:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    -1, 15,
                    max(282, currentGeometry.width() + 20), max(60, currentGeometry.height() + 10)))
                self.anim.start()
            elif event.type() == QEvent.Leave:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    9, 20,
                    max(282, currentGeometry.width() - 20), max(60, currentGeometry.height() - 10)))
                self.anim.start()
        return super().eventFilter(obj, event)
        
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
            ellipse (Ellipse): La nouvelle ellipse à associer au bouton.
        """
        self.ellipse = ellipse  # Met à jour la référence à l'objet ellipse.

        
class SuppButton(QWidget):
    """
    Widget bouton pour supprimer une ellipse spécifique sur une interface graphique. Ce bouton offre un moyen direct
    de retirer des éléments graphiques, ce qui améliore la gestion des objets affichés sur la carte.
    
    Attributes:
        map (PreMap): La scène graphique où les éléments sont gérés.
        ellipse (QGraphicsEllipseItem): L'ellipse à supprimer lors de l'activation du bouton.
    """
    
    def __init__(self, map, ellipse):
        """
        Initialise le bouton de suppression avec les références à la scène graphique et à l'ellipse ciblée.
        
        Args:
            map (PreMap): La scène qui contient l'ellipse.
            ellipse (InteractiveEllipse): L'ellipse spécifique à supprimer.
        """
        super().__init__()
        self.map = map  # La carte contenant l'ellipse.
        self.ellipse = ellipse  # L'ellipse à supprimer.
        self.initializeUI()  # Configuration de l'interface utilisateur.
        
    def initializeUI(self):
        """
        Configure l'interface utilisateur du bouton, incluant son apparence et l'action associée au clic.
        Définit les styles QSS pour le bouton et initialise les animations pour une interaction dynamique.
        """
        self.setGeometry(100, 100, 200, 100)  # Dimensions et position du bouton.
        self.button = QPushButton("Supprimer", self)  # Création du bouton avec le texte "Supprimer".
        self.button.setStyleSheet("""
    QPushButton {
        background-color: #555555; /* Dark Grey */
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
    }
    QPushButton:hover {
        background-color: #444444;
    }
""")
        
        self.button.clicked.connect(self.onButtonClick)  # Connexion de l'événement de clic à la méthode de suppression.
        
        layout = QVBoxLayout()  # Organisation des éléments dans un layout vertical.
        layout.addWidget(self.button)  # Ajout du bouton au layout.

        # Animation setup
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.button.installEventFilter(self)

        self.setLayout(layout)  # Application du layout au widget.

    def eventFilter(self, obj, event):
        """
        Filtre les événements pour appliquer des animations au bouton lors d'interactions spécifiques (entrée et sortie de la souris).
        
        Args:
            obj (QObject): L'objet qui reçoit l'événement.
            event (QEvent): L'événement qui est traité.
        
        Returns:
            bool: Indique si l'événement a été traité ici.
        """
        # Gestion de l'animation pour agrandir ou réduire le bouton lors du survol par la souris.
        if obj is self.button:
            if event.type() == QEvent.Enter:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    -1, 15,
                    max(282, currentGeometry.width() + 20), max(60, currentGeometry.height() + 10)))
                self.anim.start()
            elif event.type() == QEvent.Leave:
                currentGeometry = self.button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    9, 20,
                    max(282, currentGeometry.width() - 20), max(60, currentGeometry.height() - 10)))
                self.anim.start()
        return super().eventFilter(obj, event)
        
    def onButtonClick(self):
        """
        Gestionnaire d'événements déclenché par un clic sur le bouton. Supprime l'ellipse spécifiée de la scène, si elle est présente.
        Réinitialise également la référence à l'ellipse pour éviter les erreurs de référence
        """
        if self.ellipse is None: return  # Vérification de l'existence de l'ellipse.
        if self.ellipse and self.ellipse.scene():
            self.ellipse.scene().removeItem(self.ellipse)  # Suppression de l'ellipse de la scène.
            self.map.supprime_point(self.ellipse)  # Suppression de l'ellipse de la carte.
            self.ellipse = None  # Réinitialisation de la référence à l'ellipse.
        
    def changeEllipse(self, ellipse):
        """
        Permet de changer l'ellipse associée à ce bouton. Utilisé pour rediriger les actions vers une nouvelle ellipse.
        
        Args:
            ellipse (InteractiveEllipse): La nouvelle ellipse à associer pour suppression future.
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
            label.setStyleSheet("""QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 12px;
            }""")
            edit = QSpinBox()  # Crée un champ de saisie pour entrer la valeur du paramètre.
            edit.setStyleSheet(style_spinbox)
            edit.setMinimum(0)  # Définit la valeur minimale.
            edit.setMaximum(100)  # Définit la valeur maximale.
            valeurs_layout.addWidget(label)  # Ajoute le label au layout horizontal.
            valeurs_layout.addWidget(edit)  # Ajoute le champ de saisie au layout.
            self.valeur_edits.append(edit)  # Stocke le QSpinBox dans la liste pour un accès ultérieur.
        
        layout.addLayout(valeurs_layout)  # Ajoute le layout des champs de saisie au layout vertical principal.
        
        # Bouton pour soumettre les informations saisies par l'utilisateur.
        self.submit_button = QPushButton("Soumettre")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                border: 1px solid #3C9F40;
                margin: 4px 2px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #397d34;
            }
        """)
        self.submit_button.clicked.connect(self.afficher_informations)
        layout.addWidget(self.submit_button)

        # Animation setup
        self.anim = QPropertyAnimation(self.submit_button, b"geometry")
        self.submit_button.installEventFilter(self)
        
        self.setLayout(layout)  # Applique le layout vertical au widget.

    def eventFilter(self, obj, event):
        if obj is self.submit_button:
            if event.type() == QEvent.Enter:
                currentGeometry = self.submit_button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    -1, 38,
                    max(282, currentGeometry.width() + 20), max(60, currentGeometry.height() + 10)))
                self.anim.start()
            elif event.type() == QEvent.Leave:
                currentGeometry = self.submit_button.geometry()
                self.anim.setDuration(200)
                self.anim.setEndValue(QRect(
                    9, 43,
                    max(282, currentGeometry.width() - 20), max(48, currentGeometry.height() - 10)))
                self.anim.start()
        return super().eventFilter(obj, event)
        
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

class CustomInputDialog(QDialog):
    """
    Dialogue personnalisé pour la saisie d'un entier par l'utilisateur. Ce dialogue est configuré pour recueillir
    un nombre entier avec des contraintes spécifiques, servant généralement à définir des valeurs telles que la taille d'une population
    dans des simulations ou des analyses.

    Attributes:
        value (int or None): Stocke la valeur entière saisie par l'utilisateur, accessible après la fermeture du dialogue.
    """
    def __init__(self, parent=None):
        """
        Initialise le dialogue en définissant le titre de la fenêtre et en appelant la méthode de configuration de l'interface.
        
        Args:
            parent (QWidget, optional): Widget parent de ce dialogue. Default is None.
        """
        super().__init__(parent)
        self.setWindowTitle("Saisie d'un entier")
        self.setupUI()
        self.value = None

    def setupUI(self):
        """
        Configure l'interface utilisateur du dialogue, incluant les widgets pour la saisie, les boutons d'action,
        et leurs styles respectifs.
        """
        layout = QVBoxLayout()

        label = QLabel("Veuillez entrer la taille de la population :")
        label.setStyleSheet("color: white;")

        self.spinBox = QSpinBox(self)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(2000000)
        self.spinBox.setStyleSheet(style_spinbox)

        okButton = QPushButton("OK")
        okButton.setStyleSheet("background-color: #1E90FF; color: white;")
        okButton.clicked.connect(self.accept)

        cancelButton = QPushButton("Annuler")
        cancelButton.setStyleSheet("background-color: #555555; color: white;")
        cancelButton.clicked.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(self.spinBox)
        layout.addWidget(okButton)
        layout.addWidget(cancelButton)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #333333;")

    def getInt(self):
        """
        Affiche le dialogue et retourne la valeur saisie et un booléen indiquant si l'opération est acceptée ou annulée.
        
        Returns:
            tuple(int,bool): Contient l'entier saisie et un booléen (True si accepté, False si annulé).
        """
        if self.exec() == QDialog.Accepted:
            return self.spinBox.value(), True
        return 0, False
      
        
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

 