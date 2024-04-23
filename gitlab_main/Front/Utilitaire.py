from PySide6.QtGui import QColor
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_unique_colors(int1, int2):
    """
    Génère une couleur unique en fonction de deux entiers donnés.
    
    Utilise une combinaison des deux entiers pour calculer les composantes RGB de la couleur.
    Ceci est utile pour attribuer une couleur distinctive à chaque candidat basée sur des attributs uniques.
    
    Args:
        int1 (int): Premier entier.
        int2 (int): Deuxième entier.
        
    Returns:
        QColor: Couleur générée à partir des deux entiers.
    """
    logging.info('<generate_unique_colors> int1: {}, int2: {}'.format(int1, int2))

    r = int(int1)*(13) % 256
    g = int(int2)*(13) % 256
    b = int(int1* int2) % 256
    return QColor(r, g, b)

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
    logging.info('<normalise_button> nom: {}, prenom: {}, liste: {}'.format(nom, prenom, liste))

    x, y = liste[1], liste[2]
    return (nom + " " + prenom, generate_unique_colors(x, y), 0, (x, y))

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
    logging.info('<normalise_button_C> nom: {}, prenom: {}, liste: {}'.format(nom, prenom, liste))

    charisme, x, y = liste[0], liste[1], liste[2]
    return (nom, prenom, charisme, x, y)

def normalise_Ind(ind, score):
    """
    Normalise un individu avec un score.
    
    Args:
        ind (Individual): Objet représentant un individu.
        score (int): Score associé à l'individu.
        
    Returns:
        tuple: Tuple contenant le nom complet, la couleur générée, le score, et un tuple des coordonnées.
    """
    logging.info('<normalise_Ind> ind: {}, score: {}'.format(ind, score))

    return (ind.nom() + " " + ind.prenom(), generate_unique_colors(ind.x(), ind.y()), score, (ind.x(), ind.y()))

def normalise_rechargement(liste):
    """
    Normalise une liste d'individus sans score.
    
    Args:
        liste (list): Liste d'objets représentant des individus.
        
    Returns:
        list: Liste normalisée des individus avec des scores mis à zéro.
    """
    logging.info('<normalise_rechargement> liste: {}'.format(liste))

    tmp = []
    for i in range(len(liste)):
        tmp.append(normalise_Ind(liste[i], 0))
    return tmp

def normalise_Ind_Mult(l):
    """
    Normalise une liste d'individus avec des index.
    
    Args:
        l (list): Liste d'objets représentant des individus.
        
    Returns:
        list: Liste normalisée des individus avec des index ajoutés.
    """
    logging.info('<normalise_Ind_Mult> l: {}'.format(l))

    tmp = []
    for i in range(len(l)):
        tmp.append(normalise_Ind(l[i], i + 1))
    return tmp
