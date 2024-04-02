from PySide6.QtWidgets import QApplication
import sys

from BaseDonnee.Base_Donnee import Base_donnee

import Internet
import os

csv_file = "emissions.csv"
"""
if os.path.exists(csv_file):
    os.remove(csv_file)
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bd = Base_donnee.creer(123,500,True)
    bd.window.show()
    sys.exit(app.exec())