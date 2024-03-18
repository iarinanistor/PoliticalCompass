import sys
from Loading import show_loading_dialog
from Utilitaire import *
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox
#Variable global du fichier 
type1 ="Copeland"
type2="Borda"
type3="Pluralite"
type4="STV"
type5="Approbation"


class EntreeCandidat(QWidget):
    def __init__(self,bd,l=200,h=80,tailleMap=500):
        """
        Constructeur de la classe EntreeCandidat qui descend de la classe QWidget.

        Args:
            id (int): Identifiant de la classe.
            bd (Base_donnee): Base de données utilisée pour générer les candidats et la map
            l (int): Longueur des widgets. Par défaut, 200
            h (int): Hauteur des widgets. Par défaut, 80
            tailleMap (int): Taille de la carte. Par défaut, 500.
        
        Returns:
            void
        """
        super().__init__()
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
        """
        Méthode pour vider la zone d'entrée clavier de l'utilisateur.

        Returns:
            void
        """
        self.nom_edit.clear()
        self.prenom_edit.clear()
        
        for edit in self.valeur_edits:
            edit.clear()
    
    def afficher_informations(self):
        """
        Méthode pour afficher les informations entrées par l'utilisateur pour soumettre un nouveau candidat 
        (dans la console).

        Returns:
            void
        """
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        valeurs = [edit.value() for edit in self.valeur_edits]
        if nom != "" and prenom != "" :# Utiliser la liste self.valeur_edits
            print("Nom:", nom)
            print("Prénom:", prenom)
            print("Valeurs entières:", valeurs)
            new = normalise_button( nom,prenom,valeurs)
            newC = normalise_button_C( nom,prenom,valeurs)
            self.bd.ajoute(new,newC)
            
        # Effacer les données des zones de texte
        self.refresh_champ()


class Bouton_Mvote(QWidget):
    def __init__(self,bd,type_m="Approbation",l=200,h=80):
        """
        Constructeur de la classe Bouton_Mvote qui descend de la classe QWidget.

        Args:
            bd (Base_donnee): Base de données utilisée pour générer les candidats et la map
            type_m (str): Nom de la méthode de vote à afficher sur le bouton
            l (int): Longueur des widgets. Par défaut, 200
            h (int): Hauteur des widgets. Par défaut, 80
        
        Returns:
            void
        """
        super().__init__()
        self.bd= bd
        self.h = h
        self.l = l
        self.setFixedSize(self.l, self.h)
        self.map=self.bd.map
        self.type_m = type_m
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
        """
        Méthode qui calcule le vainqueur suivant la méthode de vote choisie.

        Returns:
            void
        """
        if self.type_m == type1: #Copeland
            self.bd.refresh_MV([normalise_Ind(self.map.Copeland(),1)])
            
        elif self.type_m == type2: #Borda
            self.bd.refresh_MV([normalise_Ind(self.map.Borda(),1)])
            
        elif self.type_m == type3: #Pluralite
            self.bd.refresh_MV([normalise_Ind(self.map.Pluralite(),1)])
            
        elif self.type_m == type4: #STV
            self.bd.refresh_MV([normalise_Ind(self.map.STV(),1)])
            
        else : #Approbation
            self.bd.refresh_MV([normalise_Ind(self.map.Approbation(3),1)])

class Boutoun_GenerAleatoire(QWidget):
    def __init__(self,bd,l,h):
        """
        Constructeur de la classe Boutoun_GenerAleatoire qui descend de la classe QWidget.

        Args:
            bd (Base_donnee): Base de données utilisée pour générer les candidats et la map
            l (int): Longueur des widgets.
            h (int): Hauteur des widgets.
        
        Returns:
            void
        """
        super().__init__()
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
        """
        Méthode qui génère un candidat aléatoirement.

        Returns:
            void
        """
        cd = self.bd.genere_aleatoire_candidat_BM()
        nom =cd.nom()
        prenom = cd.prenom()
        valeurs=[cd.charisme(),int(cd.x()),int(cd.y())]
        
        new = normalise_button( nom,prenom,valeurs)
        newC = normalise_button_C( nom,prenom,valeurs)
        self.bd.ajoute(new,newC)

class BoutonIO(QWidget):
    def __init__(self,bd,nom,l=200,h=80):
        """
        Constructeur de la classe BoutonIO qui descend de la classe QWidget.

        Args:
            bd (Base_donnee): Base de données utilisée pour générer les candidats et la map
            nom (str): Nom affiché sur le bouton
            l (int): Longueur des widgets. Par défaut, 200
            h (int): Hauteur des widgets. Par défaut, 80
        
        Returns:
            void
        """
        super().__init__()
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
        self.io_button = QPushButton(self.nom)
        self.io_button.clicked.connect(self.save_text)
        layout.addWidget(self.io_button)

    def save_text(self):
        """
        Méthode qui sauvegarde les données dans un fichier ou charge les données d'un fichier.

        Returns:
            voids
        """
        #show_loading_dialog()
        text = self.text_edit.text()
        if self.nom == "recharge":
            print("Texte Chargé :", text,"\n")
            self.bd.recharge(text)
        else :
            self.bd.save(text)
            print("Texte sauvegardé :", text,"\n")
        self.text_edit.clear()  # Efface le texte après sauvegarde

class BoutonRecharge(BoutonIO):
    def __init__(self, bd, l=200, h=80):
        """
        Constructeur de la classe BoutonRecharge qui descend de la classe BoutonIO.

        Args:
            bd (Base_donnee): Base de données utilisée pour générer les candidats et la map
            l (int): Longueur des widgets. Par défaut, 200
            h (int): Hauteur des widgets. Par défaut, 80
        
        Returns:
            void
        """
        super().__init__(bd, "recharge", l, h)
        
class BoutonSave(BoutonIO):
    def __init__(self, bd, l=200, h=80):
        """
        Constructeur de la classe BoutonSave qui descend de la classe BoutonIO.

        Args:
            bd (Base_donnee): Base de données utilisée pour générer les candidats et la map
            l (int): Longueur des widgets. Par défaut, 200
            h (int): Hauteur des widgets. Par défaut, 80

        Returns:
            void
        """
        super().__init__(bd, "save", l, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BoutonIO()
    widget.show()
    sys.exit(app.exec())

    
"""def refresh_MV(self, new):
        # Créer un dictionnaire des points existants pour une recherche plus efficace
        existing_points = {name: (color, score, position) for name, color, score, position in self.points}
        
        # Liste pour stocker les points mis à jour
        updated_points = []

        # Mettre à jour les scores des candidats existants avec ceux fournis dans la liste new
        for name, color, score, position in new:
            if name in existing_points:
                # Si le point existe, mettre à jour son score avec celui fourni dans la liste new
                color, _, _ = existing_points[name]
                updated_points.append((name, color, score, position))
                # Retirer le point de existing_points pour marquer qu'il a été traité
                del existing_points[name]

        # Ajouter les points restants de la liste existante sans les modifier
        for name, (color, score, position) in existing_points.items():
            updated_points.append((name, color, score, position))

        # Mettre à jour la liste de points avec les nouveaux et les anciens points mis à jour
        self.refresh_ListPoint(updated_points)"""