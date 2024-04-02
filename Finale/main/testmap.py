import unittest
from unittest.mock import patch
from io import *
from Back.Map import Map
import os

class TestMap(unittest.TestCase):

    def setUp(self):
        self.test_map = Map(bd=None, nom="Test Map", liste_electeur=[], population=[], generationX=5, generationY=5)

    def tearDown(self):
        del self.test_map

    def test_distance(self):
        point1 = [0, 0]
        point2 = [3, 4]
        self.assertEqual(self.test_map.distance(point1, point2), 5.0)

    def test_generation(self):
        self.test_map.generation()
        self.assertEqual(len(self.test_map.population), 5)
        self.assertEqual(len(self.test_map.population[0]), 5)

    def test_generationAleatoire(self):
        with patch('random.random', side_effect=[0.1]):
            self.test_map.generationAleatoire()
            self.assertEqual(len(self.test_map.population), 5)
            self.assertEqual(len(self.test_map.population[0]), 5)

    def test_genereCand(self):
        with patch('random.random', side_effect=[0.3]):
            result = self.test_map.genereCand('Test', ['A', 'B', 'C'], 0, 3)
            self.assertEqual(result.nom, 'Test')
            self.assertIn(result.x, range(4))
            self.assertIn(result.y, range(4))

    def test_generationTest(self):
        with patch('random.random', side_effect=[0.3]):
            self.test_map.generationTest(0, 3)
            self.assertEqual(len(self.test_map.population), 5)
            self.assertEqual(len(self.test_map.population[0]), 5)

    def test_listes_listes_votes(self):
        self.test_map.generation()
        result = self.test_map.listes_listes_votes()
        self.assertEqual(len(result), 25)

    def test_Copeland(self):
        self.test_map.generation()
        result = self.test_map.Copeland()
        self.assertIsNotNone(result)

    def test_Copeland_MC(self):
        self.test_map.generation()
        result = self.test_map.Copeland_MC()
        self.assertIsNotNone(result)

    def test_Pluralite(self):
        self.test_map.generation()
        result = self.test_map.Pluralite()
        self.assertIsNotNone(result)

    def test_Borda(self):
        self.test_map.generation()
        result = self.test_map.Borda()
        self.assertIsNotNone(result)

    def test_STV(self):
        self.test_map.generation()
        result = self.test_map.STV()
        self.assertIsNotNone(result)

    def test_Approbation(self):
        self.test_map.generation()
        result = self.test_map.Approbation(3)
        self.assertIsNotNone(result)

    def test_ecrire_lire(self):
        self.test_map.generation()
        self.test_map.ecrire("test_file.txt")
        candidats, population = self.test_map.lire("test_file.txt")
        self.assertEqual(len(candidats), 0)
        self.assertEqual(len(population), 25)

        os.remove("test_file.txt")

    def test_liste_to_matrice(self):
        self.test_map.generation()
        self.test_map.liste_to_matrice()
        self.assertEqual(len(self.test_map.population), 5)
        self.assertEqual(len(self.test_map.population[0]), 5)

    def test_chargement(self):
        self.test_map.generation()
        self.test_map.ecrire("test_file.txt")

        new_map = Map(bd=None, nom="Test Map", liste_electeur=[], population=[], generationX=5, generationY=5)
        new_map.chargement("test_file.txt")
        self.assertEqual(len(new_map.population), 5)
        self.assertEqual(len(new_map.population[0]), 5)

        os.remove("test_file.txt")

if __name__ == '__main__':
    unittest.main()
