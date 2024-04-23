import sys
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from Front.Widgets.Boutons import *
from PySide6.QtGui import QIcon, QFont

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
        self.main_content_widget.setFixedHeight(150)
        main_layout.addWidget(self.main_content_widget, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=0)

        style_sidebar_button = """QPushButton {
            border: 1px solid #555;
            border-radius: 10px;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #555, stop: 1 #888);
            color: white;
            padding: 5px;
            min-width: 100px;
            min-height: 40px;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #777, stop: 1 #aaa);
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #333, stop: 1 #666);
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
        bouton_monte_carlo = BoutonTournoi(self.bd)
        bouton_monte_carlo.setStyleSheet(style_sidebar_1_buttons)
        self.sidebar_layout_1.addWidget(bouton_monte_carlo)
        bouton_bilan_carbone = QPushButton("Bilan Carbone")
        bouton_bilan_carbone.setStyleSheet(style_sidebar_1_buttons)
        self.sidebar_layout_1.addWidget(bouton_bilan_carbone)
        bouton_taux_satisfaction = QPushButton("Taux de satisfaction")
        bouton_taux_satisfaction.setStyleSheet(style_sidebar_1_buttons)
        self.sidebar_layout_1.addWidget(bouton_taux_satisfaction)
        self.democratie = QPushButton("Démocratie liquide")
        self.democratie.setStyleSheet(style_sidebar_1_buttons)
        self.democratie.clicked.connect(self.democratie_liquide)
        self.sidebar_layout_1.addWidget(self.democratie)

    
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
        for i in reversed(range(self.sidebar_layout_1.count())):
            widget = self.sidebar_layout_1.itemAt(i).widget()
            if widget is not None:
                widget.close()

    def close_sidebar_2_buttons(self) -> None:
        """
        Ferme les boutons de la barre latérale du menu.
        """
        for i in reversed(range(self.sidebar_layout_2.count())):
            widget = self.sidebar_layout_2.itemAt(i).widget()
            if widget is not None:
                widget.close()

    def toggle_stats_sidebar(self) -> None:
        """
        Affiche la barre latérale des statistiques.
        """
        if not self.sidebar_1_visible:
            if self.sidebar_2_visible:
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideMenu()
    window.show()
    sys.exit(app.exec())
