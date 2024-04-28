from PySide6.QtWidgets import QPushButton, QLineEdit, QVBoxLayout, QWidget, QProgressBar
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize


class BoutonIO(QWidget):
    def __init__(self, bd, nom, l=200, h=80):
        super().__init__()
        self.h = h
        self.l = l
        self.setFixedSize(self.l, self.h*2)
        self.bd = bd
        self.nom=nom
        layout = QVBoxLayout(self)

        # Champ de texte
        self.text_edit = QLineEdit()
        layout.addWidget(self.text_edit)

        # Bouton I/O
        self.io_button = DownloadButton(self.nom,parent=self)
        layout.addWidget(self.io_button)

    def save_text(self):
        #show_loading_dialog()
        text = self.text_edit.text()
        if self.nom == "recharge":
            print("Texte Charger :", text,"\n")
            self.bd.recharge(text)
        else :
            self.bd.save(text)
            print("Texte sauvegardé :", text,"\n")
        self.text_edit.clear()  # Efface le texte après sauvegarde

class BoutonRecharge(BoutonIO):
    def __init__(self, bd, l=200, h=80):
        super().__init__(bd, "recharge", l, h)
        
class BoutonSave(BoutonIO):
    def __init__(self, bd, l=200, h=80):
        super().__init__(bd, "save", l, h)

class DownloadButton(QPushButton):
    def __init__(self,nom, longueur=200, largeur=40, parent=None):
        super().__init__(nom, parent)
        self.setIcon(QIcon("Front/Widgets/upload.png"))  # Définir l'icône du bouton
        self.setIconSize(QSize(24, 24))  # Définir la taille de l'icône
        self.clicked.connect(self.start_download)
        self.downloading = False
        self.progressBar = None
        self.setStyleSheet(open("Front/Widgets/style.qss").read())  # vous pouvez le déplacer à un endroit global
        self.longueur = longueur
        self.largeur = largeur
        self.setFixedSize(self.longueur, self.largeur)

    def start_download(self):
        if not self.downloading:
            self.downloading = True
            self.hide()
            if self.progressBar is None:
                self.progressBar = QProgressBar()
                self.progressBar.setMinimum(0)
                self.progressBar.setMaximum(100)
                self.progressBar.setStyleSheet(open("Front/Widgets/style.qss").read())  # vous pouvez le déplacer à un endroit global
                layout = self.parentWidget().layout()
                layout.replaceWidget(self, self.progressBar)
                self.progressBar.setFixedSize(220, 20)

            else:
                self.progressBar.setValue(0)
                self.progressBar.show()
            self.timer = self.startTimer(10)
            self.progress = 0

    def timerEvent(self, event):
        if self.progress >= 100:
            self.killTimer(self.timer)
            self.downloading = False
            self.show()
            self.progressBar.hide()
        else:
            self.progress += 1
            self.progressBar.setValue(self.progress)

import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Application")

        layout = QVBoxLayout(self)
        layout.addWidget(DownloadButton("test"))
        layout.addWidget(DownloadButton("test"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
