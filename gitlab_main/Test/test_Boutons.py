from unittest.mock import MagicMock
import pytest
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from Front.Widgets.Boutons import EntreeCandidat
from Front.Widgets.Boutons import*
# Mock de la base de données
class MockDatabase:
    def ajoute(self, *args):
        pass
    
@pytest.fixture
def app(qtbot):
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication([])
    yield test_app
    test_app.quit()
    
@pytest.fixture
def mock_bd():
    return MagicMock()

@pytest.fixture
def entree_candidat(qtbot):
    # Initialisation de la classe avec une base de données mockée
    ec = EntreeCandidat(MockDatabase())
    qtbot.addWidget(ec)
    yield ec

def test_afficher_informations(entree_candidat):

            
    entree_candidat.bd.ajoute = MagicMock()

    # Paramétrer les valeurs des champss
    entree_candidat.nom_edit.setText("John")
    entree_candidat.prenom_edit.setText("Doe")
    entree_candidat.valeur_edits[0].setValue(50)
    entree_candidat.valeur_edits[1].setValue(100)
    entree_candidat.valeur_edits[2].setValue(200)

    # Appeler la méthode à tester
    entree_candidat.ajouter_informations()

    # Vérifier si la méthode bd.ajoute a été appelée 
    assert entree_candidat.bd.ajoute.called == True


def test_refresh_champ(entree_candidat):
    entree_candidat.nom_edit.setText("John")
    entree_candidat.prenom_edit.setText("Doe")
    entree_candidat.valeur_edits[0].setValue(50)
    entree_candidat.valeur_edits[1].setValue(100)
    entree_candidat.valeur_edits[2].setValue(200)

    entree_candidat.refresh_champ()

    assert entree_candidat.nom_edit.text() == ""
    assert entree_candidat.prenom_edit.text() == ""
    assert all(edit.value() == 0 for edit in entree_candidat.valeur_edits)

def test_on_button_clicked_Mvote():
    # Créer une instance de Bouton_Mvote avec un MagicMock pour bd
    mock_bd = MagicMock()
    mock_nom = MagicMock()
    mock_x = MagicMock()
    bouton = Bouton_Mvote(mock_bd, type_m="Approbation", rayon=None, l=200, h=95)
    
    # Appeler la méthode on_button_clicked
    bouton.on_button_clicked()
    
    # Vérifier si la méthode refresh_MV de bd a été appelée avec les bonnes valeurs
    assert mock_bd.refresh_MV.call_count == 1
    
def test_on_button_clicked(mock_bd):
    # Créer une instance de BoutonGenerAleatoire avec un MagicMock pour bd
    bouton = Boutoun_GenerAleatoire(mock_bd, l=200, h=95)
    
    # Appeler la méthode on_button_clicked
    bouton.on_button_clicked()
    
    # Vérifier si la méthode ajoute de bd a été appelée
    assert mock_bd.ajoute.called

def test_save_text_recharge(monkeypatch, mock_bd):
    # Créer une instance de BoutonRecharge avec un MagicMock pour bd
    bouton_recharge = BoutonRecharge(mock_bd, l=200, h=95)
    
    # Modifier le texte dans le QLineEdit
    new_text = "test.txt"
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: new_text)
        bouton_recharge.text_edit.setText(new_text)
        bouton_recharge.save_text()
    
    # Vérifier si la méthode recharge de bd a été appelée avec le bon texte
    mock_bd.recharge.assert_called_once_with(new_text)

def test_save_text_save(monkeypatch, mock_bd):
    # Créer une instance de BoutonSave avec un MagicMock pour bd
    bouton_save = BoutonSave(mock_bd, l=200, h=95)
    
    # Modifier le texte dans le QLineEdit
    new_text = "test.txt"
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: new_text)
        bouton_save.text_edit.setText(new_text)
        bouton_save.save_text()
    
    # Vérifier si la méthode save de bd a été appelée avec le bon texte
    mock_bd.save.assert_called_once_with(new_text)
