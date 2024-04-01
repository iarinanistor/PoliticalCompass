from PySide6.QtGui import QColor
import logging
from Front.Utilitaire import *
from Back.Candidat import Candidat

def test_generate_unique_colors():
    # Test with two integers
    color = generate_unique_colors(10, 20)
    assert isinstance(color, QColor)

def test_normalise_button():
    # Test with a name, a surname, and a list
    nom = "John"
    prenom = "Doe"
    candidat = Candidat("John", "Doe", 50, 30, 10, 20)
    result = normalise_button(nom, prenom, [candidat.charisme(), candidat.x(), candidat.y()])
    assert isinstance(result, tuple)
    assert len(result) == 4
    assert isinstance(result[1], QColor)

def test_normalise_button_C():
    # Test with a name, a surname, and a list containing charisma, x, and y
    nom = "John"
    prenom = "Doe"
    candidat = Candidat("John", "Doe", 50, 30, 10, 20)
    result = normalise_button_C(nom, prenom, [candidat.charisme(), candidat.x(), candidat.y()])
    assert isinstance(result, tuple)
    assert len(result) == 5
    assert isinstance(result[1], str)
    assert isinstance(result[2], int)
    assert isinstance(result[3], int)
    assert isinstance(result[4], int)

def test_normalise_Ind():
    # Test with a candidate object and a score
    candidat = Candidat("John", "Doe", 50, 30, 10, 20)
    score = 5
    result = normalise_Ind(candidat, score)
    assert isinstance(result, tuple)
    assert len(result) == 4
    assert isinstance(result[1], QColor)
    assert result[2] == score

def test_normalise_rechargement():
    # Test with a list of candidate objects without scores
    candidats = [
        Candidat("John", "Doe", 50, 30, 10, 20),
        Candidat("Alice", "Smith", 60, 35, 15, 25)
    ]
    result = normalise_rechargement(candidats)
    assert isinstance(result, list)
    assert len(result) == len(candidats)
    assert all(isinstance(item, tuple) for item in result)
    assert all(len(item) == 4 for item in result)

def test_normalise_Ind_Mult():
    # Test with a list of candidate objects with indexes
    candidats = [
        Candidat("John", "Doe", 50, 30, 10, 20),
        Candidat("Alice", "Smith", 60, 35, 15, 25)
    ]
    result = normalise_Ind_Mult(candidats)
    assert isinstance(result, list)
    assert len(result) == len(candidats)
    assert all(isinstance(item, tuple) for item in result)
    assert all(len(item) == 4 for item in result)
