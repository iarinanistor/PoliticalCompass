from LWindow import LWindow
import sys
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LWindow()
    window.show()
    sys.exit(app.exec())
 