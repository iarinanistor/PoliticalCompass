import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QProgressBar, QVBoxLayout

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        """
        Constructeur de la classe ProgressDialog.

        Args:
            parent (QWidget): Widget parent. Par défaut, None.
        """
        super().__init__(parent)
        self.setWindowTitle("Loading...")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        layout = QVBoxLayout(self)
        
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        layout.addWidget(self.progress)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)  # Update progress every 50 milliseconds
        
    def update_progress(self):
        """
        Méthode pour mettre à jour la barre de progression.
        """
        value = self.progress.value() + 1
        if value > self.progress.maximum():
            self.timer.stop()
            self.accept()  # Close the dialog when progress is complete
        else:
            self.progress.setValue(value)

def show_loading_dialog():
    """
    Fonction pour afficher la boîte de dialogue de chargement.
    """
    app = QApplication(sys.argv)
    dialog = ProgressDialog()
    dialog.exec()
