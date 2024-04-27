from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QLabel, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer, Qt
import sys
import logging
from random import randint
from Back.Candidat import Candidat
from Front.Widgets.Resultat import *
import unittest

class TestListeResultat(unittest.TestCase):
    def setUp(self):
        candidats = [(Candidat("Doe", "John", 50, 30, 5, 5,),100)]
        self.listeResultat = ListeResultat(candidats)
    
    def test_populate_list(self):
        """Teste si la liste est correctement peuplée avec des candidats."""
        self.listeResultat.populate_list()
        # Supposons que populate_list ajoute réellement des items à la QListWidget
        self.assertNotEqual(self.listeResultat.count(), 1)
    
class TestBarreScore(unittest.TestCase):
    def setUp(self):
        self.candidat = Candidat("Doe", "John", 50, 30, 5, 5)
        self.barreScore = BarreScore(self.candidat, 100)
    
    def test_initialisation(self):
        """Teste si le widget est correctement initialisé avec un candidat et un score."""
        self.assertEqual(self.barreScore.cand.nom(), "Doe")
        self.assertEqual(self.barreScore.score, 100)


if __name__ == "__main__":
    #app = QApplication([])  # Nécessaire pour tester les widgets
    #unittest.main()
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)
    
    # Générer des candidats pour le test
    candidats = [(Candidat("Prenom" + str(i), "Nom" + str(i),
                randint(0, 100), randint(0, 100),randint(0, 100), randint(0, 100)),1)
                 for i in range(5)]
    
    # Créer et peupler ListeResultat
    listeResultat = ListeResultat(candidats)
    listeResultat.populate_list()
    
    layout.addWidget(listeResultat)
    window.show()
    sys.exit(app.exec_())