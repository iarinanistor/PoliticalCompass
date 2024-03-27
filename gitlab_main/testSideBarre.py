from PySide6.QtWidgets import QApplication
from Front.Widgets.IO_Bouton import *
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideMenu(None)
    window.show()
    sys.exit(app.exec())