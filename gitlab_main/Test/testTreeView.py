from gitlab_main.Tournoi.TreeView import arbre_test

from PySide6.QtWidgets import QApplication

def main():
    app = QApplication([])
    tr = arbre_test()
    tr.view.show()
    res = tr.fait_gagner(tr.liste_candidates[1])
    tr.view.show()
    app.exec()

if __name__ == "__main__":
    main()
