def un_seul_vainqueur(vainqueurs):
    '''vainqueurs : List[Candidat] -> Candidat
        retourne le candidat le plus agee et le plus charismatic
    '''
    return max(vainqueurs, key = lambda x : (x.age, x.charisme)) 

def comptage_majorite(electeurs) :
    ''' electeurs : List[Electeur] -> int
        retourne la majorite d'une liste contenant n elements
    '''
    nb_electeurs = len(electeurs)
    return nb_electeurs//2 + 1 

def comptage_votes(candidats,electeurs):
    ''' candidats : List[Candidat] electeurs : List[Electeur] -> Dict{Candidat:int}
        retourne une dictionnaire avec chaque candidat et son nb de votes
    '''
    nb_votes = {candidate:0 for candidate in candidats}

    for electeur in electeurs :
        nb_votes[electeur.liste_a_completer[0]] += 1
        """a changer apres : la liste des candidats que l'electeur a choisi (ordonnee)"""
        """ il peut etre un attribut ou le resultat d'une methode"""

    return nb_votes

def pluralite(candidats,electeurs):
    '''candidats : List[Candidat] electeurs : List[Electeur] -> Candidat
        retourne le candidat gagnant par la regle de vote PLURALITE
        les critere de departage : age, charisme
    '''
    nb_votes = comptage_votes(candidats,electeurs)
    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]
    return un_seul_vainqueur(vainqueurs)

def borda(candidats,electeurs):
    '''candidats : List[Candidat] electeurs : List[Electeur] -> Candidat
        retourne le candidat gagnant par la regle de vote BORDA
        les critere de departage : age, charisme
    '''
    nb_votes = {candidate:0 for candidate in candidats}
    n = len(candidats)

    for electeur in electeurs :
        for i in range(n):
            nb_votes[electeur.liste_a_completer[i]] += n-1-i
        """a changer apres : la liste des candidats que l'electeur a choisi (ordonnee)"""
        """ il peut etre un attribut ou le resultat d'une methode"""

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]

    return un_seul_vainqueur(vainqueurs)

def stv(candidats,electeurs):
    '''candidats : List[Candidat] electeurs : List[Electeur] -> Candidat
        retourne le candidat gagnant par la regle de vote STV
        les critere de departage : age, charisme
    '''

    majorite = comptage_majorite(electeurs)

    while True :
        nb_votes = comptage_votes(candidats,electeurs)

        for candidate,votes in votes.items():
            if votes >= majorite :
                return candidate
            
        candidate_elimine = min(nb_votes, key = nb_votes.get)
        
        for electeur in electeurs :
            (electeur.liste_a_completer).remove(candidate_elimine)
        """a changer apres : la liste des candidats que l'electeur a choisi (ordonnee)"""
        """ il peut etre un attribut ou le resultat d'une methode"""


def approbation(candidats,electeurs):
    '''candidats : List[Candidat] electeurs : List[Electeur] -> Candidat
        retourne le candidat gagnant par la regle de vote APPROBATION
        les critere de departage : age, charisme
    '''
    nb_votes = {candidate:0 for candidate in candidats}

    for electeur in electeurs :
        nb_approbation = electeur.approb 
        '''si on ajoute une attribut dans la classe electeur et aussi une contraine qu'elle soit <= len(candidats)'''
        for i in range(nb_approbation):
            nb_votes[electeur.liste_a_completer[i]] += 1
        """a changer apres : la liste des candidats que l'electeur a choisi (ordonnee)"""
        """ il peut etre un attribut ou le resultat d'une methode"""

    max_vote = max(nb_votes.values())
    vainqueurs = [candidate for candidate,score in nb_votes.items() if score == max_vote]
    
    return un_seul_vainqueur(vainqueurs)

