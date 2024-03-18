import sys
from PySide6.QtWidgets import QApplication, QMessageBox


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler



class CustomMessageBox(QMessageBox):
    @measure_energy(handler=csv_handler)
    def __init__(self, *args, **kwargs):
        """
        Constructeur de la classe CustomMessageBox.

        Args:
            args: Arguments de la classe parente.
            kwargs: Arguments nommés de la classe parente.
        """
        super().__init__(*args, **kwargs)

        # Ajout d'une icône prédéfinie pour une croix rouge à la boîte de message
        self.setIcon(QMessageBox.Warning)

        # Ajouter le texte à la boîte de message
        self.setText("Une erreur s'est produite.")
        self.setInformativeText("Croix rouge à côté")

        # Personnalisation du bouton standard pour une croix rouge
        self.setStandardButtons(QMessageBox.Ok)
        self.button(QMessageBox.Ok).setStyleSheet("background-color: red;")


if __name__ == "__main__":
    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Créer une instance de CustomMessageBox
    msgBox = CustomMessageBox()

    # Définir le titre de la boîte de message
    msgBox.setWindowTitle("Message d'erreur")

    # Afficher la boîte de message
    msgBox.exec()

    # Quitter l'application
    sys.exit(app.exec())
