import sys
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QComboBox, QMessageBox
from Front.Widgets.Boutons import *
from PySide6.QtGui import QIcon, QFont, QPixmap
from Back.Inteligent.SLCV import SLCV
from Tournoi.TreeView import Tournoi
import logging

#Importation de la consommation des fonctions utilisées
from calculs_emissions import emission_moyen_ouverture_menu_lat, emission_moyen_fermeture_menu_lat, emission_moyen_ouverture_menu_lat2, emission_moyen_fermeture_menu_lat2, emission_moyen_bouton_vote_ouverture, emission_moyen_bouton_vote_fermeture

# Configuration du logger
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Définition des commandes avec leur valeur
data_set_commands  = { # data set pour le numero de commandes 
    "lance borda": 1,
    "lance copeland": 2,
    "lance pluralité": 3,
    "lance STV": 4,
    "lance approbation": 5,
    "génère un candidats": 6,
    "Jenner" :6,
    
}
data_set_preProcessing = { # data set pour pouvoir regroup les commande par classe 
    "lance": 1,
    "génère": 2,
    "Jenner":2
}

class TournamentOptionsDialog(QDialog):
    def __init__(self, bd):
        super().__init__()
        self.bd = bd
        self.setWindowTitle("Options de Tournoi")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()
        logging.info("Dialogue des options de tournoi initialisé.")

    def setup_ui(self):
        layout = QVBoxLayout()

        # Définir la couleur de fond du dialogue
        self.setStyleSheet("""
            QDialog {
                background-color: #003366;  /* Dark blue background */
                color: #ffffff;  /* White text for better readability */
            }""")

        # Styles pour les boutons individuels
        simulate_button_style = """
            QPushButton {
                font: bold 14px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 5px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """

        cheater_button_style = """
            QPushButton {
                font: bold 14px;
                border: 2px solid #FF9800;
                border-radius: 10px;
                padding: 5px;
                background-color: #FF9800;
                color: white;
            }
            QPushButton:hover {
                background-color: #FFB74D;
            }
            QPushButton:pressed {
                background-color: #F57C00;
            }
        """

        confirm_button_style = """
            QPushButton {
                font: bold 14px;
                border: 2px solid #2196F3;
                border-radius: 10px;
                padding: 5px;
                background-color: #2196F3;
                color: white;
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
            QPushButton:pressed {
                background-color: #1976D2;
            }
        """

        # Bouton pour simuler le tournoi
        simulate_button = BoutonTournoi(self.bd)
        simulate_button.setStyleSheet(simulate_button_style)
        layout.addWidget(simulate_button)

        # Bouton pour inclure un tricheur
        cheater_button = QPushButton("Inclure un tricheur")
        cheater_button.setStyleSheet(cheater_button_style)
        cheater_button.clicked.connect(self.load_candidates)
        layout.addWidget(cheater_button)

        # ComboBox pour choisir un tricheur (non visible initialement)
        self.cheater_combo = QComboBox()
        self.cheater_combo.setStyleSheet("""
            QComboBox {
                font: 14px;
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: #616161;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(images/icons/cil-down-arrow.png);
            }
        """)
        self.cheater_combo.setVisible(False)
        layout.addWidget(self.cheater_combo)

        # Bouton pour confirmer le tricheur sélectionné
        confirm_button = QPushButton("Confirmer le tricheur")
        confirm_button.setStyleSheet(confirm_button_style)
        confirm_button.clicked.connect(self.confirm_cheater)
        confirm_button.setVisible(False)
        self.confirm_button = confirm_button
        layout.addWidget(confirm_button)
        
        self.setLayout(layout)
        logging.debug("Interface utilisateur du dialogue des options configurée.")

    def load_candidates(self):
        if len(self.bd.map.liste_electeur) > 1:
            if not self.cheater_combo.isVisible():
                candidates = self.bd.map.liste_electeur
                self.cheater_combo.clear()
                for candidate in candidates:
                    self.cheater_combo.addItem(f"{Candidat.nom(candidate)} {Candidat.prenom(candidate)}", candidate)
                self.cheater_combo.setVisible(True)
                self.confirm_button.setVisible(True)
            else:
                self.cheater_combo.setVisible(False)
                self.confirm_button.setVisible(False)
        else:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Erreur")
            error_msg.setText("Pas assez de candidats pour inclure un tricheur.")
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setStyleSheet("QLabel { color: white; } QPushButton { color: black; }")
            error_msg.exec_()

    def confirm_cheater(self):
        selected_candidate = self.cheater_combo.currentData()
        if selected_candidate:
            self.tr = Tournoi(self.bd.map, self.bd.map.liste_electeur)
            won = self.tr.fait_gagner(selected_candidate)
            self.tr.view.update()  # Nécessaire pour actualiser l'affichage

            # Créer et configurer QMessageBox pour afficher le résultat avec une image personnalisée
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Résultat du Tournoi")
            if won:
                msg_box.setText("Le tricheur a gagné le tournoi!")
                icon_path = "images/icons/winner.png"
            else:
                msg_box.setText("Le tricheur a perdu le tournoi.")
                icon_path = "images/icons/perdant.png"

            # Ajouter une image avec QLabel à la QMessageBox
            icon_label = QLabel(msg_box)
            msg_box.setStyleSheet("""QLabel {
                color: white;
            }
            """)
            icon_label.setPixmap(QPixmap(icon_path))
            icon_label.setScaledContents(True)
            icon_label.setMaximumSize(32, 32)  # Taille de l'image

            # Positionner l'image dans la boîte de dialogue
            msg_box.layout().addWidget(icon_label, 0, 0, 1, 1, Qt.AlignLeft)
            msg_box.setIcon(QMessageBox.NoIcon)  # Désactiver l'icône par défaut

            # Afficher la boîte de dialogue
            msg_box.exec_()

class SideMenu(QMainWindow):
    def __init__(self, bd, Blongeur=300, Bhauteur=40, tailleMap=500):
        """
        Constructeur de la classe SideMenu.

        Args:
            bd (object): Objet représentant une base de données.
            Blongeur (int): Longueur des boutons. Par défaut, 300.
            Bhauteur (int): Hauteur des boutons. Par défaut, 40.
            tailleMap (int): Taille de la carte. Par défaut, 500.
        """
        super().__init__()

        self.bd = bd
        logging.info("Menu lateral initialise avec la base de donnees.")
        ic(self.bd," MenuLateral")
        self.Blongeur = Blongeur
        self.Bhauteur = Bhauteur
        self.tailleMap = tailleMap

        # Layout principal
        main_layout = QHBoxLayout()
        
        # Contenu principal
        self.main_content_layout = QVBoxLayout()

        # Widgets pour les sidebars
        self.sidebar_layout_1 = QVBoxLayout()
        self.sidebar_widget_1 = QWidget()
        self.sidebar_widget_1.setLayout(self.sidebar_layout_1)
        self.sidebar_widget_1.setMaximumWidth(0)
 
        self.sidebar_layout_2 = QVBoxLayout()
        self.sidebar_widget_2 = QWidget()
        self.sidebar_widget_2.setLayout(self.sidebar_layout_2)
        self.sidebar_widget_2.setMaximumWidth(0)

        main_layout.addWidget(self.sidebar_widget_1)
        main_layout.addWidget(self.sidebar_widget_2)

        # Widget pour contenir les éléments du contenu principal
        self.main_content_widget = QWidget()
        self.main_content_widget.setLayout(self.main_content_layout)
        self.main_content_widget.setFixedHeight(200)
        main_layout.addWidget(self.main_content_widget, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=0)

        style_sidebar_button = """QPushButton {
    border: 1px solid #555;
    border-radius: 10px;
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #6a1b9a, stop: 1 #ab47bc);  /* Dégradé de violet pour un look plus dynamique */
    color: white;
    padding: 5px;
    min-width: 100px;
    min-height: 40px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #ec407a, stop: 1 #f06292);  /* Dégradé de rose lors du survol pour une sensation plus interactive */
}
QPushButton:pressed {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #42a5f5, stop: 1 #64b5f6);  /* Bleu lorsqu'il est pressé pour un feedback visuel clair */
}"""

        # Bouton pour ouvrir/fermer la sidebar 1 (Menu)
        self.sidebar_menu_button = QPushButton()
        self.sidebar_menu_button.setIcon(QIcon("images/icons/icon_menu.png"))
        self.sidebar_menu_button.setStyleSheet(style_sidebar_button)
        self.sidebar_menu_button.setFixedSize(20, self.Bhauteur)
        self.sidebar_menu_button.clicked.connect(self.toggle_menu_sidebar)
        self.sidebar_menu_button.setToolTip("Menu")
        self.main_content_layout.addWidget(self.sidebar_menu_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Bouton pour ouvrir/fermer la sidebar 2 (Statistiques)
        self.sidebar_stats_button = QPushButton()
        self.sidebar_stats_button.setIcon(QIcon("images/icons/cil-chart.png"))
        self.sidebar_stats_button.setStyleSheet(style_sidebar_button)
        self.sidebar_stats_button.setFixedSize(20, self.Bhauteur)
        self.sidebar_stats_button.clicked.connect(self.toggle_stats_sidebar)
        self.sidebar_stats_button.setToolTip("Statistiques")
        self.main_content_layout.addWidget(self.sidebar_stats_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        # Bouton pour activer la commande vocale
        self.voc_button = QPushButton()
        self.voc_button.setIcon(QIcon("images/icons/cil-voice-over-record.png"))
        self.voc_button.setStyleSheet(style_sidebar_button)
        self.voc_button.setFixedSize(20, self.Bhauteur)
        self.voc_button.clicked.connect(self.activate_voice_command)
        self.voc_button.setToolTip("Commande vocale")
        self.main_content_layout.addWidget(self.voc_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Ajouter le layout principal à la fenêtre
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialisation de l'animation pour les sidebars
        self.animation_1 = QPropertyAnimation(self.sidebar_widget_1, b"maximumWidth")
        self.animation_1.setDuration(600)
        self.animation_1.setEasingCurve(QEasingCurve.InOutQuad)

        self.animation_2 = QPropertyAnimation(self.sidebar_widget_2, b"maximumWidth")
        self.animation_2.setDuration(600)
        self.animation_2.setEasingCurve(QEasingCurve.InOutQuad)

        # Initialisation de l'état des sidebars (pour pouvoir les refermer)
        self.sidebar_1_visible = False
        self.sidebar_2_visible = False

        # Initialisation de l'état du menu des règles de vote (pour pouvoir la refermer)
        self.regle_de_vote_visible = False

        self.democratie_visible = False

        self.carbon_display_visible = False

    def add_sidebar_1_buttons(self) -> None:
        """
        Ajoute des boutons à la barre latérale des statistiques.
        """
        # BoutonMC(self.bd,"Copeland", "Monte Cralo Copleand")
        style_sidebar_1_buttons = """
    QPushButton {
    background-color: #4CAF50;
    border: 2px solid #4CAF50;
    border-radius: 20px;
    color: white;
    padding: 10px 20px;
    /* Définir la taille des boutons */
    min-width: 200px;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #45a049;
    border-color: #45a049;
}

QPushButton:pressed {
    background-color: #388e3c;
    border-color: #388e3c;
}
"""
        bouton_monte_carlo = QPushButton("Tournoi")
        bouton_monte_carlo.setStyleSheet(style_sidebar_1_buttons)
        bouton_monte_carlo.clicked.connect(self.open_tournament_options)
        self.sidebar_layout_1.addWidget(bouton_monte_carlo)
        self.bouton_bilan_carbone = QPushButton("Bilan Carbone")
        self.bouton_bilan_carbone.setStyleSheet(style_sidebar_1_buttons)
        self.sidebar_layout_1.addWidget(self.bouton_bilan_carbone)
        self.bouton_bilan_carbone.clicked.connect(self.affiche_carbone)
        bouton_taux_satisfaction = QPushButton("Taux de satisfaction")
        bouton_taux_satisfaction.setStyleSheet(style_sidebar_1_buttons)
        #self.sidebar_layout_1.addWidget(bouton_taux_satisfaction)
        
        self.bouton_visualisation_3d = BoutonVisuel3D(self.bd)
        self.bouton_visualisation_3d.setStyleSheet(style_sidebar_1_buttons)
        self.sidebar_layout_1.addWidget(self.bouton_visualisation_3d)

        if (self.bd != None):
            #Ajout de la consommation
            self.bd.conso += emission_moyen_ouverture_menu_lat2

    
    def add_sidebar_buttons(self) -> None:
        """
        Ajoute des boutons à la barre latérale du menu.
        """
        entreeCand = EntreeCandidat(self.bd,self.Blongeur,self.Bhauteur,self.tailleMap)
        self.sidebar_layout_2.addWidget(entreeCand)
        bouton_Genr = Boutoun_GenerAleatoire(self.bd, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_Genr)
        bouton_save = BoutonSave(self.bd, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_save)
        bouton_recharge = BoutonRecharge(self.bd, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_recharge)
        self.regle_de_vote = QPushButton("Règles de vote")
        self.regle_de_vote.setFixedSize(200, self.Bhauteur)
        self.regle_de_vote.setFont(QFont('Arial', 10, QFont.Bold))
        self.regle_de_vote.setStyleSheet("""
    QPushButton {
        color: #ffffff; /* Texte blanc pour un bon contraste */
        border-style: solid;
        border-width: 1px;
        border-radius: 10px;
        border-color: #666666; /* Bordure légèrement plus sombre pour la définition */
        padding: 5px;
        margin: 4px;
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #00bfff, stop:1 #009acd /* Dégradé de bleu céleste à bleu moyen */
        );
    }
    QPushButton:hover {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #32cd32, stop:1 #228b22 /* Dégradé de vert clair à vert forêt */
        );
    }
    QPushButton:pressed {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #ff6347, stop:1 #ff4500 /* Dégradé de tomate à orange rouge */
        );
    }
""")
        self.regle_de_vote.clicked.connect(self.Menu)
        self.sidebar_layout_2.addWidget(self.regle_de_vote)

        if (self.bd != None):
            #Ajout de la consommation
            self.bd.conso += emission_moyen_ouverture_menu_lat

    def add_menu_buttons(self) -> None:
        """
        Ajoute des boutons de menu à la barre latérale des règles de vote.
        """
        self.rayon = None
        bouton_Copeland = Bouton_Mvote(self.bd, "Copeland",self.rayon, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_Copeland)
        bouton_Borda = Bouton_Mvote(self.bd, "Borda",self.rayon, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_Borda)
        bouton_Pluralite = Bouton_Mvote(self.bd, "Pluralite",self.rayon, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_Pluralite)
        bouton_STV = Bouton_Mvote(self.bd, "STV",self.rayon, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_STV)
        bouton_Approbation = Bouton_Mvote(self.bd, "Approbation",self.rayon, self.Blongeur, self.Bhauteur)
        self.sidebar_layout_2.addWidget(bouton_Approbation)

        if (self.bd != None):
            # Ajout de la consommation
            self.bd.conso += emission_moyen_bouton_vote_ouverture
    
    def add_democratie_buttons(self) -> None:
        """
        Ajoute des boutons de menu à la barre latérale des règles de vote liquide.
        """
        self.poids_lab = QLabel("Rayon :")
        self.poids = QSpinBox()
        self.poids_lab.setStyleSheet("""
            QLabel {
                color: #ffffff;  /* Texte blanc pour un meilleur contraste */
                font-family: 'Arial';  /* Police Arial, mais vous pouvez choisir celle que vous préférez */
                font-size: 14px;  /* Taille de la police */
                padding: 4px;  /* Un peu de marge interne pour que le texte respire */
            }
        """)

        # Configuration du style du QSpinBox
        self.poids.setStyleSheet("""
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
""")
        self.poids.setMaximum(250)
        self.sidebar_layout_1.addWidget(self.poids_lab)
        self.sidebar_layout_1.addWidget(self.poids)
        bouton_Copeland_liquide = Bouton_Mvote(self.bd, "Copeland liquide",self.poids.value(), self.Blongeur, self.Bhauteur)
        self.sidebar_layout_1.addWidget(bouton_Copeland_liquide)
        bouton_Borda_liquide = Bouton_Mvote(self.bd, "Borda liquide",self.poids.value(), self.Blongeur, self.Bhauteur)
        self.sidebar_layout_1.addWidget(bouton_Borda_liquide)
        bouton_Pluralite_liquide = Bouton_Mvote(self.bd, "Pluralite liquide",self.poids.value(), self.Blongeur, self.Bhauteur)
        self.sidebar_layout_1.addWidget(bouton_Pluralite_liquide)
        bouton_STV_liquide = Bouton_Mvote(self.bd, "STV liquide",self.poids.value(), self.Blongeur, self.Bhauteur)
        self.sidebar_layout_1.addWidget(bouton_STV_liquide)
        bouton_Approbation_liquide = Bouton_Mvote(self.bd, "Approbation liquide",self.poids.value(), self.Blongeur, self.Bhauteur)
        self.sidebar_layout_1.addWidget(bouton_Approbation_liquide)

    def close_menu_buttons(self) -> None:
        """
        Ferme les boutons du menu dans la barre latérale des règles de vote.
        """

        if (self.bd != None):
            # Ajout de la consommation
            self.bd.conso += emission_moyen_bouton_vote_fermeture

        for i in reversed(range(self.sidebar_layout_2.count())):
            widget = self.sidebar_layout_2.itemAt(i).widget()
            if isinstance(widget, Bouton_Mvote):
                widget.close()

    def Menu(self) -> None:
        """
        Affiche les boutons du menu dans la barre latérale des règles de vote.
        """
        if not self.regle_de_vote_visible:
            # Afficher les boutons
            self.add_menu_buttons()
        else:
            self.close_menu_buttons()
            # Mettre à jour l'état des règles de vote
        self.regle_de_vote_visible = not self.regle_de_vote_visible

    def close_democratie_buttons(self) -> None:
        """
        Ferme les boutons du menu dans la barre latérale des règles de vote.
        """
        for i in reversed(range(self.sidebar_layout_1.count())):
            widget = self.sidebar_layout_1.itemAt(i).widget()
            if isinstance(widget, Bouton_Mvote) or isinstance(widget, QLabel) or isinstance(widget, QSpinBox):
                widget.close()

    def democratie_liquide(self):
        """
        Affiche les boutons du menu dans la barre latérale de la démocratie liquide.
        """
        if not self.democratie_visible:
            # Afficher les boutons
            self.add_democratie_buttons()
        else:
            self.close_democratie_buttons()  # Fermer les boutons du menu
        self.democratie_visible = not self.democratie_visible  # Mettre à jour l'état des boutons de la démocratie liquide


    def open_settings(self) -> None:
        """
        Ouvre les paramètres.
        """
        print("Ouverture des paramètres...")  # à remplir avec ce qu'on veut faire avec

    def close_sidebar_1_buttons(self) -> None:
        """
        Ferme les boutons de la barre latérale des statistiques.
        """

        if (self.bd != None):
            #Ajout de la consommation
            self.bd.conso += emission_moyen_fermeture_menu_lat2

        for i in reversed(range(self.sidebar_layout_1.count())):
            widget = self.sidebar_layout_1.itemAt(i).widget()
            if widget is not None:
                widget.close()

    def close_sidebar_2_buttons(self) -> None:
        """
        Ferme les boutons de la barre latérale du menu.
        """

        if (self.bd != None):
            #Ajout de la consommation
            self.bd.conso += emission_moyen_fermeture_menu_lat

        for i in reversed(range(self.sidebar_layout_2.count())):
            widget = self.sidebar_layout_2.itemAt(i).widget()
            if widget is not None:
                widget.close()

    def toggle_stats_sidebar(self) -> None:
        """
        Affiche la barre latérale des statistiques.
        """
        logging.info("Basculer la barre laterale des statistiques.")
        if not self.sidebar_1_visible:
            if self.sidebar_2_visible:
                logging.debug("Fermeture du menu general car il est ouvert.")
                # Fermer le menu général s'il est ouvert
                self.toggle_menu_sidebar()
            self.animation_1.setStartValue(0)
            self.animation_1.setEndValue(self.Blongeur)
            self.add_sidebar_1_buttons()
        else:
            self.animation_1.setStartValue(self.Blongeur)
            self.animation_1.setEndValue(0)
            self.close_sidebar_1_buttons()
        self.animation_1.start()
        self.sidebar_1_visible = not self.sidebar_1_visible

    def toggle_menu_sidebar(self) -> None:
        """
        Affiche la barre latérale du menu.
        """
        if not self.sidebar_2_visible:
            if self.sidebar_1_visible:
                # Fermer le menu des statistiques s'il est ouvert
                self.toggle_stats_sidebar()
            self.animation_2.setStartValue(0)
            self.animation_2.setEndValue(self.Blongeur)
            self.add_sidebar_buttons()
        else:
            self.animation_2.setStartValue(self.Blongeur)
            self.animation_2.setEndValue(0)
            self.close_sidebar_2_buttons()
        self.animation_2.start()
        self.sidebar_2_visible = not self.sidebar_2_visible

    def activate_voice_command(self):
        logging.debug("Activation de la commande vocale.")
        slcv = SLCV()  # Créer une instance de la classe SLCV
        input_phrase = slcv.ecouter()  # Appeler la méthode ecouter() à partir de l'instance
        logging.info(f"Phrase reçue: {input_phrase}")
        if input_phrase:
            pre_analysed = slcv.pre_analse(input_phrase, data_set_preProcessing)  # Appeler la méthode pre_analse() à partir de l'instance
            command_values = slcv.traitement(pre_analysed, data_set_commands)  # Appeler la méthode traitement() à partir de l'instance

            if command_values:
                logging.info(f"Commandes dans la phrase '{input_phrase}' : {command_values}")
            else:
               logging.warning("Aucune correspondance significative trouvee pour les commandes vocales.")

            
            liste = command_values
            for commande in liste:
                if commande == 1:
                    self.bd.refresh_MV([(self.bd.map.Borda(None),1)])
                elif commande == 2:
                    self.bd.refresh_MV([(self.bd.map.Copeland(None),1)])
                elif commande == 3:
                    self.bd.refresh_MV([(self.bd.map.Pluralite(None),1)])
                elif commande == 4:
                    self.bd.refresh_MV([(self.bd.map.STV(None),1)])
                elif commande == 5:
                    self.bd.refresh_MV([(self.bd.map.Approbation(3,None),1)])

    def open_tournament_options(self):
        self.tournament_dialog = TournamentOptionsDialog(self.bd)
        self.tournament_dialog.show()

    def affiche_carbone(self):
        '''
            Affiche la consommation actuelle du programme
        '''
        if not self.carbon_display_visible:
            # Display the carbon footprint
            self.carbone_lab = QLabel("Emission carbone actuelle : ")
            self.carbone_lab.setStyleSheet("""QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 14px;
                padding: 4px;
            }""")
            self.sidebar_layout_1.addWidget(self.carbone_lab)
            
            self.conso_lab = QLabel(str(self.bd.conso) + " kW/h")
            self.conso_lab.setStyleSheet("""QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 14px;
                padding: 4px;
            }""")
            self.sidebar_layout_1.addWidget(self.conso_lab)
            self.carbon_display_visible = True  # maj de l'etat
        else:
            # on ferme le display s'il est visible
            self.close_carbone()
            self.carbon_display_visible = False  # Umaj de l'etat

    def close_carbone(self):
        """
        Close the carbon emission display.
        """
        for i in reversed(range(self.sidebar_layout_1.count())):
            widget = self.sidebar_layout_1.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.deleteLater()

        self.carbone_lab = None
        self.conso_lab = None



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideMenu()
    window.show()
    sys.exit(app.exec())
