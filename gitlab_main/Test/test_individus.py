import pytest
import numpy as np
from Back.Individus import Individus  # Supposons que votre classe Individus est dans un fichier nommé "individus.py"
from Back.Candidat import Candidat
from icecream import ic

# Fixtures pour les tests
@pytest.fixture
def individu():
    return Individus(nom="John", x=5, y=5, liste_electeur=[])

# Tests

def test_creation_individu(individu):
    assert isinstance(individu, Individus)
    assert individu.nom == "John"
    assert individu.x == 5
    assert individu.y == 5
    assert individu.liste_electeur == []
    assert individu.poids == 1
    assert 0 <= individu.c <= 10
    assert not individu.adelegue

def test_get_c(individu):
    assert 0 <= individu.get_c() <= 10

def test_liste_vote():
    try:
        # Création de quelques candidats de test
        candidat1 = Candidat("Dupont", "Jean", 80, 35, 2, 2)
        candidat2 = Candidat("Martin", "Marie", 70, 42, 7, 7)
        candidat3 = Candidat("Bernard", "Pierre", 90, 28, 5, 5)
        candidat4 = Candidat("Macron","Hugo",80,47,2,2)
        candidat5 = Candidat("Vincent","Victor",70,52,7,9)
        candidat6 = Candidat("Petit","Kevin",90,42,4,5)

        # Création d'un individu avec les candidats comme électeurs
        individu1 = Individus(nom="Individu1", x=5, y=5, liste_electeur=[candidat1, candidat2, candidat3])
        individu2 = Individus(nom="Individu2", x=5, y=5, liste_electeur=[candidat4, candidat5, candidat6])

        # Appel de la fonction liste_vote
        votes = individu1.liste_vote()
        votes1 = individu2.liste_vote1()

        # Vérification des résultats
        assert len(votes) == 3
        assert votes[0] == candidat3
        assert votes[1] == candidat2
        assert votes[2] == candidat1

        assert len(votes1) == 3  
        assert votes1[0] == candidat6
        assert votes1[1] == candidat4
        assert votes1[2] == candidat5

    except Exception:
        ic(individu.liste_vote)  # Utilisation de IceCream pour imprimer les détails de l'exception
        pytest.fail("Une exception s'est produite.")

if __name__ == "__main__":
    pytest.main()
