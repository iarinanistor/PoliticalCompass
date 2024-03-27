import sys
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from Front.Widgets.Boutons import *
from PySide6.QtGui import QIcon

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
        self.sidebar_widget_1.setContentsMargins(0,25,0,0)
 
        self.sidebar_layout_2 = QVBoxLayout()
        self.sidebar_widget_2 = QWidget()
        self.sidebar_widget_2.setLayout(self.sidebar_layout_2)
        self.sidebar_widget_2.setMaximumWidth(0)
        self.sidebar_widget_2.setContentsMargins(0,25,0,0)

        main_layout.addWidget(self.sidebar_widget_1)
        main_layout.addWidget(self.sidebar_widget_2)

        # Widget pour contenir les éléments du contenu principal
        self.main_content_widget = QWidget()
        self.main_content_widget.setLayout(self.main_content_layout)
        self.main_content_widget.setFixedHeight(120)
        self.main_content_layout.setContentsMargins(0,25,0,0)
        main_layout.addWidget(self.main_content_widget, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=0)

        # Bouton pour ouvrir/fermer la sidebar 1 (Menu)
        self.sidebar_menu_button = QPushButton()
        self.sidebar_menu_button.setIcon(QIcon("images/icons/icon_menu.png"))
        self.sidebar_menu_button.setStyleSheet("border-radius: 20px;")
        self.sidebar_menu_button.setFixedSize(20, self.Bhauteur)
        self.sidebar_menu_button.clicked.connect(self.toggle_menu_sidebar)
        self.main_content_layout.addWidget(self.sidebar_menu_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Bouton pour ouvrir/fermer la sidebar 2 (Statistiques)
        self.sidebar_stats_button = QPushButton()
        self.sidebar_stats_button.setIcon(QIcon("images/icons/cil-chart.png"))
        self.sidebar_stats_button.setStyleSheet("border-radius: 20px;")
        self.sidebar_stats_button.setFixedSize(20, self.Bhauteur)
        self.sidebar_stats_button.clicked.connect(self.toggle_stats_sidebar)
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
        bouton_monte_carlo = QPushButton("Monte Carlo")
        bouton_monte_carlo.setStyleSheet("""
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
""")
        self.sidebar_layout_1.addWidget(bouton_monte_carlo)
        bouton_bilan_carbone = QPushButton("Bilan Carbone")
        bouton_bilan_carbone.setStyleSheet("""
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
""")
        self.sidebar_layout_1.addWidget(bouton_bilan_carbone)
        bouton_taux_satisfaction = QPushButton("Taux de satisfaction")
        bouton_taux_satisfaction.setStyleSheet("""
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
""")
        self.sidebar_layout_1.addWidget(bouton_taux_satisfaction)
        self.democratie = QPushButton("Démocratie liquide")
        self.democratie.setStyleSheet("""
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
""")
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
        self.regle_de_vote.setFixedSize(120, self.Bhauteur)
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
            if isinstance(widget, Bouton_Mvote) or isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
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
