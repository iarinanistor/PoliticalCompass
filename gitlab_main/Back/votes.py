import numpy as np
from copy import deepcopy
import math

def distance(point1, point2):
    '''
    Calcule la distance entre deux points dans un espace multidimensionnel.

    Args:
        point1 (np.ndarray): Les coordonnées du premier point.
        point2 (np.ndarray): Les coordonnées du deuxième point.

    Returns:
        float: La distance entre les deux points.
    '''
    distance = np.linalg.norm(point1- point2)
    return distance

def F(x, y, xi, yi, wi):
    """
    Calcule la distance entre deux points prenant en compte la popularité/charisme du candidat/parti.

    Args:
    x (float): valeur x du premier point.
    y (float): valeur y du premier point.
    xi (float): valeur xi du deuxieme point.
    yi (float): valeur y1 du deuxieme point.
    wi (float): La valeur de wi, représentant la popularité/charisme du candidat/parti du deuxieme point.

    Returns:
    float: La valeur de la fonction F(x, y) prenant en compte la popularité/charisme du candidat/parti.
    """
    return math.exp(-4 * math.log(2) * ((x - xi)**2 - (y - yi)**2) / (wi**2)) 



def un_seul_vainqueur(vainqueurs):
    '''
    Parameters:
        vainqueurs : List[Candidat]
    Returns:
        Candidat: le candidat le plus agee et le plus charismatic
    '''
    return max(vainqueurs, key = lambda x : (x.age(), x.charisme())) 

def comptage_majorite(electeurs) :
    ''' 
    Paramaters:
        electeurs : List[Individus] 
    Returns:
        int : la majorite d'une liste contenant n elements
    '''
    nb_electeurs = len(electeurs)
    return nb_electeurs//2 + 1


def is_majority(n,electeurs) :
    '''
    Parameters:
        n:int
        electeurs : List[Individus]
    Returns:
        bool : true si n est plus grand que la moitie de longueur de liste d'electeurs
    '''
    nb_electeurs = 0
    for elec in electeurs:
        nb_electeurs += elec.poids
    return n > (nb_electeurs/2)


def comptage_votes(candidats,electeurs):
    ''' 
    Parameters:
        candidats : List[Candidat] 
        electeurs : List[Individus]
    Returns:
        Dict{Candidat:int} : dictionnaire avec chaque candidat et son nb de votes-etant le premier classe
         
    '''
    nb_votes = {candidate:0 for candidate in candidats}

    for electeur in electeurs :
        nb_votes[(electeur.liste_vote())[0]] += electeur.poids

    return nb_votes


def pluralite(candidats,electeurs):
    '''
    Parameters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
    Returns:
        Candidat : le candidat gagnant par la regle de vote PLURALITE
                    les critere de departage : age, charisme
    '''
    nb_votes = comptage_votes(candidats,electeurs)
    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]
    return un_seul_vainqueur(vainqueurs)

def borda(candidats,electeurs):
    '''
    Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
    Returns:    
        Candidat : le candidat gagnant par la regle de vote BORDA
        les criteres de departage : age, charisme
    '''
    nb_votes = {candidate:0 for candidate in candidats}
    n = len(candidats)

    for electeur in electeurs :
        for i in range(n):
            nb_votes[electeur.liste_vote()[i]] += (n-1-i)*electeur.poids

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]

    return un_seul_vainqueur(vainqueurs)


def stv(candidats, electeurs):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
    Returns:    
        Candidat : le candidat gagnant par la regle de vote STV
        les criteres de departage : age, charisme
    '''
    
    l_candidat = deepcopy(candidats)
    l_electeur = electeurs
    dico = {electeur: electeur.liste_vote() for electeur in l_electeur}
    max_iteration =len(candidats)-1

    for i in range (max_iteration):
        nb_votes = comptage_votes(l_candidat, l_electeur)
        for candidate, votes in nb_votes.items():
            if is_majority(votes, l_electeur):
                return candidate
            
        candidate_elimine = min(nb_votes, key=nb_votes.get)
        
        for electeur in electeurs:
            dico[electeur].remove(candidate_elimine)
        l_candidat.remove(candidate_elimine)
    return max(nb_votes, key=nb_votes.get)

def approbation(candidats, electeurs, nb_approbation):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
        nb_approbation : int
    Returns:    
        Candidat : le candidat gagnant par la regle de vote APPROBATION avec les nb_approbation premiers canddiats clasees
        les criteres de departage : age, charisme
    '''
    nb_votes = {candidate: 0 for candidate in candidats}

    for electeur in electeurs:
        for i in range(nb_approbation):
            votes = electeur.liste_vote()
            if i < len(votes):  # Vérifier si la liste des votes contient suffisamment de candidats
                nb_votes[votes[i]] += electeur.poids

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate, score in nb_votes.items() if score == max_vote]

    return un_seul_vainqueur(vainqueurs)

def liste_approbation(candidats,votant):
    """
    Retourne une liste des candidats approuvés par un votant.

    Args:
        candidats (list): Liste des candidats.
        votant (Point): Les coordonnées du votant.

    Returns:
        list: Liste des candidats approuvés par le votant.
    """
    l=[]
    for candidat in candidats:
        if F(candidat.x(),candidat.y(),votant.x,votant.y)<=50:
            l.append(candidat)
    return l

def liste_approb_totale(candidats,votants):
    """
    Retourne une liste des candidats vainqueurs par approbation totale.

    Args:
        candidats (list): Liste des candidats.
        votants (list): Liste des votants.

    Returns:
        list: Liste des candidats vainqueurs.
    """
    nb_votes={candidats:0 for candidat in candidats}
    for votant in votants:
        l=liste_approbation(candidats,votant)
        for cand in l:
            nb_votes[cand]+=1

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]
    return un_seul_vainqueur(vainqueurs)

def battleOneToOne(candidats,electeurs):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus]
    Returns:    
        List[(Candidat,Candidat)] : liste des couple pour les duel de condorcet 
    '''
    pairs_votes = {(c1,c2):0 for c1 in candidats for c2 in candidats if c1!=c2}

    for electeur in electeurs:
        ordre_votes = electeur.liste_vote()
        for i, c1 in enumerate(ordre_votes):
            for c2 in ordre_votes[i+1:]:
                pairs_votes[(c1,c2)] += electeur.poids
    return pairs_votes

def vainqueurCondorcet(candidats,electeurs):
    """
    Retourne le vainqueur selon le critère de Condorcet.

    Args:
        candidats (list): Liste des candidats.
        electeurs (list): Liste des électeurs.

    Returns:
        any: Le candidat vainqueur selon le critère de Condorcet, ou None s'il n'y en a pas.
    """
    pairs_votes = battleOneToOne(candidats,electeurs)
    for candidat in candidats:
        gagne = 0
        for opponent in candidats:
            if candidat != opponent:
                if pairs_votes[(candidat,opponent)] <= pairs_votes[(opponent,candidat)]:
                    gagne = 1
                    break
        if gagne == 0 :
            return candidat
    return None

def copeland(candidats,electeurs):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
        nb_approbation : int
    Returns:    
        Candidat : le candidat gagnant par la regle de vote APPROBATION avec les nb_approbation premiers canddiats clasees
        les criteres de departage : age, charisme
    '''
    nb_votes = {candidate:0 for candidate in candidats}
    pairs_votes = battleOneToOne(candidats,electeurs)
    for candidat in candidats:
        for opponent in candidats:
            if candidat != opponent:
                if pairs_votes[(candidat,opponent)] > pairs_votes[(opponent,candidat)]:
                    nb_votes[candidat] +=1
                if pairs_votes[(candidat,opponent)] == pairs_votes[(opponent,candidat)]:
                    nb_votes[candidat] +=1
    max_vote = max(nb_votes.values())
    vainqueurs = [candidat for candidat,score in nb_votes.items() if score == max_vote]
    return un_seul_vainqueur(vainqueurs)

def simpson(candidats,electeurs):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
        nb_approbation : int
    Returns:    
        Candidat : le candidat gagnant par la regle de vote APPROBATION avec les nb_approbation premiers canddiats clasees
        les criteres de departage : age, charisme
    '''
    nb_loss = {candidate:0 for candidate in candidats}
    pairs_votes = battleOneToOne(candidats,electeurs)
    for candidat in candidats:
        li = []
        for opponent in candidats:
            if candidat != opponent:
                if pairs_votes[(candidat,opponent)] < pairs_votes[(opponent,candidat)]:
                    li.append(pairs_votes[(opponent,candidat)])
        nb_loss[candidat] = max(li)
    min_loss = max(nb_loss.values())
    vainqueurs = [candidat for candidat,score in nb_loss.items() if score == min_loss]
    return un_seul_vainqueur(vainqueurs)