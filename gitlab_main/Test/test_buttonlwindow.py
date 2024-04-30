import pytest
import sys
from PySide6.QtCore import QPoint, QEvent, Qt
from PySide6.QtGui import QMouseEvent, QGuiApplication
from PySide6.QtWidgets import QApplication, QPushButton, QGraphicsEllipseItem, QGraphicsScene
from unittest.mock import MagicMock, create_autospec
from Front.Widgets.ButonLWindow import *

# Test class EventFilter
# La fixture 'qtbot' est fournie par pytest-qt pour interagir avec les widgets Qt
@pytest.fixture
def event_filter(qtbot):
    app = QApplication.instance() or QApplication([])
    test_widget = QPushButton("Test")
    event_filter = EventFilter()
    test_widget.installEventFilter(event_filter)
    return event_filter, test_widget

def test_mouse_press_event(event_filter):
    ef, button = event_filter
    # Create a mouse event at position (10, 10) with a left mouse button press
    event = QMouseEvent(QEvent.MouseButtonPress, QPoint(10, 10), button.mapToGlobal(QPoint(10, 10)), Qt.LeftButton, Qt.MouseButtons(Qt.LeftButton), Qt.NoModifier)
    # Assert that the event filter processes this event and blocks it as expected
    assert ef.eventFilter(button, event) == True

# Test class StartSCVButton
@pytest.fixture
def mock_scv():
    scv = MagicMock()
    scv.start = MagicMock()
    return scv

@pytest.fixture
def start_scv_button(qtbot, mock_scv):
    button = StartSCVButton(scv=mock_scv)
    qtbot.addWidget(button)
    return button, mock_scv

def test_initialization(start_scv_button):
    button, _ = start_scv_button
    assert button.button.text() == "Activer CV"
    assert "Cliquez pour activer le système de vision par ordinateur." in button.button.toolTip()

def test_button_click(start_scv_button, qtbot):
    button, mock_scv = start_scv_button
    qtbot.mouseClick(button.button, Qt.LeftButton)
    mock_scv.start.assert_called_once()

def test_event_filter(start_scv_button, qtbot):
    button, _ = start_scv_button
    qtbot.addWidget(button)
    enter_event = QEvent(QEvent.Enter)
    leave_event = QEvent(QEvent.Leave)

    button.eventFilter(button.button, enter_event)
    button.eventFilter(button.button, leave_event)

    # Vérifiez que l'animation est configurée correctement
    assert button.anim.duration() == 200
    assert isinstance(button.anim.endValue(), QRect)

# Test class MapTypeDialog
@pytest.fixture
def map_dialog(qtbot):
    dialog = MapTypeDialog()
    qtbot.addWidget(dialog)
    return dialog

def test_initial_state(map_dialog):
    """
    Teste l'état initial de la boîte de dialogue.
    """
    assert map_dialog.mapType is None
    assert map_dialog.windowTitle() == "Choix du type de map"
    assert not map_dialog.loadingLabel_3d.isVisible()
    assert not map_dialog.loadingLabel_2d.isVisible()

def test_select_map_type_3d(map_dialog, qtbot):
    """
    Teste la sélection du type de carte 3D.
    """
    with qtbot.waitSignal(map_dialog.accepted, timeout=5000):
        map_dialog.selectMapType("3D")
    print("3D Button Visible:", map_dialog.map3DButton.isVisible())
    print("3D Loading Label Visible:", map_dialog.loadingLabel_3d.isVisible())
    assert map_dialog.mapType == "3D"
    assert not map_dialog.map3DButton.isVisible()
    assert not map_dialog.loadingLabel_3d.isVisible()

def test_select_map_type_2d(map_dialog, qtbot):
    """
    Teste la sélection du type de carte 2D.
    """
    with qtbot.waitSignal(map_dialog.accepted, timeout=5000):
        map_dialog.selectMapType("2D")
    print("2D Button Visible:", map_dialog.map2DButton.isVisible())
    print("2D Loading Label Visible:", map_dialog.loadingLabel_2d.isVisible())
    assert map_dialog.mapType == "2D"
    assert not map_dialog.map2DButton.isVisible()
    assert not map_dialog.loadingLabel_2d.isVisible()

# Test class CreationButton
@pytest.fixture
def mock_premap():
    premap = MagicMock()
    premap.liste_points = []  # Commencez avec une liste vide pour tester la gestion des erreurs
    return premap

@pytest.fixture
def creation_button(qtbot, mock_premap):
    button = CreationButton(premap=mock_premap)
    qtbot.addWidget(button)
    return button, mock_premap

def test_creation_button_init(creation_button):
    button, _ = creation_button
    assert button.button.text() == "Lancer l'application"

def test_button_click_no_points(creation_button, qtbot):
    button, premap = creation_button
    with qtbot.waitSignal(button.button.clicked, timeout=100):
        qtbot.mouseClick(button.button, Qt.LeftButton)
    assert premap.liste_points == []  # Vérifie que la liste est toujours vide

def test_button_click_with_points(creation_button, qtbot, mock_premap):
    button, premap = creation_button
    premap.liste_points = ["point1", "point2"]  # Simulez des points ajoutés
    with qtbot.waitSignal(button.button.clicked, timeout=100):
        qtbot.mouseClick(button.button, Qt.LeftButton)

# Test class TypeGenerationButton
@pytest.fixture
def type_generation():
    """Provide a sample type generation tuple (name, QColor object)."""
    return ("Generation Type", QColor('blue'))

@pytest.fixture
def parent_window():
    """Mock a parent window with an attribute to set type_generation."""
    window = MagicMock()
    window.type_generation = None
    return window

@pytest.fixture
def type_gen_button(qtbot, parent_window, type_generation):
    """Fixture to create TypeGenerationButton with mock parent and type."""
    button = TypeGenerationButton(parent_window, type_generation)
    qtbot.addWidget(button)
    return button, parent_window, type_generation

def test_initialization(type_gen_button):
    """Test the initialization and UI setup of the button."""
    button, parent, type_gen = type_gen_button
    expected_color = type_gen[1].name(QColor.HexRgb)  # Get the color as a hex string
    assert button.button.text() == type_gen[0]
    assert expected_color in button.button.styleSheet()

def test_button_click_updates_parent(type_gen_button, qtbot):
    """Test that clicking the button updates the type_generation in the parent."""
    button, parent, type_gen = type_gen_button
    qtbot.mouseClick(button.button, Qt.LeftButton)
    assert parent.type_generation == type_gen  # Parent's type_generation should be updated

def test_coloration_method(type_gen_button):
    """Verify the coloration method applies the correct styles to the button."""
    button, _, _ = type_gen_button
    color = QColor('red')
    expected_color = color.name(QColor.HexRgb)  # Convert to hex string
    button.coloration(color)
    assert expected_color in button.button.styleSheet()

def test_event_filter_animations(type_gen_button, qtbot):
    """Test the hover animations of the button."""
    button, _, _ = type_gen_button
    qtbot.addWidget(button.button)
    
    # Simulate mouse enter
    enter_event = QEvent(QEvent.Enter)
    button.eventFilter(button.button, enter_event)
    qtbot.wait(300)  # wait for animation to potentially start
    
    # Simulate mouse leave to trigger animation reset
    leave_event = QEvent(QEvent.Leave)
    button.eventFilter(button.button, leave_event)
    qtbot.wait(300)  # wait for animation to potentially complete

    # Check if the animation's end value is set
    assert button.anim.endValue() is not None
    assert button.anim.endValue().width() > 0

# Test class RayonButton
@pytest.fixture
def mock_ellipse():
    """Fixture to create a mock ellipse object."""
    ellipse = MagicMock()
    ellipse.change_taille = MagicMock()
    return ellipse

@pytest.fixture
def rayon_button(qtbot, mock_ellipse):
    """Fixture to create RayonButton with a mocked ellipse."""
    button = RayonButton(ellipse=mock_ellipse, coef=0.1)
    qtbot.addWidget(button)
    return button, mock_ellipse

def test_initialization(rayon_button):
    """Test the initialization of the RayonButton."""
    button, ellipse = rayon_button
    assert button.button.text() == 'ajouter 0.1'

def test_button_click_adjusts_ellipse_size(rayon_button, qtbot):
    """Test that clicking the button adjusts the ellipse size as expected."""
    button, ellipse = rayon_button
    qtbot.mouseClick(button.button, Qt.LeftButton)
    ellipse.change_taille.assert_called_once_with(500 * 0.1)  # Expected adjustment

def test_event_filter_animations(rayon_button, qtbot):
    """Test the hover animations of the button."""
    button, _ = rayon_button
    qtbot.addWidget(button.button)
    
    # Simulate mouse enter
    enter_event = QEvent(QEvent.Enter)
    button.eventFilter(button.button, enter_event)
    qtbot.wait(200)  # Wait for the animation to potentially start
    
    # Check that the animation's end value is set correctly
    assert button.anim.endValue() == QRect(-1, 15, 282, 60)

    # Simulate mouse leave
    leave_event = QEvent(QEvent.Leave)
    button.eventFilter(button.button, leave_event)
    qtbot.wait(200)  # Wait for the animation to potentially end

    # Check that the animation resets to the initial size
    assert button.anim.endValue() == QRect(9, 20, 282, 60)

# Test class SuppButton
@pytest.fixture
def graphics_scene():
    """Fixture to create a QGraphicsScene."""
    return create_autospec(QGraphicsScene)

@pytest.fixture
def interactive_ellipse(graphics_scene):
    """Fixture to create a mock QGraphicsEllipseItem."""
    ellipse = create_autospec(QGraphicsEllipseItem)
    ellipse.scene.return_value = graphics_scene
    return ellipse

@pytest.fixture
def mock_map():
    """Fixture to create a mock map that contains ellipses."""
    map_mock = MagicMock()
    map_mock.suprime_point = MagicMock()
    return map_mock

@pytest.fixture
def supp_button(qtbot, mock_map, interactive_ellipse):
    """Fixture to create SuppButton with mock dependencies."""
    button = SuppButton(map=mock_map, ellipse=interactive_ellipse)
    qtbot.addWidget(button)
    return button, mock_map, interactive_ellipse

def test_initialization(supp_button):
    """Test the initialization and UI setup of the SuppButton."""
    button, _, _ = supp_button
    assert isinstance(button.button, QPushButton)
    assert button.button.text() == "Supprimer"

def test_button_click_removes_ellipse(supp_button, qtbot, graphics_scene):
    """Test that clicking the button removes the ellipse from its scene."""
    button, mock_map, ellipse = supp_button
    qtbot.mouseClick(button.button, Qt.LeftButton)
    graphics_scene.removeItem.assert_called_once_with(ellipse)
    mock_map.suprime_point.assert_called_once_with(ellipse)
    assert button.ellipse is None

def test_change_ellipse(supp_button):
    """Test the changeEllipse method."""
    button, _, _ = supp_button
    new_ellipse = create_autospec(QGraphicsEllipseItem)
    button.changeEllipse(new_ellipse)
    assert button.ellipse is new_ellipse

def test_event_filter_animations(supp_button, qtbot):
    """Test the hover animations of the button."""
    button, _, _ = supp_button
    qtbot.addWidget(button.button)

    # Simulate mouse enter
    enter_event = QEvent(QEvent.Enter)
    button.eventFilter(button.button, enter_event)
    qtbot.wait(200)  # Wait for the animation to potentially start

    # Check that the animation's end value is set correctly
    assert button.anim.endValue() == QRect(-1, 15, 282, 60)

    # Simulate mouse leave
    leave_event = QEvent(QEvent.Leave)
    button.eventFilter(button.button, leave_event)
    qtbot.wait(200)  # Wait for the animation to potentially end

    # Check that the animation resets to the initial size
    assert button.anim.endValue() == QRect(9, 20, 282, 60)

# Test class ZoneButton
@pytest.fixture
def lwindow_mock():
    """ Fixture pour créer un mock de LWindow. """
    mock = MagicMock()
    mock.compass = MagicMock()
    mock.type_generation = [None, 'type1']
    mock.ellipse_touched = MagicMock()
    mock.openPopup = MagicMock()
    return mock

@pytest.fixture
def zone_button(lwindow_mock):
    """ Fixture pour créer et retourner une instance de ZoneButton avec un mock de LWindow. """
    return ZoneButton(lwindow=lwindow_mock)

def test_initialization(zone_button):
    """ Teste si le widget est correctement initialisé. """
    assert zone_button.lwindow is not None
    assert zone_button.map is not None
    assert len(zone_button.valeur_edits) == 3  # Assure que trois QSpinBox sont créés

def test_refresh_champ(zone_button):
    """ Teste la fonction refresh_champ pour s'assurer qu'elle réinitialise les valeurs des QSpinBox à 0. """
    for edit in zone_button.valeur_edits:
        edit.setValue(10)  # Définir une valeur initiale non nulle
    zone_button.refresh_champ()
    assert all(edit.value() == 0 for edit in zone_button.valeur_edits)

def test_afficher_informations(zone_button):
    """ Teste la fonction afficher_informations pour vérifier la manipulation et l'utilisation des valeurs des spins. """
    zone_button.valeur_edits[0].setValue(5)
    zone_button.valeur_edits[1].setValue(10)
    zone_button.valeur_edits[2].setValue(15)
    zone_button.afficher_informations()
    zone_button.lwindow.compass.place_point.assert_called_once_with(25, 50, 'type1', 75, zone_button.lwindow.ellipse_touched)
    assert zone_button.submit_button.isEnabled() == True  # Vérifie que le bouton est réactivé

def test_button_animation(zone_button, qtbot):
    """Test button animations for hover enter and leave events."""
    # Ensure the widget is in a proper state and added to the test environment
    qtbot.addWidget(zone_button.submit_button)

    # Simulating mouse enter event
    enter_event = QEvent(QEvent.Enter)
    QApplication.sendEvent(zone_button.submit_button, enter_event)
    qtbot.wait(200)  # Increase wait time to ensure animation has time to start

    # Check if the animation is running after the enter event
    assert zone_button.anim.state() == QPropertyAnimation.Running, "Animation should start on mouse enter"

    # Allow animation to complete before simulating leave
    QTimer.singleShot(200, lambda: None)  # This just delays the next step
    qtbot.wait(300)

    # Simulating mouse leave event
    leave_event = QEvent(QEvent.Leave)
    QApplication.sendEvent(zone_button.submit_button, leave_event)
    qtbot.wait(200)  # Again, ensure there's enough time for animation to react

    # Check if the animation is still running after the leave event
    assert zone_button.anim.state() == QPropertyAnimation.Running, "Animation should start on mouse leave"

# Test class CustomInputDialog
@pytest.fixture
def customInput(qtbot, mock_map):
    """Fixture to create ZoneButton with a mock map."""
    button = CustomInputDialog(map=mock_map)
    qtbot.addWidget(button)
    return button, mock_map

def test_dialog_setup(qapp):
    dialog = CustomInputDialog()
    assert dialog.windowTitle() == "Saisie d'un entier"
    assert dialog.spinBox.minimum() == 1
    assert dialog.spinBox.maximum() == 2000000

def test_getInt_accept(qapp, qtbot):
    dialog = CustomInputDialog()
    qtbot.addWidget(dialog)
    dialog.spinBox.setValue(10)  # Set a value for testing
    result, accepted = dialog.getInt()
    assert accepted == True
    assert result == 10

def test_getInt_cancel(qapp, qtbot):
    dialog = CustomInputDialog()
    qtbot.addWidget(dialog)
    dialog.spinBox.setValue(5)  # Set a value for testingk
    result, accepted = dialog.getInt()
    assert accepted == False
    assert result == 0
