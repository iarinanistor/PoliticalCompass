import sys
from Front.Utilitaire import *
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox
from PySide6.QtGui import QIcon
import logging

#Variable global du fichier 
type1 ="Copeland"
type2="Borda"
type3="Pluralite"
type4="STV"
type5="Approbation"
fichier = "Front/Widgets/Texture/Bouton.qss"
# config LOG 
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from Internet import internet
from Internet import iso_code
#Importation de la consommation des fonctions utilisées
from Calcul_Emissions import emission_moyen_soumission_candidat, emission_moyen_copeland_liquide, emission_moyen_borda_liquide, emission_moyen_pluralite_liquide, emission_moyen_stv_liquide, emission_moyen_approbation_liquide

class EntreeCandidat(QWidget):
    def __init__(self,bd,l=200,h=80,tailleMap=500):
        super().__init__()
        self.setStyleSheet(open(fichier).read())
        self.bd=bd
        layout = QVBoxLayout()
        # Definir la taille du widget
        self.setFixedSize(l, h*2.5)
        # Layout pour le nom et le prénom sur la même ligne
        nom_prenom_layout = QHBoxLayout()
        
        # Zone de texte pour le nom
        self.nom_label = QLabel("Nom:")
        self.nom_edit = QLineEdit()
        nom_prenom_layout.addWidget(self.nom_label)
        nom_prenom_layout.addWidget(self.nom_edit)
        
        # Zone de texte pour le prénom
        self.prenom_label = QLabel("Prénom:")
        self.prenom_edit = QLineEdit()
        nom_prenom_layout.addWidget(self.prenom_label)
        nom_prenom_layout.addWidget(self.prenom_edit)
        
        layout.addLayout(nom_prenom_layout)
        
        # Layout pour les trois champs d'entier côte à côte
        valeurs_layout = QHBoxLayout()
        
        self.valeur_edits = []  # Liste pour stocker les boutons de type QSpinBox
        
        nom_boutons = ["Charisme", "   X", "  Y"]
        for i in range(3):  # Trois champs d'entier côte à côte
            label = QLabel(nom_boutons[i])
            edit = QSpinBox()
            # Vous pouvez définir d'autres limites si nécessaire
            edit.setMinimum(0)
            if i == 0:
                edit.setMaximum(100)
            else:
                edit.setMaximum(tailleMap)
            valeurs_layout.addWidget(label)
            valeurs_layout.addWidget(edit)
            self.valeur_edits.append(edit)  # Ajouter le bouton à la liste
        
        layout.addLayout(valeurs_layout)
        
        # Bouton pour soumettre les informations
        submit_button = QPushButton("Soumettre")
        submit_button.clicked.connect(self.afficher_informations)
        layout.addWidget(submit_button)
        
        self.setLayout(layout)
        
        # Redimensionner le widget principal
        #self.resize(h,l)  # Largeur : 600 pixels, Hauteur : 200 pixels
    def refresh_champ(self):
        self.nom_edit.clear()
        self.prenom_edit.clear()
        
        for edit in self.valeur_edits:
            edit.clear()
    
    def afficher_informations(self):
        logging.info("<Gestion des Boutons de soumission de Candidat>")
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        valeurs = [edit.value() for edit in self.valeur_edits]
        if nom != "" and prenom != "" :# Utiliser la liste self.valeur_edits
            logging.info('          Informations soumises - Nom: {}, Prenom: {}, Valeurs entieres: {}.'.format(nom, prenom, valeurs))
            
            print("Nom:", nom)
            print("Prénom:", prenom)
            print("Valeurs entières:", valeurs)
            new = normalise_button( nom,prenom,valeurs)
            newC = normalise_button_C( nom,prenom,valeurs)
            self.bd.ajoute(new,newC)
        logging.info("<Fin Gestion des Boutons de soumission de Candidat>")    
        # Effacer les données des zones de texte
        self.refresh_champ()

        #Ajout de la consommation
        self.bd.conso += emission_moyen_soumission_candidat


class Bouton_Mvote(QWidget):
    def __init__(self,bd,type_m="Approbation",rayon=None,l=200,h=80):
        super().__init__()
        self.setStyleSheet(open(fichier).read())
        self.bd= bd
        self.h = h
        self.l = l
        self.setFixedSize(self.l, self.h)
        self.map=self.bd.map
        self.type_m = type_m
        self.rayon = rayon
        layout = QVBoxLayout()
        
        # Créer un bouton
        self.button = QPushButton(self.type_m)
        
        # Connecter un signal à une fonction lorsque le bouton est cliqué
        self.button.clicked.connect(self.on_button_clicked)
        
        # Ajouter le bouton au layout
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
    # Fonction appelée lorsque le bouton est cliqué
    def on_button_clicked(self):
        logging.info("<Gestion des Boutons des regles de vote>")
        logging.info('          Bouton {} clique.'.format(self.type_m))
        
        self.button.setEnabled(False)
        if self.type_m == type1:
            self.bd.refresh_MV([normalise_Ind(self.map.Copeland(self.rayon),1)])

            #Ajout de la consommation
            self.bd.conso += emission_moyen_copeland_liquide
            
        elif self.type_m == type2: #Borda
            self.bd.refresh_MV([normalise_Ind(self.map.Borda(self.rayon),1)])
            
            #Ajout de la consommation
            self.bd.conso += emission_moyen_borda_liquide

        elif self.type_m == type3:
            self.bd.refresh_MV([normalise_Ind(self.map.Pluralite(self.rayon),1)])
            
            #Ajout de la consommation
            self.bd.conso += emission_moyen_pluralite_liquide

        elif self.type_m == type4:
            self.bd.refresh_MV([normalise_Ind(self.map.STV(self.rayon),1)])
            
            #Ajout de la consommation
            self.bd.conso += emission_moyen_stv_liquide

        else :
            self.bd.refresh_MV([normalise_Ind(self.map.Approbation(3,self.rayon),1)])
            
            #Ajout de la consommation
            self.bd.conso += emission_moyen_approbation_liquide

        logging.info("<Fin Gestion des Boutons des regles de vote>")
        self.button.setEnabled(True)

class Boutoun_GenerAleatoire(QWidget):
    def __init__(self,bd,l,h):
        super().__init__()
        self.setStyleSheet(open(fichier).read())
        self.h = h
        self.l = l
        self.setFixedSize(self.l, self.h)
        self.bd = bd
        
        layout = QVBoxLayout()
        
        # Créer un bouton
        self.button = QPushButton("Genere un Candidat")
        
        # Connecter un signal à une fonction lorsque le bouton est cliqué
        self.button.clicked.connect(self.on_button_clicked)
        
        # Ajouter le bouton au layout
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
    # Fonction appelée lorsque le bouton est cliqué
    def on_button_clicked(self):

        self.button.setEnabled(False)
        cd = self.bd.genere_aleatoire_candidat_BM()
        nom =cd.nom()
        prenom = cd.prenom()
        valeurs=[cd.charisme(),int(cd.x()),int(cd.y())]
        
        new = normalise_button( nom,prenom,valeurs)
        newC = normalise_button_C( nom,prenom,valeurs)
        self.bd.ajoute(new,newC)
        self.button.setEnabled(True)

class BoutonIO(QWidget):
    def __init__(self,bd,nom,l=200,h=80):
        super().__init__()
        self.setStyleSheet(open(fichier).read())
        self.h = h
        self.l = l
        self.setFixedSize(self.l, self.h*2)
        self.bd = bd
        self.nom=nom
        layout = QVBoxLayout(self)

        # Champ de texte
        self.text_edit = QLineEdit()
        layout.addWidget(self.text_edit) 

        # Bouton I/O
        if self.nom == "recharge":
            self.io_button = QPushButton()
            self.io_button.setIcon(QIcon("images/icons/cil-file.png"))
        else:
            self.io_button = QPushButton()
            self.io_button.setIcon(QIcon("images/icons/cil-save.png"))
        self.io_button.clicked.connect(self.save_text)
        layout.addWidget(self.io_button)

    def save_text(self):
        logging.info("<Gestion des Boutons de recharge>")
        self.io_button .setEnabled(False)
        text = self.text_edit.text()
        if self.nom == "recharge":   
            logging.info('          Fichier de recharge specifie: {}.'.format(text))
            self.bd.recharge(text)
        else :
            logging.info('          Fichier de sauvegarde specifie: {}.'.format(text))
            self.bd.save(text)
        logging.info("<Fin Gestion des Boutons de sauvegarde>")
        self.text_edit.clear()  # Efface le texte après sauvegarde
        self.io_button.setEnabled(True)
        
class BoutonRecharge(BoutonIO):
    def __init__(self, bd, l=200, h=80):
        super().__init__(bd, "recharge", l, h)
        
class BoutonSave(BoutonIO):
    def __init__(self, bd, l=200, h=80):
        super().__init__(bd, "save", l, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BoutonIO()
    widget.show()
    sys.exit(app.exec()) 