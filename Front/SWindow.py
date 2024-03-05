from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy, QSpacerItem
from MenuLateral import SideMenu
from ListeRes import ListePoint
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QColor
from MapQT import Compass
from Base_Donnee import Base_donnee
import sys


class SettingsWindow(QMainWindow):
    def __init__(self, tailleMap = 250):
        """
        Constructeur de la classe SettingsWindow qui descend de la classe QMainWindow.

        Args:
            tailleMap (int): Taille de la map

        Returns:
            void
        """
        super().__init__()
        self.setWindowTitle("Réglages de la fenêtre principale")
        self.tailleMap = tailleMap
        
        #Configurer la géométrie de la fenêtre
        self.setGeometry(100, 100, 1200, 800)

        #Taille des boutons
        self.Blongeur = 300
        self.Bhauteur = 40

        #Créer un widget central pour la fenêtre principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Créer un layout vertical principal pour organiser les sous-layouts horizontaux
        main_layout = QVBoxLayout(central_widget)

        #Variables contenant les attributs de style des widgets
        main_frame_style = """
                        QFrame {
                            background-color: #777777;
                            border: 2px solid #B0B0B0;
                            border-radius: 3px;
                            margin: 2px;
                        }
                      """
        
        frame_style = """
                        QFrame {
                            background-color: #47E3FF;
                            border: 2px solid #B0B0B0;
                            border-radius: 3px;
                            margin: 2px;
                        }
                      """
        
        label_style = """
                        QFrame {
                            background-color: #DDDDDD;
                        }
                      """


        #Frame centré contenant les autres frames
        main_frame = QFrame(self)
        main_frame.setFixedSize(600, 200)
        main_frame.setFrameShape(QFrame.StyledPanel)
        main_frame.setFrameShadow(QFrame.Raised)
        main_frame.setStyleSheet(main_frame_style)

        main_layout.addWidget(main_frame, alignment=Qt.AlignCenter)

        main_frame_layout = QVBoxLayout(main_frame)
        main_frame.setLayout(main_layout)


        #Frame pour la taille de la map centré contenant les informations à modifier
        tailleMap_frame = QFrame(main_frame)
        tailleMap_frame.setFixedSize(400, 50)
        tailleMap_frame.setFrameShape(QFrame.StyledPanel)
        tailleMap_frame.setFrameShadow(QFrame.Raised)
        tailleMap_frame.setStyleSheet(frame_style)

        #Layout contenant le label et la zone d'entrée utilisateur pour la taille de la grille
        tailleMap_layout = QHBoxLayout(tailleMap_frame)
        #longueur_layout.setAlignment(Qt.AlignCenter)

        tailleMap_label = QLabel("Taille de la map :")
        tailleMap_label.setStyleSheet(label_style)
        self.tailleMap_input = QLineEdit(self)
        #Taille du label
        tailleMap_label.setFixedSize(110, 30)
        #Taille de l'entry
        self.tailleMap_input.setFixedSize(150, 30)

        #Ajout des widgets à la fenêtre
        tailleMap_layout.addWidget(tailleMap_label)
        tailleMap_layout.addWidget(self.tailleMap_input)

        #main_layout.addLayout(longueur_layout)
        tailleMap_frame.setLayout(tailleMap_layout)
        main_frame_layout.addWidget(tailleMap_frame, alignment=Qt.AlignCenter)


        #Bouton de validation de la taille de la map
        taille_map_button = QPushButton("Valider", self)
        taille_map_button.clicked.connect(self.on_taille_button_clicked)
        taille_map_button.setFixedSize(80, 20)
        tailleMap_layout.addWidget(taille_map_button)
        main_frame_layout.addWidget(tailleMap_frame, alignment=Qt.AlignCenter)

        #Bouton de validation des réglages
        validate_button = QPushButton("Valider", self)
        validate_button.clicked.connect(self.on_validate_button_clicked)
        main_layout.addWidget(validate_button)

        self.setLayout(main_layout)

    
    #Fonctions pour modifier les dimensions de la grille
    def setTailleMap(self, taille):
        """
        Méthode setter qui modifie l'attribut tailleMap

        Args:
            tailleMap (int): Taille de la map

        Returns:
            void
        """
        self.tailleMap = taille

    #Fonction de validation de la taille de la grille
    def on_taille_button_clicked(self):
        """
        Méthode qui valide la taille de la map entrée par l'utilisateur

        Returns:
            void: Affiche une fenêtre pop-up décrivant le succès ou l'échec de la modification
                  (OK si taille > 100
                   Fail si taille <= 100)
        """
        #On récupère la valeur entrée par l'utilisateur
        newTailleMap = int(self.tailleMap_input.text())

        #Test si la taille entrée est bien >= 100
        if (newTailleMap < 100):
            message_error_box = QMessageBox(self)
            message_error_box.setWindowTitle("Warning")
            message_error_box.setText("La taille ne peut pas être inférieur à 100 !")
            message_error_box.setFixedSize(500, 200)
            
            message_error_box.exec()
        else:
            #Affichage d'une pop-up confirmant la modification
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Modification de la taille de la map")
            message_box.setText("Changement de la taille de la map effectué avec succès !")
            message_box.setFixedSize(500, 200)

            message_box.exec()

            #On modifie l'attribut tailleMap
            self.tailleMap = newTailleMap

    #Fonction de validation des réglages
    def on_validate_button_clicked(self):
        """
        Méthode qui valide les paramètres et ferme la fenêtre SWindow pour ouvrir la fenêtre MainWindow

        Returns:
            void
        """
        #Fermeture de la fenêtre
        self.close()

        #Ouverture de la fenêtre principale
        bd = Base_donnee.creer(123, self.tailleMap)
        bd.window.show()


if __name__ == "__main__":
    app = QApplication([])
    swindow = SettingsWindow()
    swindow.show()
    sys.exit(app.exec())