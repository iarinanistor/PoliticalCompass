from Front.Windows.LWindow import LWindow
import sys
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LWindow()
    app.setQuitOnLastWindowClosed(False)
    window.show()
    sys.exit(app.exec())
 