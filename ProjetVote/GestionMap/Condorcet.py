def genre_combat(liste, acc):
    # Génère la liste des combats possibles entre tous les candidats
    if not liste: return acc
    tmp = liste[0]
    newacc = acc + [(tmp, i) for i in liste[1:]]
    return genre_combat(liste[1:], newacc) 

def combat(listes_listes_votes,cmb):# renvois 1 si le combat est gagner par le premier element du couple combat -1 si c'est le deuxieme 0 si egaliter.
    a=cmb[0]
    b=cmb[1]
    cpta=0
    cptb=0
    flag=0
    for liste_votes in listes_listes_votes:
        if flag == 1:
            flag = 0
        for votes in liste_votes:
            if(votes == a):
                cpta+=1
                flag=1
                break
            if(votes ==b):
                cptb+=1
                flag=1
                break 
    if cpta>cptb:
        return 1
    elif cptb>cpta:
        return -1
    else:
        return 0

def all_combat(listes_listes_votes):
    liste_candidat={}
    for candidat in listes_listes_votes[1]: # genere la liste des candidat
        liste_candidat[candidat] = 0
    
    for duel in genre_combat(listes_listes_votes[1],[]): # genere la liste des combat
        resultat=combat(listes_listes_votes,duel)
        if( resultat == 0):
            liste_candidat[duel[0]]+=1/2
            liste_candidat[duel[1]]+=1/2
        elif( resultat == 1):
            liste_candidat[duel[0]]+=1
        else:
            liste_candidat[duel[1]]+=1
    return dict(sorted(liste_candidat.items(), key=lambda item: item[1],reverse=True))
    