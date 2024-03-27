import sys
from PySide6.QtWidgets import *
from Front.Widgets.MenuLateral import SideMenu
from Front.Widgets.ListeRes import ListePoint
from PySide6.QtCore import *
from PySide6.QtGui import *
from Front.Widgets.MapQT import Compass
from Front.Planete.Planete import Planete
from resources_rc import *
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class LWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.Blongeur = 300
        self.Bhauteur = 40

        main_layout = QVBoxLayout()

        self.map2d_choix = False

        self.choix = QLabel("Choisissez une map")
        self.map2d_button = QPushButton("Map 2D")
        self.map2d_button.setFixedSize(200, self.Bhauteur)
        main_layout.addWidget(self.choix)
        main_layout.addWidget(self.map2d_button, alignment=Qt.AlignLeft)

        self.compass = Planete()
        self.compass.setFixedSize(500, 500)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.compass)

        self.setLayout(main_layout)
        main_layout.addLayout(top_layout)
        self.setGeometry(100, 100, 1250, 900)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #global bd
    window = LWindow()
    window.show()
    sys.exit(app.exec())

        
                



        
