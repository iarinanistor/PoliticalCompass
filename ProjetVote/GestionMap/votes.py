
import bib_objet as ob

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
    return n > (len(electeurs)/2)

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
        nb_votes[(electeur.liste_vote())[0]] += 1

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
            nb_votes[electeur.liste_vote()[i]] += n-1-i

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]

    return un_seul_vainqueur(vainqueurs)

def stv(candidats,electeurs):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
    Returns:    
        Candidat : le candidat gagnant par la regle de vote STV
        les criteres de departage : age, charisme
    '''

    l_candidat = candidats
    l_electeur = electeurs
    while True :
        nb_votes = comptage_votes(l_candidat,l_electeur)

        for candidate,votes in nb_votes.items():
            if is_majority(votes,l_electeur):
                return candidate
            
        candidate_elimine = min(nb_votes, key = nb_votes.get)
        
        for electeur in l_electeur :
            (electeur.liste_vote()).remove(candidate_elimine)
        l_candidat.remove(candidate_elimine)
        


def approbation(candidats,electeurs,nb_approbation):
    '''Paramaters:
        candidats : List[Candidat] 
        electeurs : List[Individus] 
        nb_approbation : int
    Returns:    
        Candidat : le candidat gagnant par la regle de vote APPROBATION avec les nb_approbation premiers canddiats clasees
        les criteres de departage : age, charisme
    '''
    nb_votes = {candidate:0 for candidate in candidats}

    for electeur in electeurs :
        for i in range(nb_approbation):
            nb_votes[electeur.liste_vote()[i]] += 1
        """a changer apres : la liste des candidats que l'electeur a choisi (ordonnee)"""
        """ il peut etre un attribut ou le resultat d'une methode"""

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]
    
    return un_seul_vainqueur(vainqueurs)

