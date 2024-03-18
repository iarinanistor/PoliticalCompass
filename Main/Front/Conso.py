from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy, QSpacerItem
from MenuLateral import SideMenu
from ListeRes import ListePoint
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QColor
from MapQT import Compass
from SWindow import SettingsWindow
from Base_Donnee import Base_donnee
import sys

import os

csv_file_path = "Conso_energie.csv"

if os.path.exists(csv_file_path):
    os.remove(csv_file_path)


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

devices = DeviceFactory.create_devices()
meter = EnergyMeter(devices)


#csv_handler = CSVHandler("Conso_energie.csv")

from VarGlob import csv_handler


trace = meter.get_trace()

#Début de la mesure
meter.start(tag="Début de la mesure")

app = QApplication([])
swindow = SettingsWindow()
swindow.show()


#Fin de la mesure
meter.stop()

#Affichage de la consommation énergétique
trace += meter.get_trace()
print(trace)

#Sauvegarde des données dans un fichier CSV
csv_handler.save_data()
"""
    Enregistre les données sous la forme :
        timestamp;tag;duration;package_0;nvidia_gpu_0
        temps au moment du relevé; nom de la fonction; durée de la mesure; Energie consommée par le CPU; Energie consommée par le GPU
"""


sys.exit(app.exec())