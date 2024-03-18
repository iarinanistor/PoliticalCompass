from PySide6.QtGui import QColor


#Importation des bibliothèques pour calculer la consommation d'énergie et l'empreinte carbone
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

#csv_handler = CSVHandler("Conso_energie.csv")

#from Conso import csv_handler

from VarGlob import csv_handler


@measure_energy(handler=csv_handler)
def generate_unique_colors(int1, int2):
    """
    Génère une couleur unique en fonction de deux entiers donnés.
    
    Args:
        int1 (int): Premier entier.
        int2 (int): Deuxième entier.
        
    Returns:
        QColor: Couleur générée à partir des deux entiers.
    """
    # Utilisation des entiers pour calculer les composantes RGB
    r = int(int1) % 256
    g = int(int2) % 256
    b = int(int1 * int2) % 256
    return QColor(r, g, b)

@measure_energy(handler=csv_handler)
def normalise_button(nom, prenom, liste):
    """
    Normalise les informations d'un bouton.
    
    Args:
        nom (str): Nom de la personne.
        prenom (str): Prénom de la personne.
        liste (list): Liste contenant des informations supplémentaires.
        
    Returns:
        tuple: Tuple contenant le nom complet, la couleur générée, un paramètre, et un tuple des coordonnées.
    """
    x, y = liste[1], liste[2]
    return (nom + " " + prenom, generate_unique_colors(x, y), 0, (x, y))

@measure_energy(handler=csv_handler)
def normalise_button_C(nom, prenom, liste):
    """
    Normalise les informations d'un bouton avec un attribut de charisme supplémentaire.
    
    Args:
        nom (str): Nom de la personne.
        prenom (str): Prénom de la personne.
        liste (list): Liste contenant le charisme et d'autres informations.
        
    Returns:
        tuple: Tuple contenant le nom, prénom, charisme, et un tuple des coordonnées.
    """
    charisme, x, y = liste[0], liste[1], liste[2]
    return (nom, prenom, charisme, x, y)

@measure_energy(handler=csv_handler)
def normalise_Ind(ind, score):
    """
    Normalise un individu avec un score.
    
    Args:
        ind (Individual): Objet représentant un individu.
        score (int): Score associé à l'individu.
        
    Returns:
        tuple: Tuple contenant le nom complet, la couleur générée, le score, et un tuple des coordonnées.
    """
    return (ind.nom() + " " + ind.prenom(), generate_unique_colors(ind.x(), ind.y()), score, (ind.x(), ind.y()))

@measure_energy(handler=csv_handler)
def normalise_rechargement(liste):
    """
    Normalise une liste d'individus sans score.
    
    Args:
        liste (list): Liste d'objets représentant des individus.
        
    Returns:
        list: Liste normalisée des individus avec des scores mis à zéro.
    """
    tmp = []
    for i in range(len(liste)):
        tmp.append(normalise_Ind(liste[i], 0))
    return tmp

@measure_energy(handler=csv_handler) 
def normalise_Ind_Mult(l):
    """
    Normalise une liste d'individus avec des index.
    
    Args:
        l (list): Liste d'objets représentant des individus.
        
    Returns:
        list: Liste normalisée des individus avec des index ajoutés.
    """
    tmp = []
    for i in range(len(l)):
        tmp.append(normalise_Ind(l[i], i + 1))
    return tmp