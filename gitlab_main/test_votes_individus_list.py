from random import uniform
from Back.Map import Map
from Back.votes import *
from Back.Individus import Individus
from Back.Candidat import Candidat


#fonction pour manipuler la matrices comme une liste
def concat(matrix):
    '''
    Parameters:
        matrix : list[liste[x]]
    Returns:
        liste[x] : la concatenation des listes dans la matrice
    '''
    l = []
    for i in range(len(matrix)):
        l+=matrix[i]
    return l

def affiche_candidat(candidat):
    '''
    Parameters:
        candidat : Candidat
    Returns:
        void : l'affichage d'un candidat
    '''
    print(candidat.nom()+" "+candidat.prenom()+" age:"+str(candidat.age())+" charisme:"+str(candidat.charisme()))


#generation des candidats et population : un petit echantillon pour tester les fonctions


cand1 = Candidat("Martin","chloe",4,50,60,60)
cand2 = Candidat("Grand","Nathan",5,46,42,55)
cand3 = Candidat("Petit","John",3,42,15,15)
l_candidats = [cand1,cand2,cand3]
ind1 =Individus("1",10,10,l_candidats)
ind2 =Individus("2",50,50,l_candidats)
ind3 =Individus("3",75,75,l_candidats)

population=[[ind1,ind2,ind3]]

map=Map(None,"France",l_candidats,population)
listes_ordonnees = map.listes_listes_votes()

print('Listes ordonnnes des candidats pour chaque votant:\n')
for list_ord in listes_ordonnees:
    for candidat in list_ord:
        affiche_candidat(candidat)
    print('\n')

votants = concat(population)
#pour ind1 : Petit John, Grand Nathan et Martin Chloe
#pour ind2 : Grand Nathan, Martin Chloe et Petit John
#pour ind3 : Martin Chloe, Grand Nathan et Petit John
    
"""on veut tester les methodes des votes pour la nouvelle version des individus
les nouveaux individus ont une liste des poids et une liste de competences
ca signifie que un individu ne represente pas une seule personne
maintenant, un individu represente plusieurs personnes places sur la meme case
"""
print(str(' Test modalites de vote:\n').upper())

#les asserts ont ete teste avec la liste des candidats ordonne par la distance euclidienne et pas par la fonction F

print("##########PLURALITE##########")


vainqueur_pluralite = pluralite(l_candidats,votants)
#assert(vainqueur_pluralite==cand1)
print('1.Test pluralite avant ajout des poids:')
affiche_candidat(vainqueur_pluralite)

#on ajoute un autre electeur place dans la meme case que ind2 avec la poids 1 et la competence choisi par une loi uniforme entre 0 et 1
print(ind2.poids)
print(ind2.nom)
print(ind2.c)
ind2.poids.append(1)
ind2.c.append(uniform(0,1))

vainqueur_pluralite = pluralite(l_candidats,votants)
#assert(vainqueur_pluralite==cand2)
print('1.Test pluralite apres ajout des poids:')
affiche_candidat(vainqueur_pluralite)

ind2.poids.pop()
ind2.c.pop()


print('\n')
print("##########BORDA##########")

vainqueur_borda = borda(l_candidats,votants)
#assert(vainqueur_borda==cand2)
print('1.Test Borda avant ajout des poids:')
affiche_candidat(vainqueur_borda)

ind3.poids.append(1)
ind3.c.append(uniform(0,1))



vainqueur_borda = borda(l_candidats,votants)
#assert(vainqueur_borda==cand1)
print('1.Test Borda apres ajout des poids:')
affiche_candidat(vainqueur_borda)

ind3.poids.pop()
ind3.c.pop()


print('\n')
print("##########APPROBATION##########")
print('on teste avec les 2 premiers acceptes')
vainqueur_approbation = approbation(l_candidats,votants,2)
#assert(vainqueur_approbation==cand2)
print('1.Test Approbation avant ajout des poids:')
affiche_candidat(vainqueur_approbation)

ind3.poids.append(1)
ind3.c.append(uniform(0,1))


vainqueur_approbation = approbation(l_candidats,votants,2)
#assert(vainqueur_approbation==cand2)
print('1.Test Approbation apres ajout des poids:')
affiche_candidat(vainqueur_approbation)

ind3.poids.pop()
ind3.c.pop()


print('\n')
print("##########APPROBATION PAR DISTANCE##########")
vainqueur_approbation_dist = liste_approb_totale(l_candidats,votants)
#assert(vainqueur_approbation_dist==cand1)
print('1.Test Approbation Distance avant ajout des poids:')
affiche_candidat(vainqueur_approbation_dist)

ind3.poids.append(1)
ind3.c.append(uniform(0,1))



vainqueur_approbation_dist = liste_approb_totale(l_candidats,votants)
#assert(vainqueur_approbation_dist==cand1)
print('1.Test Approbation Distance apres ajout des poids:')
affiche_candidat(vainqueur_approbation)

ind3.poids.pop()
ind3.c.pop()


print('\n')
print("##########COPELAND##########")
vainqueur_copeland = copeland(l_candidats,votants)  
#assert(vainqueur_copeland==cand2)
print('1.Test Copeland avant ajout des poids:')
affiche_candidat(vainqueur_copeland)

ind3.poids.append(1)
ind3.c.append(uniform(0,1))


vainqueur_copeland = copeland(l_candidats,votants)
#assert(vainqueur_copeland==cand1)
print('1.Test Copeland apres ajout des poids:')
affiche_candidat(vainqueur_copeland)

ind3.poids.pop()
ind3.c.pop()


print('\n')
print("TEST STV A FAIRE!!!!!!!!!!")


















