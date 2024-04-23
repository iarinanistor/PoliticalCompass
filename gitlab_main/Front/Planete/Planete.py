import logging
import sys
import math
from Front.Utilitaire import generate_unique_colors
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QImage, QVector2D, QColor
from PySide6.QtCore import QTimer 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Planete(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lastPos = None
        self.angularSpeed = QVector2D(0.0, 0.0)
        self.setMouseTracking(True)
        self.spheres = []
        self.auto_rotation_timer = QTimer(self)
        self.auto_rotation_timer.timeout.connect(self.auto_rotate_planet)
        self.auto_rotation_timer.start(20)
        self.coef_taille = 0.9

    def auto_rotate_planet(self):
        """
        Fait tourner automatiquement la planète.
        """
        self.angularSpeed += QVector2D(0.1, 0.1)
        self.update()

    def initializeGL(self):
        """
        Initialise les paramètres OpenGL.
        """
        glDisable(GL_LIGHTING)
        gluPerspective(45, (self.width() / self.height()), 0.1, 50.0)
        glTranslatef(0.0, 0 , -5)
        filename = str(os.getcwd())+"/Front/Planete/Texture/final.png" # repertoire courrant , si il y a un buf cela est du a quel endroit on lance le fichier 

        self.texture = self.load_texture(filename) 
        glEnable(GL_DEPTH_TEST)

    def load_texture(self, filename):
        """
        Charge la texture de la planète.
        """
        
        texture_surface = QImage(filename)
        if texture_surface.isNull():
            texture_surface= QImage( str(os.getcwd())+"/gitlab_main/Front/Planete/Texture/final.png") #depend de ou on lance le fichier 
            if texture_surface.isNull():
                print("Failed to load texture.")
                print("Attempting to load image at:", filename)
                print("Absolute path:", os.path.abspath(filename))
                print("File exists:", os.path.exists(filename))
                return None
        
        texture_surface = texture_surface.convertToFormat(QImage.Format_RGBA8888)
        width = texture_surface.width()
        height = texture_surface.height()

        texture_data = texture_surface.bits().tobytes()

        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texid

    def paintGL(self):
        """
        Dessine la planète et les sphères ajoutées.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.update_sphere_rotation()
        self.draw_sphere()
        for sphere in self.spheres:
            self.draw_point_on_sphere(*sphere)

    def update_sphere_rotation(self):
        """
        Met à jour la rotation de la planète.
        """
        glLoadIdentity()
        glRotatef(self.angularSpeed.x(), 1, 0, 0)
        glRotatef(self.angularSpeed.y(), 0, 1, 0)

    def draw_sphere(self):
        """
        Dessine la sphère représentant la planète.
        """
        if self.texture is None:
            print("Texture not loaded, skipping draw.")
            return  # Exit the function if texture is not loaded
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluQuadricNormals(quad, GLU_SMOOTH)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(quad, self.coef_taille, 32, 32)
        gluDeleteQuadric(quad)

    def draw_point_on_sphere(self, radius, latitude, longitude,color):
        """
        Dessine un point sur la surface de la planète.

        Args:
            radius (float): Rayon de la sphère.
            latitude (float): Latitude du point.
            longitude (float): Longitude du point.
            color (QColor): Couleur du point.
        """
        x = radius * math.sin(math.radians(latitude)) * math.cos(math.radians(longitude))
        y = radius * math.sin(math.radians(latitude)) * math.sin(math.radians(longitude))
        z = radius * math.cos(math.radians(latitude))
        glPushMatrix()
        glTranslatef(x, y, z)
        color_rgb = (int(color.redF() * 255), int(color.greenF() * 255), int(color.blueF() * 255))
        glColor3ub(*color_rgb )  
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, (0.05/0.5)*self.coef_taille, 10, 10)
        gluDeleteQuadric(quad)
        glColor3f(1.0, 1.0, 1.0)
        glPopMatrix()

    def mousePressEvent(self, event):
        self.auto_rotation_timer.stop()
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        if self.lastPos:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()

            sensitivity = 0.2
            self.angularSpeed += QVector2D(-dy * sensitivity, -dx * sensitivity)

            self.lastPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.auto_rotation_timer.start(20)
        self.lastPos = None

    def refresh_Map( self, new):
        """
        Actualise la carte avec des nouveaux candidats.

        Args:
            new (list): Liste des nouveaux candidats à afficher.
        """
        logging.info('<Planete.refresh_Map>')
        self.clear_spheres()
        
        for cand in new:
            x = cand.x()*5 # on re-adapte la taille, pour que ce soit propotionelle
            y = cand.y()*5
            color = generate_unique_colors(x, y)
            self.add_sphere(x,y,color)
        logging.info('</Planete.refresh_Map>')

    def add_sphere(self, latitude, longitude,color):
        """
        Ajoute une sphère représentant un point sur la surface de la planète.

        Args:
            latitude (float): Latitude du point.
            longitude (float): Longitude du point.
            color (QColor): Couleur du point.
        """
        logging.info('<Planete.add_sphere>')
        logging.info('<Planete.add_sphere.INFO> latitude: %s, longitude: %s, color: %s', latitude, longitude, color.name())
        self.spheres.append((self.coef_taille, latitude, longitude, color))
        self.update()
        logging.info('</Planete.add_sphere>')

    def remove_sphere(self, latitude, longitude):
        """
        Supprime une sphère représentant un point sur la surface de la planète.

        Args:
            latitude (float): Latitude du point.
            longitude (float): Longitude du point.
        """
        logging.info('<Planete.remove_sphere>')
        logging.info('<Planete.remove_sphere.INFO> latitude: %s, longitude: %s', latitude, longitude)
        for sphere in self.spheres:
            if sphere == (self.coef_taille,latitude, longitude):
                self.spheres.remove(sphere)
                break
        self.update()
        logging.info('</Planete.remove_sphere>')
    
    def clear_spheres(self):
        """
                Efface toutes les sphères représentant les points sur la surface de la planète.
        """
        logging.info('<Planete.clear_spheres>')
        self.spheres = []
        self.update() 
        logging.info('</Planete.clear_spheres>')

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
        logging.info('<MainWindow.clear_all_spheres>')
        self.openGLWidget.clear_spheres()
        logging.info('</MainWindow.clear_all_spheres>')
        
    def add_sphere_clicked(self):
        """
        Ajoute une sphère sur la surface de la planète en fonction des coordonnées saisies.
        """
        logging.info('<MainWindow.add_sphere_clicked>')
        latitude = float(self.latitude_input.text())
        longitude = float(self.longitude_input.text())
        self.openGLWidget.add_sphere(latitude, longitude, QColor.white)
        self.latitude_input.clear()
        self.longitude_input.clear()
        logging.info('</MainWindow.add_sphere_clicked>')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

