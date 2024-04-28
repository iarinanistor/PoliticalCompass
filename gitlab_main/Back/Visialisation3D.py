import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from Back.Map import Map
from PySide6.QtCore import QThread, Signal

def projection_3D(map):
    """
    Affiche un graphique de surface 3D représentant la répartition des poids sur une grille, basée sur un objet Map.

    Cette méthode calcule les hauteurs cumulées de chaque individu positionné dans la grille, et affiche ces données
    sous forme d'une surface 3D.

    :param map: Objet Map contenant les individus avec leurs coordonnées et poids.
    """
    # Initialisation de la matrice des hauteurs basée sur la taille de la grille dans l'objet map
    taille_x = taille_y = map.generationX  # Utilisation des attributs de l'objet map pour définir la taille de la grille
    hauteurs = np.zeros((taille_x, taille_y))  # Matrice des hauteurs initialisée à zéro

    # Accumulation des poids des individus dans la matrice des hauteurs
    for individu in map.L_population:
        if individu is not None:  # Vérification que l'individu existe
            hauteurs[individu.y, individu.x] += sum(individu.poids)  # Ajout des poids à la hauteur correspondante

    # Préparation des axes x et y pour le graphique
    x = np.arange(hauteurs.shape[1])
    y = np.arange(hauteurs.shape[0])
    x, y = np.meshgrid(x, y)  # Création des grilles de coordonnées pour les axes x et y

    # Configuration et affichage du graphique 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, hauteurs, cmap='viridis', edgecolor='none')  # Création de la surface 3D
    fig.colorbar(surf, shrink=0.5, aspect=5)  # Ajout d'une barre de couleur pour visualiser les hauteurs
    ax.set_xlabel('X')  # Étiquette de l'axe X
    ax.set_ylabel('Y')  # Étiquette de l'axe Y
    ax.set_zlabel('Hauteur')  # Étiquette de l'axe des hauteurs
    ax.set_title('Surface 3D des Individus')  # Titre du graphique
    plt.show()

def visualiser_surface_3d(map):
    """
    Visualise une surface 3D lisse en utilisant une interpolation polynomiale à partir des données des individus dans l'objet map.

    Cette fonction extrait les coordonnées et les poids de chaque individu, effectue une interpolation pour lisser la surface,
    et affiche le résultat sous forme d'une surface 3D colorée.

    :param map: Objet Map contenant la liste des individus avec leurs coordonnées et poids.
    """
    individus = map.L_population  # Accès à la liste des individus dans l'objet map
    # Extraction des coordonnées x, y et des poids (hauteurs) de chaque individu
    x = np.array([individu.x for individu in individus if individu is not None])
    y = np.array([individu.y for individu in individus if individu is not None])
    hauteurs = np.array([sum(individu.poids) for individu in individus if individu is not None])

    qualité = 100  # Définition de la résolution de la grille d'interpolation
    
    xi = np.linspace(x.min(), x.max(), qualité)
    yi = np.linspace(y.min(), y.max(), qualité)
    xi, yi = np.meshgrid(xi, yi)  # Création des grilles de coordonnées pour l'interpolation

    zi = griddata((x, y), hauteurs, (xi, yi), method='cubic')  # Interpolation cubique pour lisser la surface

    # Configuration et affichage du graphique 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none')  # Création de la surface 3D lisse
    fig.colorbar(surf, shrink=0.5, aspect=5)  # Ajout d'une barre de couleur
    ax.set_xlabel('X')  # Étiquette de l'axe X
    ax.set_ylabel('Y')  # Étiquette de l'axe Y
    ax.set_zlabel('Hauteur')  # Étiquette de l'axe des hauteurs
    ax.set_title('Surface 3D lisse des Individus')  # Titre du graphique
    plt.show()

class VisualisationThread(QThread):
    """
    Thread dédié à la visualisation de données 3D. Ce thread gère l'extraction et l'interpolation des données
    pour ne pas bloquer l'interface utilisateur pendant les calculs.

    :param map: Objet Map contenant les données à visualiser
    """
    dataReady = Signal(object, object, object)  # Signal émis avec les données prêtes pour la visualisation

    def __init__(self, map):
        super().__init__()
        self.map = map  # Référence à l'objet Map

    def run(self):
        try:
            individus = self.map.L_population
            if not individus:
                print("Aucun individu disponible.")
                return
            x = np.array([individu.x for individu in individus if individu is not None])
            y = np.array([individu.y for individu in individus if individu is not None])
            hauteurs = np.array([sum(individu.poids) for individu in individus if individu is not None])

            qualité = 100
            xi = np.linspace(x.min(), x.max(), qualité)
            yi = np.linspace(y.min(), y.max(), qualité)
            xi, yi = np.meshgrid(xi, yi)

            zi = griddata((x, y), hauteurs, (xi, yi), method='cubic')
            self.dataReady.emit(xi, yi, zi)  # Émission du signal avec les données interpolées
        except Exception as e:
            print(f"Erreur lors du traitement des données : {e}")

 