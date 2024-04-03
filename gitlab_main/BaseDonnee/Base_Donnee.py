from Front.Windows.MWindow import MainWindow
from Back.Map import *
from Back.Candidat import *
from Front.Utilitaire import *
import logging
# Configurer le système de journalisation
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
class Base_donnee():
    def __init__(self, id, window=None,tailleMap=500):
        """
        Constructeur de la classe Base_donnee.

        Args:
            id (int): Identifiant de la base de données.
            window (MainWindow): Fenêtre principale associée à la base de données. Par défaut, None.
            tailleMap (int): Taille de la carte. Par défaut, 500.
        """
        self.id = id
        self.map = Map(self, str(id), [], [], tailleMap, tailleMap)
        self.map.creer_L_population()
        self.window = window
        
    
    def refresh(self,NormaliserCandidat):
        """
        Méthode pour rafraîchir la fenêtre principale avec des candidats normalisés.

        Args:
            NormaliserCandidat (list): Liste des candidats normalisés à afficher.
        """
        logging.info("<Rafraichissement interface>")
        logging.info("  Rafraichissement de l'interface utilisateur effectue avec succes.")
    
        self.window.refresh(NormaliserCandidat)
        logging.info("<Fin de rafraichissement de l'interface>")
    
    def ajoute(self,new,newC):
        """
        Méthode pour ajouter un nouvel élément et un nouveau candidat à la base de données.

        Args:
            new: Nouvel élément à ajouter.
            newC: Nouveau candidat à ajouter.
        """
        logging.info("<Ajout bd>")
        logging.info("  Ajout d'un nouvel element a windows.")
        self.window.ajouteElement(new) 
        logging.info("  Ajout d'un nouvel element a la candidats.")
        self.map.ajoute_candidat(newC)
        logging.info("<Fin ajout bd>")
    
    def genere_aleatoire_candidat_BM(self): # genere aleatoirement un Candidat de la Classe Candidiat
        """
        Méthode pour générer aléatoirement un candidat de la classe Candidiat.

        Returns:
            Candidat: Nouveau candidat généré aléatoirement.
        """
        logging.debug("Generation aleatoire d\'un candidat.")
        return Candidat.random_candidat(self.window.tailleMap,self.window.tailleMap)
    
    def refresh_MV(self,l):
        """
        Méthode pour rafraîchir la liste de résultats.

        Args:
            l (list): Liste des résultats à afficher.
        """
        logging.info("<Rafraichissement carte>")
        logging.info("  Rafraichissement de la vue de la carte effectue avec succes.")
        self.window.listePoint.refresh_MV(l)
        logging.info("</Rafraichissement carte>")
        
    def save(self,fichier):
        """
        Méthode pour sauvegarder la carte dans un fichier.

        Args:
            fichier (str): Chemin du fichier de sauvegarde.
        """
        logging.info("<Sauvegarde>")
        logging.info("  Sauvegarde des donnees dans le fichier {}.".format(fichier))
    
        self.map.ecrire(fichier)
        logging.info("<Fin sauvegarde>")
        
    def recharge(self,ficher):
        """
        Méthode pour recharger la carte à partir d'un fichier.

        Args:
            fichier (str): Chemin du fichier à charger.
        """
        logging.info("<Rchargement>")
        logging.info("  Rechargement des donnees a partir du fichier {}.".format(ficher))
        
        self.map.chargement(ficher)
        liste = self.map.liste_electeur
        self.window.refresh(normalise_rechargement(liste))
        
        logging.info("<Fin Rechargement>")

        
    @staticmethod
    def creer(id,tailleMap=500,Pl=False,map=None):
        """
        Méthode statique pour créer une nouvelle instance de Base_donnee.

        Args:
            id (int): Identifiant de la base de données.
            tailleMap (int): Taille de la carte. Par défaut, 500.

        Returns:
            Base_donnee: Nouvelle instance de Base_donnee créée.
        """
        if map is None:
            new = Base_donnee(id,tailleMap)
            # création de la map du Back
            new.map.generationAleatoire()
        else : new = map
        
        # création de la window
        window = MainWindow(new, tailleMap,Pl)
        # affectation 
        new.window = window
        logging.info("Creation d'une nouvelle base de donnees avec ID {}.".format(id))
        return new

