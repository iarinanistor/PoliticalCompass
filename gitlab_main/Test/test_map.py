import pytest
import numpy as np
import random
from unittest.mock import patch, MagicMock
from Back.Map import Map
from Back.Candidat import Candidat
from Back.Individus import Individus

@pytest.fixture
def sample_map():
    # Créer une carte de test avec des paramètres arbitraires
    candidat1 = Candidat("Dupont", "Jean", 80, 35, 2, 2)
    candidat2 = Candidat("Martin", "Marie", 70, 42, 7, 7)
    candidat3 = Candidat("Bernard", "Pierre", 90, 28, 5, 5)
    sample_map = Map(bd=None, nom="Sample Map", liste_electeur=[candidat1, candidat2, candidat3], population=[], generationX=8, generationY=8)
    sample_map.creer_L_population()
    return sample_map

def test_distance(sample_map):
    # Tester la méthode de calcul de la distance entre deux points
    point1 = np.array([1, 1])
    point2 = np.array([4, 5])
    assert sample_map.distance(point1, point2) == 5

def test_ajoute_candidat(sample_map):
    # Tester l'ajout d'un candidat à la liste des candidats
    sample_map.ajoute_candidat(Candidat("John", "Doe", 50, 45, 2, 3))
    assert len(sample_map.liste_electeur) == 4
    assert sample_map.liste_electeur[-1].nom() == "John"
    assert sample_map.liste_electeur[-1].prenom() == "Doe"
    assert sample_map.liste_electeur[-1].charisme() == 50
    assert sample_map.liste_electeur[-1].age() == 45
    assert sample_map.liste_electeur[-1].x() == 2
    assert sample_map.liste_electeur[-1].y() == 3

def test_liste_to_matrice(sample_map):
    # Tester la conversion de la liste de population en matrice de population
    sample_map.L_population = [Individus("John", 0, 0, sample_map.liste_electeur),
                               Individus("Jane", 1, 1, sample_map.liste_electeur)]
    sample_map.liste_to_matrice()
    assert len(sample_map.population) == 8  # Vérifier la taille de la matrice
    assert sample_map.population[0][0].nom == ['John']  # Vérifier si le premier individu est correctement placé
    assert sample_map.population[1][1].nom == ['Jane']  # Vérifier si le deuxième individu est correctement placé

def test_generation(sample_map):
    # Tester la méthode de génération de population linéaire
    sample_map.generation()
    assert len(sample_map.population) == sample_map.generationX  # Vérifier le nombre de lignes
    assert len(sample_map.population[0]) == sample_map.generationY  # Vérifier le nombre de colonnes
    # Vérifier si les éléments sont bien des instances d'Individus
    assert all(isinstance(ind, Individus) for row in sample_map.population for ind in row)

def test_generationAleatoire(sample_map):
    # Tester la méthode de génération de population aléatoire
    sample_map.generationAleatoire()
    assert len(sample_map.population) == sample_map.generationX  # Vérifier le nombre de lignes
    assert len(sample_map.population[0]) == sample_map.generationY  # Vérifier le nombre de colonnes
    # Vérifier si les éléments sont bien des instances d'Individus
    assert all(isinstance(ind, Individus) for row in sample_map.population for ind in row)

def test_refresh_Candidat(sample_map):
    # Tester la méthode refresh_Candidat
    # Ajouter quelques candidats à la liste des électeurs
    sample_map.liste_electeur.append(Candidat("John", "Doe", 5, 20, 2, 3))
    sample_map.liste_electeur.append(Candidat("Jane", "Smith", 7, 25, 4, 5))
    # Rafraîchir la liste des électeurs dans la population
    sample_map.refresh_Candidat()
    # Vérifier si tous les individus de la population ont la même liste d'électeurs que la liste principale
    for row in sample_map.population:
        for ind in row:
            assert ind.liste_electeur == sample_map.liste_electeur

def test_genereCand(sample_map):
    # Tester la méthode genereCand
    nom = "Test"
    liste = []
    dbt = 0
    fin = 8
    # Générer un individu avec genereCand
    test_individu = sample_map.genereCand(nom, liste, dbt, fin)
    # Vérifier si l'individu généré a les bonnes coordonnées et la bonne liste d'électeurs
    assert test_individu.nom == ['Test']
    assert test_individu.liste_electeur == liste
    assert dbt <= test_individu.x <= fin
    assert dbt <= test_individu.y <= fin

def test_refresh_Candidat(sample_map):
    # Tester la méthode refresh_Candidat
    # Ajouter quelques candidats à la liste des électeurs
    sample_map.liste_electeur.append(Candidat("John", "Doe", 5, 20, 2, 3))
    sample_map.liste_electeur.append(Candidat("Jane", "Smith", 7, 25, 4, 5))
    # Rafraîchir la liste des électeurs dans la population
    sample_map.refresh_Candidat()
    # Vérifier si tous les individus de la population ont la même liste d'électeurs que la liste principale
    for row in sample_map.population:
        for ind in row:
            assert ind.liste_electeur == sample_map.liste_electeur

def test_genere_L_Cand(sample_map):
    # Tester la méthode genere_L_Cand
    # Ajouter quelques candidats à la liste principale des électeurs
    sample_map.liste_electeur.append(Candidat("John", "Doe", 5, 20, 2, 3))
    sample_map.liste_electeur.append(Candidat("Jane", "Smith", 7, 25, 4, 5))
    # Générer la liste des candidats à partir de la carte
    sample_map.genere_L_Cand()
    # Vérifier si la liste des électeurs a été correctement mise à jour dans la population
    for row in sample_map.population:
        for ind in row:
            assert ind.liste_electeur == sample_map.liste_electeur

def test_creer_L_population(sample_map):
    # Tester la méthode creer_L_population
    # Générer la liste de population à partir de la carte
    sample_map.creer_L_population()
    # Vérifier si la liste de population a été correctement mise à jour
    assert len(sample_map.L_population) == 0

def test_listes_listes_votes(sample_map):
    # Appel de la fonction à tester
    result = sample_map.listes_listes_votes()
    
    # Vérification de la taille de la liste retournée
    assert len(result) == 0
    
    # Vérification du contenu de la liste retournée
    for sublist in result:
        assert isinstance(sublist, list)  # Vérifie que chaque élément est une liste
        for vote in sublist:
            assert isinstance(vote, int)  # Vérifie que chaque élément de la liste est un entier (vote)

# Test pour la fonction Copeland
def test_Copeland(sample_map):
    result = sample_map.Copeland()
    assert isinstance(result, Candidat)  # Le résultat devrait être une chaîne de caractères représentant le gagnant de Copeland

# Test pour la fonction Pluralite
def test_Pluralite(sample_map):
    result = sample_map.Pluralite()
    assert isinstance(result, Candidat)  # Le résultat devrait être une chaîne de caractères représentant le gagnant de Pluralite

# Test pour la fonction Borda
def test_Borda(sample_map):
    result = sample_map.Borda()
    assert isinstance(result, Candidat)  # Le résultat devrait être une chaîne de caractères représentant le gagnant de Borda

# Test pour la fonction Approbation
def test_Approbation(sample_map):
    nb_approbation = 5  # Nombre de votes d'approbation pour le test
    result = sample_map.Approbation(nb_approbation)
    assert isinstance(result, Candidat)  # Le résultat devrait être une chaîne de caractères représentant le gagnant d'Approbation

def test_delegation_empty_list():
    assert Map.delegation([]) is None, "Aucun électeur à déléguer devrait retourner None"

def test_delegation_single_elector():
    electeur = Individus()
    result = Map.delegation([electeur])
    assert result is electeur, "Un seul électeur devrait recevoir le vote"

def test_delegation_different_competence():
    # Créer des électeurs avec des compétences différentes
    electeurs = [Individus() for _ in range(5)]
    for i, electeur in enumerate(electeurs):
        electeur.c[0] = i  # Directement modifier la liste pour ajuster la compétence

    # Tester plusieurs fois pour voir si l'électeur avec la plus haute compétence est souvent choisi
    selections = [Map.delegation(electeurs) for _ in range(1000)]
    most_common = max(set(selections), key=selections.count)

    assert most_common == electeurs[-1], "L'électeur avec la plus haute compétence devrait être choisi le plus fréquemment"

# Test pour la fonction liste_poids
def test_liste_poids(sample_map):
    rayon = 5  # Rayon pour le test
    result = sample_map.liste_poids(rayon)
    # Assurez-vous que le résultat est bien une liste
    assert isinstance(result, list)
    # Assurez-vous que tous les éléments de la liste sont des objets de type Individus
    assert all(isinstance(ind, Individus) for ind in result)

def test_candidat_prefere_cand1_prefered(sample_map):
    cand1 = sample_map.liste_electeur[0]  # Obtenir le premier candidat
    cand2 = sample_map.liste_electeur[1]  # Obtenir le second candidat
    # Simuler des poids spécifiques pour les votes
    sample_map.L_population = [
        MagicMock(poids=[10], liste_vote=MagicMock(return_value=[cand1, cand2])), 
        MagicMock(poids=[5], liste_vote=MagicMock(return_value=[cand2, cand1]))
    ]
    assert sample_map.candidat_prefere(cand1, cand2) == cand1

def test_candidat_prefere_cand2_prefered(sample_map):
    cand1 = sample_map.liste_electeur[0]  # Obtenir le premier candidat
    cand2 = sample_map.liste_electeur[1]  # Obtenir le second candidat
    # Simuler des poids inversés pour les votes
    sample_map.L_population = [
        MagicMock(poids=[5], liste_vote=MagicMock(return_value=[cand1, cand2])), 
        MagicMock(poids=[10], liste_vote=MagicMock(return_value=[cand2, cand1]))
    ]
    assert sample_map.candidat_prefere(cand1, cand2) == cand2


def test_generate_matches_empty():
    """ Test avec une liste vide. """
    assert Map.generate_matches([]) == []

def test_generate_matches_single_element():
    """ Test avec un seul élément. """
    assert Map.generate_matches([1]) == []

def test_generate_matches_two_elements():
    """ Test avec deux éléments. """
    assert Map.generate_matches([1, 2]) == [(1, 2)]

def test_generate_matches_multiple_elements():
    """ Test avec plusieurs éléments. """
    assert Map.generate_matches([1, 2, 3]) == [(1, 2), (1, 3), (2, 3)]

def test_generate_matches_non_numeric():
    """ Test avec des éléments non numériques. """
    assert Map.generate_matches(['a', 'b', 'c']) == [('a', 'b'), ('a', 'c'), ('b', 'c')]

def test_generate_matches_Candidat():
    candidat1 = Candidat("Dupont", "Jean", 80, 35, 2, 2)
    candidat2 = Candidat("Martin", "Marie", 70, 42, 7, 7)
    candidat3 = Candidat("Bernard", "Pierre", 90, 28, 5, 5)
    liste_electeur=[candidat1, candidat2, candidat3]
    assert Map.generate_matches(liste_electeur) == [(liste_electeur[0], liste_electeur[1]), 
                                                    (liste_electeur[0], liste_electeur[2]), 
                                                    (liste_electeur[1], liste_electeur[2])]

def test_contraite_tournoi(sample_map):
    assert sample_map.contraite_tournoi() == {sample_map.liste_electeur[0].id : [sample_map.liste_electeur[1].id, sample_map.liste_electeur[2].id], 
                                              sample_map.liste_electeur[1].id : [sample_map.liste_electeur[2].id],
                                              sample_map.liste_electeur[2].id : []}

if __name__ == "__main__":
    pytest.main()

# WARNING : On teste les différents types de génération (Beta, Triangulaire, Exponentiel et uniforme) avec la visualisation3D
