from Back.Map import Map
from Back.Candidat import Candidat
from Back.Individus import Individus
from icecream import ic

# Fonction pour manipuler la matrice comme une liste
def concat(matrix):
    '''
    Parameters:
        matrix : list[liste[x]]
    Returns:
        liste[x] : la concatenation des listes dans la matrice
    '''
    l = []
    for i in range(len(matrix)):
        l += matrix[i]
    return l

def affiche_candidat(candidat):
    '''
    Parameters:
        candidat : Candidat
    Returns:
        void : l'affichage d'un candidat
    '''
    print(candidat.nom()+" "+candidat.prenom()+" age:"+str(candidat.age())+" charisme:"+str(candidat.charisme()))

# Génération des candidats et population : un petit échantillon pour tester les fonctions
l_candidats = Candidat.generate_candidats(4, 10, 10)
population = [
    [Individus("1", 10, 10, l_candidats), Individus("2", 0, 0, l_candidats)],
    [Individus("3", 5, 5, l_candidats), Individus("quatre", 2, 3, l_candidats), Individus("cinq", 1, 8, l_candidats)]
]
map = Map(None, "France", l_candidats, population)

listes_ordonnees = map.listes_listes_votes()

print('Listes ordonnées des candidats pour chaque votant:\n')
for list_ord in listes_ordonnees:
    for candidat in list_ord:
        affiche_candidat(candidat)
    print('\n')

votants = concat(population)
print(str(' Test modalités de vote:\n').upper())

try:
    print('1.Test pluralité:')
    vainqueur_pluralite = map.Pluralite()
    affiche_candidat(vainqueur_pluralite)
    print('#############################################')
except Exception as e:
    ic(e)  # Utilisation de IceCream pour imprimer les détails de l'exception

try:
    print('2.Test Borda:')
    vainqueur_borda = map.Borda()
    affiche_candidat(vainqueur_borda)
    print('#############################################')
except Exception as e:
    ic(e)  # Utilisation de IceCream pour imprimer les détails de l'exception

try:
    print('3.Test Approbation:')
    print('\tI. 2 premiers sont acceptés')
    v1_app = map.Approbation(2)
    affiche_candidat(v1_app)
    print('\tII. 3 premiers sont acceptés')
    v2_app = map.Approbation(3)
    affiche_candidat(v2_app)
    print('#############################################')
except Exception as e:
    ic(e)  # Utilisation de IceCream pour imprimer les détails de l'exception

try:
    print('4.Test STV:')
    vainqueur_stv = map.STV()
    affiche_candidat(vainqueur_stv)
    print('#############################################')
except Exception as e:
    ic(e)  # Utilisation de IceCream pour imprimer les détails de l'exception

print('FIN TESTS_MÉTHODES DE VOTES')
