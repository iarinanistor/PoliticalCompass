from Tournoi.TreeView import arbre_test

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsView, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fenêtre Principale")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.button = QPushButton("Lancer le tournoi")
        layout.addWidget(self.button)
        self.central_widget.setLayout(layout)
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.setEnabled(False)
        self.launch_tournament()

    def launch_tournament(self): # Remplacez cela par votre liste de candidats
        tr = arbre_test()
        self.tournament_window = QMainWindow()
        self.tournament_window.setWindowTitle("Tournoi")
        self.tournament_window.setCentralWidget(tr.view)
        self.tournament_window.show()
        self.setEnabled(True)

def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()
