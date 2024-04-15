from PySide6.QtWidgets import QApplication
import sys

from BaseDonnee.BaseDonnee import Basedonnee

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bd = Basedonnee.creer(123,500,True)
    bd.window.show()
    sys.exit(app.exec())