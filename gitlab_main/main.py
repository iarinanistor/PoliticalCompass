from PySide6.QtWidgets import QApplication
import sys

from BaseDonnee.Base_Donnee import Base_donnee

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bd = Base_donnee.creer(123,500,False)
    bd.window.show()
    sys.exit(app.exec())