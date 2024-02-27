import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
from Boutons import *
class SideMenu(QMainWindow):
    def __init__(self,bd,Blongeur = 300,Bhauteur = 40,tailleMap = 500):
        super().__init__()  
        #taille boutton 
        self.Blongeur = Blongeur
        self.Bhauteur = Bhauteur
        self.tailleMap = tailleMap
        self.bd = bd
        # Widget central pour afficher du texte
        #self.central_widget = QLabel("Texte initial")
        #self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout()

        # Bouton 1
        Menu_layout = QVBoxLayout()
        Menu = QPushButton("Menu")
        Menu.setFixedSize(self.Blongeur,self.Bhauteur)
        #self.layout.addWidget(Menu)
        #  Boutoun de creation des candidat 
        entreeCand = EntreeCandidat(self.bd,self.Blongeur,self.Bhauteur,self.tailleMap)
        self.layout.addWidget(entreeCand)
        
        # Boutoun de creation des candidat aleatoirement
        bouton_Genr = Boutoun_GenerAleatoire(self.bd,self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_Genr)
        
         #boutoun Borda
        bouton_Copeland  = Bouton_Mvote(self.bd,"Copeland", self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_Copeland)
        
        #boutoun Borda
        bouton_Borda = Bouton_Mvote(self.bd,"Borda", self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_Borda)
        
        #boutoun Pluralite
        bouton_Pluralite = Bouton_Mvote(self.bd,"Pluralite", self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_Pluralite)
        
        #boutoun STV
        bouton_STV = Bouton_Mvote(self.bd,"STV", self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_STV)
        
        # bouton Approbation
        bouton_Approbation = Bouton_Mvote(self.bd,"Approbation", self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_Approbation)
        # boutoun Save
        bouton_save = BoutonSave(self.bd, self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_save)
        #boutoun_recgarge
        bouton_recharge = BoutonRecharge(self.bd,self.Blongeur,self.Bhauteur)
        self.layout.addWidget(bouton_recharge)
       
    

        # Widget pour contenir les boutons du menu latéral
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.layout)
        self.setMenuWidget(self.menu_widget)

        # Alignement du layout principal en haut à gauche
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideMenu()
    window.show()
    sys.exit(app.exec())
