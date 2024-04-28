from PySide6.QtWidgets import QApplication
from Front.Utilitaire import generate_unique_colors
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QImage, QVector2D, QColor
from PySide6.QtCore import QTimer 
import sys

from Front.Planete.Planete import Planete
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.openGLWidget = Planete()
        self.openGLWidget.setFixedSize(500, 500)
        layout.addWidget(self.openGLWidget)

        self.latitude_label = QLabel("Latitude:")
        layout.addWidget(self.latitude_label)
        self.latitude_input = QLineEdit()
        layout.addWidget(self.latitude_input)

        self.longitude_label = QLabel("Longitude:")
        layout.addWidget(self.longitude_label)
        self.longitude_input = QLineEdit()
        layout.addWidget(self.longitude_input)

        self.add_sphere_button = QPushButton("Ajouter une sphère")
        self.add_sphere_button.clicked.connect(self.add_sphere_clicked)
        layout.addWidget(self.add_sphere_button)
        
        clear_button = QPushButton("Effacer tout")
        clear_button.clicked.connect(self.clear_all_spheres)
        layout.addWidget(clear_button)
        
    def clear_all_spheres(self):
        """
        Efface toutes les sphères affichées sur la surface de la planète.
        """

        self.openGLWidget.clear_spheres()

        
    def add_sphere_clicked(self):
        """
        Ajoute une sphère sur la surface de la planète en fonction des coordonnées saisies.
        """
        latitude = float(self.latitude_input.text())
        longitude = float(self.longitude_input.text())
        self.openGLWidget.add_sphere(latitude, longitude, QColor(255, 255, 255))
        self.latitude_input.clear()
        self.longitude_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

