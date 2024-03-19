from PySide6.QtWidgets import QApplication
import sys

from Front.Planete.Planete import *
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    
    mainWindow.show()
    sys.exit(app.exec())
