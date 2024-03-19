import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,QMessageBox
from BaseDonnee.Base_Donnee import *
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entrer deux entiers")

        layout = QVBoxLayout()

        self.number_entry1 = QLineEdit(self)
        self.number_entry1.setPlaceholderText("Entrez le premier entier")
        layout.addWidget(self.number_entry1)

        self.number_entry2 = QLineEdit(self)
        self.number_entry2.setPlaceholderText("Entrez le deuxième entier")
        layout.addWidget(self.number_entry2)

        self.button = QPushButton("Valider", self)
        self.button.clicked.connect(self.create_database_and_show)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def create_database_and_show(self):
        try:
            int1 = int(self.number_entry1.text())
            int2 = int(self.number_entry2.text())
            self.bd = Base_donnee.creer(int1, int2)
            self.bd.window.show()
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des entiers valides")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #global bd
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
