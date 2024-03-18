import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QProgressBar, QVBoxLayout


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler



class ProgressDialog(QDialog):
    @measure_energy(handler=csv_handler)
    def __init__(self, parent=None):
        """
        Constructeur de la classe ProgressDialog.

        Args:
            parent (QWidget): Widget parent. Par défaut, None.
        """
        super().__init__(parent)
        self.setWindowTitle("Loading...")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        layout = QVBoxLayout(self)
        
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        layout.addWidget(self.progress)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)  # Update progress every 50 milliseconds
    
    @measure_energy(handler=csv_handler)
    def update_progress(self):
        """
        Méthode pour mettre à jour la barre de progression.
        """
        value = self.progress.value() + 1
        if value > self.progress.maximum():
            self.timer.stop()
            self.accept()  # Close the dialog when progress is complete
        else:
            self.progress.setValue(value)

@measure_energy(handler=csv_handler)
def show_loading_dialog():
    """
    Fonction pour afficher la boîte de dialogue de chargement.
    """
    app = QApplication(sys.argv)
    dialog = ProgressDialog()
    dialog.exec()

