import sys
from Front.Utilitaire import *
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QMainWindow, QMessageBox
from PySide6.QtGui import QIcon
import logging
import matplotlib.pyplot as plt
from Back.Statistique.MonteCarlo import CreationSimulation
from Back.Candidat import Candidat
from Tournoi.TreeView import Tournoi
from Back.Visialisation3D import  VisualisationThread
from icecream import ic

#Variable global du fichier 
type1 ="Copeland" or "Copeland liquide"
type2="Borda" or "Borda liquide"
type3="Pluralite" or "Pluralite liquide"
type4="STV" or "STV liquide"
type5="Approbation" or "Approbation liquide"

# Chemin vers le fichier de style pour les widgets
fichier = "Front/Widgets/Texture/Bouton.qss"
# config LOG 
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class EntreeCandidat(QWidget):
    """
    Widget pour l'entrée des informations d'un candidat.
    
    Attributs:
        bd (BaseDeDonnees): Référence à l'objet de base de données pour ajouter des candidats.
        l (int): Largeur fixe du widget.
        h (int): Hauteur de base du widget.
        tailleMap (int): Taille maximale pour les valeurs de position X et Y du candidat.
    """
    def __init__(self,bd,l=200,h=80,taille_map=500):
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
        
        nom_boutons = ["Charisme :", "   X :", "  Y :"]
        for i in range(3):  # Trois champs d'entier  côte à côte
            label = QLabel(nom_boutons[i])
            edit = QSpinBox()
            # Vous pouvez définir d'autres limites si nécessaire
            edit.setMinimum(0)
            if i == 0:
                edit.setMaximum(100)
            else:
                edit.setMaximum(taille_map)
            valeurs_layout.addWidget(label)
            valeurs_layout.addWidget(edit)
            self.valeur_edits.append(edit)  # Ajouter le bouton à la liste
        
        layout.addLayout(valeurs_layout)
        
        # Bouton pour soumettre les informations
        submit_button = QPushButton("Soumettre")
        submit_button.clicked.connect(self.ajouter_informations)
        layout.addWidget(submit_button)
        
        self.setLayout(layout)

    def refresh_champ(self):
        """ Réinitialise les champs du formulaire. """
        self.nom_edit.clear()
        self.prenom_edit.clear()
        
        for edit in self.valeur_edits:
            edit.clear()
            
    def ajouter_informations(self):
        """ Ajoute les informations du candidat dans la base de données après validation. """
        
        logging.info("<Gestion des Boutons de soumission de Candidat>")
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        valeurs = [edit.value() for edit in self.valeur_edits]
        if nom != "" and prenom != "" :# Utiliser la liste self.valeur_edits
            logging.info('          Informations soumises - Nom: {}, Prenom: {}, Valeurs entieres: {}.'.format(nom, prenom, valeurs))
            print("Nom:", nom)
            print("Prénom:", prenom)
            print("Valeurs entières:", valeurs)
            charisme,x,y = valeurs
            x = x if x<=100 else 100
            y = y if y<=100 else 100
            self.bd.ajoute(Candidat(nom,prenom,charisme,20,x,y))
        logging.info("<Fin Gestion des Boutons de soumission de Candidat>")    
        # Effacer les données des zones de texte
        self.refresh_champ()


class Bouton_Mvote(QWidget):
    """
    Widget pour gérer les règles de vote spécifiques.

    Attributs:
        bd (BaseDeDonnees): Référence à l'objet de base de données pour manipuler les résultats de vote.
        type_m (str): Type de méthode de vote (par défaut "Approbation").
        rayon (int): Rayon applicable à certaines méthodes de vote.
        l (int): Largeur fixe du widget.
        h (int): Hauteur fixe du widget.
    """
    def __init__(self,bd,type_m="Approbation",rayon=None,l=200,h=95):
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
        """
        Gère les actions à effectuer lorsque le bouton est cliqué. Désactive le bouton,
        applique le type de vote spécifié et réactive le bouton une fois l'action terminée.
        """

        logging.info("<Gestion des Boutons des regles de vote>")
        logging.info('          Bouton {} clique.'.format(self.type_m))
        
        self.button.setEnabled(False)
        if self.type_m == type1:
            self.bd.refresh_MV([(self.map.Copeland(self.rayon),1)])
            
        elif self.type_m == type2:
            self.bd.refresh_MV([(self.map.Borda(self.rayon),1)])
            
        elif self.type_m == type3:
            self.bd.refresh_MV([(self.map.Pluralite(self.rayon),1)])
            
        elif self.type_m == type4:
            self.bd.refresh_MV([(self.map.STV(self.rayon),1)])
            
        else :
            self.bd.refresh_MV([(self.map.Approbation(3,self.rayon),1)])
        logging.info("<Fin Gestion des Boutons des regles de vote>")
        self.button.setEnabled(True)

class Boutoun_GenerAleatoire(QWidget):
    """
    Widget pour générer et ajouter un candidat aléatoire à la base de données.

    Attributs:
        bd (BaseDeDonnees): Référence à l'objet de base de données pour ajouter des candidats.
        l (int): Largeur fixe du widget.
        h (int): Hauteur fixe du widget.
    """
    def __init__(self,bd,l,h):
        super().__init__()
        self.setStyleSheet(open(fichier).read())
        self.h = h
        self.l = l
        self.setFixedSize(self.l, self.h)
        self.bd = bd
        ic(bd,"button genere alteatoire")
        layout = QVBoxLayout()
        
        # Créer un bouton
        self.button = QPushButton("Générer un Candidat")
        
        # Connecter un signal à une fonction lorsque le bouton est cliqué
        self.button.clicked.connect(self.on_button_clicked)
        
        # Ajouter le bouton au layout
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
    # Fonction appelée lorsque le bouton est cliqué
    def on_button_clicked(self):
        """
        Gère les actions à effectuer lorsque le bouton est cliqué. Désactive le bouton,
        génère un candidat aléatoire et l'ajoute à la base de données, puis réactive le bouton.
        """
        self.button.setEnabled(False)
        candidat = self.bd.genere_aleatoire_candidat_BM()
        self.bd.ajoute(candidat)
        self.button.setEnabled(True)

class BoutonMC(QPushButton):
    """
    Bouton pour lancer la simulation Monte Carlo
    """
    def __init__(self, bd, type_vote, texte):
        super().__init__(texte)
        self.bd = bd
        self.type_vote = type_vote

        # Connecter le signal clicked à la méthode on_button_clicked
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        """
        Désactive le bouton pour empêcher des clics multiples pendant l'exécution de la simulation, lance la simulation Monte Carlo 
        en utilisant les paramètres spécifiés (la carte et le type de vote), affiche les résultats de la simulation, puis réactive le bouton.
        """
        self.setEnabled(False)  # Désactiver le bouton pendant l'exécution
        print("Start")
        hitmap = CreationSimulation(self.bd.map, 5, self.type_vote)
        print("Finish")
        hitmap.show()
        self.setEnabled(True)  # Réactiver le bouton après l'exécution

class BoutonVisuel3D(QPushButton):
    """
    Bouton pour initier la visualisation 3D de données sur une carte.

    Ce bouton permet de lancer une visualisation tridimensionnelle de la population sur une carte,
    utilisant la méthode de visualisation 3D pour afficher les données de manière interactive.

    Attributs:
        bd (BaseDeDonnees): Référence à l'objet de base de données qui contient la carte utilisée pour la visualisation.
        map (Map): Carte associée à la base de données, sur laquelle la population est visualisée.
        thread (VisualisationThread): Fil d'exécution utilisé pour la visualisation 3D sans bloquer l'interface utilisateur.
    """
    def __init__(self, bd):
        """
        Initialise le bouton avec un texte, stocke la référence à la base de données, prépare la carte pour la visualisation,
        et connecte le bouton à la méthode qui gérera son action lorsqu'il sera cliqué.
        S'assure également que la population est créée sur la carte si elle n'existe pas déjà.
        """
        super().__init__("Visualisation 3D")
        self.bd = bd
        self.map = self.bd.map
        if self.map.L_population is None or []: self.map.creer_L_population()
        self.clicked.connect(self.on_button_clicked)
        self.thread = None

    def on_button_clicked(self):
        """"
        Vérifie si le fil de visualisation est inactif ou inexistant, et le démarre si c'est le cas.
        Connecte le fil de visualisation à une méthode d'affichage qui sera appelée une fois les données prêtes.
        """
        if self.thread is None or not self.thread.isRunning():
            self.thread = VisualisationThread(self.map)
            self.thread.dataReady.connect(self.display_plot)
            self.thread.start()

    def display_plot(self, xi, yi, zi):
        """
        Affiche les données de la population en 3D lorsque les données sont prêtes.
        En cas d'erreur lors de la visualisation, une exception est capturée et un message d'erreur est affiché.

        Args:
            xi, yi, zi: Coordonnées des points à afficher sur le graphique 3D.
        """
        try:
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, shrink=0.5, aspect=5)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Hauteur')
            ax.set_title('Surface 3D lisse des Individus')
            plt.show()
        except Exception as e:
            print(f"Erreur lors de l'affichage : {e}")
                   
class BoutonTournoi(QPushButton):
    """
    Bouton pour initier l'affichage d'un tournoi sous forme d'arbre à partir des données des électeurs.

    Ce bouton lance une représentation graphique d'un tournoi, utilisée pour visualiser la compétitions
    sous forme d'arbre de décision où chaque nœud représente une rencontre entre candidats.

    Attributs:
        bd (BaseDonnees): Référence à l'objet de base de données qui contient toutes les informations nécessaires, incluant la carte et la liste des électeurs.
        liste (list): Liste des électeurs qui participent au tournoi.
        tr (Tournoi): Instance de la classe Tournoi qui gère la logique du tournoi.
        tournament_window (QMainWindow): Fenêtre principale qui affiche le tournoi.
    """
    def __init__(self, bd):
        """
        Initialise le bouton avec un texte descriptif, stocke la référence à la base de données, et prépare la liste des électeurs.
        Connecte également le bouton à la méthode qui gérera son action lorsqu'il sera cliqué.
        """
        super().__init__("Arbre tournoi")
        self.bd = bd
        self.liste= self.bd.map.liste_electeur
        # Connecter le signal clicked à la méthode on_button_clicked
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        """
        Appelée lors du clic sur le bouton. Lance la logique de préparation et d'affichage du tournoi,
        puis force une mise à jour de l'affichage pour éviter les problèmes de rendu graphique.
        """
        self.launch_tournament()
        self.tr.view.update()# obligatoire sinon la fentre s'affiche en noir
         
    def launch_tournament(self):
        """
        Prépare et lance l'affichage du tournoi. Crée une nouvelle fenêtre pour visualiser l'arbre du tournoi,
        initialise les composants nécessaires, et affiche la fenêtre.
        """
        if len(self.liste) > 1:
            self.tr = Tournoi(self.bd.map,self.liste)
            self.tournament_window = QMainWindow()
            self.tournament_window.setWindowTitle("Tournoi")
            self.tournament_window.setCentralWidget(self.tr.view)
            self.tournament_window.show()
        else:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Erreur")
            error_msg.setText("Pas assez de candidats pour inclure un tricheur.")
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setStyleSheet("QLabel { color: white; } QPushButton { color: black; }")
            error_msg.exec_()
        
class BoutonIO(QWidget):
    """
    Widget général pour les opérations d'entrée/sortie, capable de gérer à la fois le chargement et la sauvegarde des données.

    Attributs:
        bd (BaseDonnees): Référence à l'objet de base de données pour effectuer des opérations de chargement et de sauvegarde.
        nom (str): Détermine le type d'opération ("recharge" pour le chargement, "save" pour la sauvegarde).
        l (int): Largeur fixe du widget.
        h (int): Hauteur fixe du widget.
    """
    def __init__(self,bd,nom,l=200,h=80):
        """
        Widget général pour les opérations d'entrée/sortie, capable de gérer à la fois le chargement et la sauvegarde des données.

        Attributs:
            bd (BaseDeDonnees): Référence à l'objet de base de données pour effectuer des opérations de chargement et de sauvegarde.
            nom (str): Détermine le type d'opération ("recharge" pour le chargement, "save" pour la sauvegarde).
            l (int): Largeur fixe du widget.
            h (int): Hauteur fixe du widget.
        """
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
            self.io_button = QPushButton(" Recharger")
            self.io_button.setIcon(QIcon("images/icons/cil-cloud-upload.png"))
        else:
            self.io_button = QPushButton(" Sauvegarder")
            self.io_button.setIcon(QIcon("images/icons/cil-cloud-download.png"))
        self.io_button.clicked.connect(self.save_text)
        layout.addWidget(self.io_button)

    def save_text(self):
        """
        Exécute l'opération de chargement ou de sauvegarde en fonction du mode du widget.
        Désactive le bouton pendant l'opération pour éviter les doubles cliques, puis réactive après l'opération.
        """
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
    """
    Sous-classe de BoutonIO configurée spécifiquement pour les opérations de chargement des données.
    """
    def __init__(self, bd, l=200, h=80):
        super().__init__(bd, "recharge", l, h)
        
class BoutonSave(BoutonIO):
    """
    Sous-classe de BoutonIO configurée spécifiquement pour les opérations de sauvegarde des données.
    """
    def __init__(self, bd, l=200, h=80):
        super().__init__(bd, "save", l, h)
