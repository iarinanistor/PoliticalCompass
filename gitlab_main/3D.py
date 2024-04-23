import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from random import uniform
from Back.Map import Map

def projection_3D(map): # affiche le graphique 
    # Création de la matrice de hauteur
    taille_x = taille_y = map.generationX # Taille de la grille
    hauteurs = np.zeros((taille_x, taille_y))

    for individu in map.L_population:
        if individu is not None:
            # Somme des poids pour la hauteur
            hauteurs[individu.y, individu.x] += sum(individu.poids)

    # Grilles pour les axes x et y
    x = np.arange(hauteurs.shape[1])
    y = np.arange(hauteurs.shape[0])
    x, y = np.meshgrid(x, y)

    # Visualisation
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, hauteurs, cmap='viridis', edgecolor='none')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Hauteur')
    ax.set_title('Surface 3D des Individus')
    plt.show()
    
def visualiser_surface_3d(map): # affichage par interpolation polynomial
    """
    Visualise une surface 3D lisse basée sur une liste d'objets Individus.
    
    :param map: objet Map
    """
    individus = map.L_population
    # Extraction des coordonnées x, y et des hauteurs (somme des poids)
    x = np.array([individu.x for individu in individus])
    y = np.array([individu.y for individu in individus])
    hauteurs = np.array([sum(individu.poids) for individu in individus])

    # Création de grilles pour l'interpolation
    qualité = 100 # plus la qualité est haute plus les temps de calcule seront important 
    
    xi = np.linspace(x.min(), x.max(), qualité)
    yi = np.linspace(y.min(), y.max(), qualité)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolation pour lisser la surface
    zi = griddata((x, y), hauteurs, (xi, yi), method='cubic')

    # Création du graphique
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none', rstride=1, cstride=1, alpha=None, antialiased=True)

    # Ajout d'une barre de couleur pour la hauteur
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # Configuration des étiquettes des axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Hauteur')
    ax.set_title('Surface 3D lisse des Individus')
    plt.show()
 
if __name__ == '__main__':
    a="Triangulaire"
    b="Uniforme"
    c="Exponentiel"
    d="Beta"   


    pop = [[None]*100]*100 # obligatoire pour creer la matrice
    nbIndividus = 10000 # mettre un grand nombre d'individus pour avoir une meilleur vision de la generation , attetion temps de calcule important pour  la genereration
    map = Map(None,population=pop,generationX=100,generationY=100)
    map.generation_pers((49,50,50),d,nbIndividus) # generation de la population
    print("fin generation")
    map.creer_L_population()# creation de la liste 
    visualiser_surface_3d(map)


 