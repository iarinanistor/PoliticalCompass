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
    assert individu.nom == ['John']
    assert individu.x == 5
    assert individu.y == 5
    assert individu.liste_electeur == []
    assert individu.poids == [1]
    assert [0] <= individu.c <= [1]
    assert individu.adelegue == [False]

def test_get_c(individu):
    assert 0 <= individu.get_c() <= 1

@pytest.fixture
def setup_individus():
    candidat1 = Candidat("Dupont", "Jean", 20, 45, 0, 0)
    candidat2 = Candidat("Martin", "Louis", 10, 30, 10, 5)
    candidat3 = Candidat("Bernard", "Gabriel", 15, 35, 20, 10)
    groupe = Individus("Groupe1", 0, 0, [candidat1, candidat2, candidat3])
    return groupe

def test_liste_vote_avec_electeurs(setup_individus):
    result = setup_individus.liste_vote()
    assert len(result) == 3
    assert result[0]._nom == "Bernard"
    assert result[1]._nom == "Martin"
    assert result[2]._nom == "Dupont"

def test_liste_vote_avec_liste_vide():
    groupe_vide = Individus("Groupe2", 5, 5)
    result = groupe_vide.liste_vote()
    assert result == None


if __name__ == "__main__":
    pytest.main()
