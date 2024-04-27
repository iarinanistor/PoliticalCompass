from Back.Statistique.MonteCarlo import *

if __name__ == '__main__':
    t=50
    start_time = time.time()
    app = QApplication(sys.argv)
    hitmap=SimulationAleatoire("",t,5,"Copeland")
    hitmap.show()
    print("Fin des tours ", time.time() - start_time)
    sys.exit(app.exec())

    