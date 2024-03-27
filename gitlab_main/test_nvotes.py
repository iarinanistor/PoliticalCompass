from Back.Map import Map
from Back.Candidat import Candidat
from Back.Individus import Individus
from Back.votes import *


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
population=[[ind1,ind2]]
ind1.poids =1
ind2.poids = 3
map=Map(None,"France",l_candidats,population)

listes_ordonnees = map.listes_listes_votes()

print('Listes ordonnnes des candidats pour chaque votant:\n')
for list_ord in listes_ordonnees:
    for candidat in list_ord:
        affiche_candidat(candidat)
    print('\n')

votants = concat(population)
print(str(' Test modalites de vote:\n').upper())

print('1.Test pluralite:')
vainqueur_pluralite = pluralite(l_candidats,votants)
assert(vainqueur_pluralite==cand2)
affiche_candidat(vainqueur_pluralite)
print('#############################################')

print('2.Test Borda:')
vainqueur_borda = borda(l_candidats,votants)
assert(vainqueur_borda==cand2)
affiche_candidat(vainqueur_borda)
print('#############################################')

print('3.Test Approbation:')
print('\tI. 2 premiers sont acceptes')
v1_app = approbation(l_candidats,votants,2)
assert(v1_app==cand2)
affiche_candidat(v1_app)
print('\tII. 3 premiers sont acceptes')
v2_app = approbation(l_candidats,votants,3)
assert(v2_app==cand1)
affiche_candidat(v2_app)
print('#############################################')

print('4.Test Copeland:')
vainqueur_copeland = copeland(l_candidats,votants)
assert(vainqueur_copeland==cand2)
affiche_candidat(vainqueur_copeland)
print('#############################################')

"""print('4.Test STV:')
vainqueur_stv = stv(l_candidats,votants)
affiche_candidat(vainqueur_stv)
print('#############################################')

print('5.Test STV:')
vainqueur_stv1 = stv1(l_candidats,votants)
affiche_candidat(vainqueur_stv1)
print('#############################################')"""

"""print('6.Test utilite')
coef = coef_utilite(l_candidats[0],votants)
print(coef)

print('7.Test liste utilite')
liste_coef = coefs_utilite(l_candidats,votants)"""



print('FIN TESTS_METHODES DE VOTES')