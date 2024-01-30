from Candidat import *


def pluralite(liste_candidats,liste_electeur):
    liste_zero=[0]*len(liste_candidats)
    nb_votes = dict(zip(liste_candidats,liste_zero))
    for electeur in liste_electeur:
        """a changer apres : la liste des candidats que l'electeur a choisi (ordonnee)"""
        """ il peut etre un attribut ou le resultat d'une methode"""
        candidat_prefere = liste_a_completer[0]
        nb_votes[candidat_prefere] += 1
    candidat_gagnant = max(nb_votes,key=nb_votes.get) 
    """on va le change pour prendre en compte l'age ou le charisme s'il ya plusieurs / on peut utiliser les exceptions"""
    return candidat_gagnant

def borda(liste_candidats,liste_electeur):
    liste_zero=[0]*len(liste_candidats)
    nb_votes = dict(zip(liste_candidats,liste_zero))
    n = len(liste_candidats)
    for electeur in liste_electeur:
        """a changer apres la liste ordonne des candidats votee par un electeur"""
        for i in range(n):
            nb_votes[liste_a_completer[i]] += n-1-i
    candidat_gagnant = max(nb_votes,key=nb_votes.get)
    return candidat_gagnant    

def stv()    