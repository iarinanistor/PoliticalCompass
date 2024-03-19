from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from Front.Widgets.Boutons import *

class SideMenu(QMainWindow):
    def __init__(self, bd, Blongeur=300, Bhauteur=40, tailleMap=500):
        super().__init__()

        self.bd = bd
        self.Blongeur = Blongeur
        self.Bhauteur = Bhauteur
        self.tailleMap = tailleMap

        # Layout principal
        main_layout = QHBoxLayout()

        # Contenu principal
        self.main_content_layout = QVBoxLayout()

        # sidebar avec scroll area
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_scroll = None  # Initialisation de la scroll area à None

        # Widget pour contenir les éléments du contenu principal
        self.main_content_widget = QWidget()
        self.main_content_widget.setLayout(self.main_content_layout)
        main_layout.addWidget(self.main_content_widget)

        # Bouton pour ouvrir/fermer la sidebar
        self.sidebar_button = QPushButton()
        self.sidebar_button.setIcon(QIcon("C:/Users/chady/OneDrive/Documents/TP_INFO/LU2IN013/jc2iy-Main/menu.png"))
        self.sidebar_button.setFixedSize(50, 70)
        self.sidebar_button.clicked.connect(self.toggle_sidebar)
        self.sidebar_button.setStyleSheet("border-radius: 20px;")
        self.main_content_layout.addWidget(self.sidebar_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Ajouter le layout principal à la fenêtre
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialisation de l'animation
        self.animation = QPropertyAnimation(self.sidebar_widget, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Initialisation de l'état de la scroll area
        self.sidebar_visible = False

    def add_sidebar_buttons(self):
        if self.sidebar_scroll is None:  # Créer la scroll area si elle n'existe pas
            self.sidebar_scroll = QScrollArea()
            self.sidebar_scroll.setWidgetResizable(True)
            self.sidebar_scroll.setWidget(self.sidebar_widget)
            self.sidebar_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Désactiver la scroll area verticale
            main_layout = self.layout()
            main_layout.addWidget(self.sidebar_scroll)
            self.settings_button = QPushButton("Paramètres")
            self.settings_button.setFixedSize(100, 40)
            self.settings_button.setStyleSheet("border-radius: 10px; background-color: #ffffff;")  # Fond blanc
            self.settings_button.clicked.connect(self.open_settings)
            self.sidebar_layout.addWidget(self.settings_button, alignment=Qt.AlignBottom | Qt.AlignLeft)
            entreeCand = EntreeCandidat(self.bd,self.Blongeur,self.Bhauteur,self.tailleMap)
            self.sidebar_layout.addWidget(entreeCand)
            bouton_Genr = Boutoun_GenerAleatoire(self.bd, self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_Genr)
            bouton_Copeland = Bouton_Mvote(self.bd, "Copeland", self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_Copeland)
            bouton_Borda = Bouton_Mvote(self.bd, "Borda", self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_Borda)
            bouton_Pluralite = Bouton_Mvote(self.bd, "Pluralité", self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_Pluralite)
            bouton_STV = Bouton_Mvote(self.bd, "STV", self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_STV)
            bouton_Approbation = Bouton_Mvote(self.bd, "K-Approbation", self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_Approbation)
            bouton_save = BoutonSave(self.bd, self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_save)
            bouton_recharge = BoutonRecharge(self.bd, self.Blongeur, self.Bhauteur)
            self.sidebar_layout.addWidget(bouton_recharge)

            self.sidebar_scroll.setFixedWidth(self.Blongeur + 30)  # Ajouter 30 pixels d'espace en longueur à la longueur des boutons pour pas prendre trop de place

    def close_sidebar_buttons(self):
        if self.sidebar_scroll is not None:  # Supprimer la scroll area si elle existe
            self.sidebar_scroll.deleteLater()
            self.sidebar_scroll = None
            for i in reversed(range(self.sidebar_layout.count())):
                widget = self.sidebar_layout.itemAt(i).widget()
                if widget is not None:
                    widget.close()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.close_sidebar_buttons()
            self.animation.setEndValue(0)
            self.animation.setStartValue(self.Blongeur)
        else:
            self.add_sidebar_buttons()
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.Blongeur)
        self.sidebar_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.animation.start()
        self.sidebar_visible = not self.sidebar_visible

    def closeEvent(self, event):
        if self.sidebar_visible:
            self.toggle_sidebar()
        QMainWindow.closeEvent(self, event)

    def open_settings(self):
        print("Ouverture des paramètres...")  # à remplir avec ce qu'on veut faire avec

