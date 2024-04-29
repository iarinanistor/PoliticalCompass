import cv2
import mediapipe as mp
import numpy as np

# code Intial de SCV a voulais etre replacer par hand2 car conflit 
# entre cv2 et mediapipe

#En vue de la complexité de faire des tests sur ces fonctions, les tests se limiteront au lancement de la fonction principale.
class testf:
    """
    Classe de test simple pour la démonstration.

    Méthodes:
        __init__: Initialise l'instance de la classe.
        fonction_SCV(self, argument): Affiche l'argument donné.
    """
    def __init__(self) :
        pass 
    def fonction_SCV(self,argument):
        print(argument)
        
class FiltreKalmanSimple:
    """
    Implémentation simple d'un filtre de Kalman pour estimer et réduire le bruit dans les mesures séquentielles.

    Attributes:
        process_noise (float): Estimation du bruit du processus.
        measurement_noise (float): Estimation du bruit de mesure.
        current_estimate (float): Estimation actuelle.
        current_error_estimate (float): Estimation de l'erreur actuelle.

    Méthodes:
        __init__(self, process_noise, measurement_noise, initial_estimate): Initialise le filtre de Kalman.
        update(self, measurement): Met à jour l'estimation basée sur une nouvelle mesure.
    """
    def __init__(self, process_noise, measurement_noise, initial_estimate):
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.current_estimate = initial_estimate
        self.current_error_estimate = 1

    def update(self, measurement):
        # Prédiction
        predicted_estimate = self.current_estimate
        predicted_error_estimate = self.current_error_estimate + self.process_noise

        # Correction
        kalman_gain = predicted_error_estimate / (predicted_error_estimate + self.measurement_noise)
        self.current_estimate = predicted_estimate + kalman_gain * (measurement - predicted_estimate)
        self.current_error_estimate = (1 - kalman_gain) * predicted_error_estimate

        return self.current_estimate
    
class Doigt:
    """
    Représente un doigt avec des points de détection spécifiques.

    Attributes:
        base, point, point2, extremite: Points représentant différentes parties du doigt.

    Méthodes:
        set_base(self, base), set_point(self, point), set_point2(self, point2), set_extremite(self, extremite): Méthodes pour définir les points du doigt.
        distance(self, point1, point2): Calcule la distance euclidienne entre deux points.
        taille(self): Retourne la longueur du doigt.
        est_leve(self): Détermine si le doigt est levé basé sur la géométrie des points.
        est_leve_pouce(self): Spécifique pour déterminer si le pouce est levé.
    """
    def __init__(self, base=None, point=None, point2=None, extremite=None):
        self.point = point
        self.point2 = point2
        self.base = base
        self.extremite = extremite

    def set_base(self, base):
        self.base = base

    def set_extremite(self, extremite):
        self.extremite = extremite

    def set_point(self, point):
        self.point = point

    def set_point2(self, point2):
        self.point2 = point2

    def distance(self,point1, point2):
        point1 = np.array([point1.x, point1.y])  # Extraction des coordonnées du NormalizedLandmark
        point2 = np.array([point2.x, point2.y])  # Extraction des coordonnées du NormalizedLandmark
        distance = np.linalg.norm(point2 - point1)
        return distance
    
    def taille(self):
        return self.distance(self.extremite, self.base)
    
    def est_leve(self):
        if (self.distance(self.base, self.point) + self.distance(self.point2, self.point) <=
                self.distance(self.base, self.extremite)):
            return 1 
        else:
            return 0
    
    def est_leve_pouce(self):
        if (self.distance(self.base, self.point) + self.distance(self.point, self.extremite)*0.95 <=
                self.distance(self.base, self.extremite)):
            return 1 
        else:
            return 0

class Hand:
    """
    Représente une main détectée, composée de plusieurs doigts.

    Attributes:
        ListeDoigt (list): Liste contenant les doigts de la main.

    Méthodes:
        __init__(self, encrage, pouce, doigt2, doigt3, doigt4, doigt5): Initialise une nouvelle instance de la main.
        creer(self, hand_landmarks): Crée la structure de la main basée sur les landmarks détectés.
        distance_pouce(self): Calcule la distance entre le pouce et l'index.
        distance(self): Calcule un rapport de distance entre le pouce et l'index.
    """

    def __init__(self, encrage=None, pouce=None, doigt2=None, doigt3=None, doigt4=None, doigt5=None):
        self.encrage = encrage
        self.pouce = pouce
        self.doigt2 = doigt2
        self.doigt3 = doigt3
        self.doigt4 = doigt4
        self.doigt5 = doigt5
        self.ListeDoigt = [pouce, doigt2, doigt3, doigt4, doigt5]
        
    def creer (self,hand_landmarks):
        self.pouce = Doigt(hand_landmarks.landmark[2], hand_landmarks.landmark[3], hand_landmarks.landmark[3],
                               hand_landmarks.landmark[4])
        self.doigt2 = Doigt(hand_landmarks.landmark[5], hand_landmarks.landmark[6], hand_landmarks.landmark[6],
                               hand_landmarks.landmark[8])
        self.doigt3 = Doigt(hand_landmarks.landmark[9], hand_landmarks.landmark[10], hand_landmarks.landmark[11],
                               hand_landmarks.landmark[12])
        self.doigt4 = Doigt(hand_landmarks.landmark[13], hand_landmarks.landmark[14], hand_landmarks.landmark[15],
                               hand_landmarks.landmark[16])
        self.doigt5 = Doigt(hand_landmarks.landmark[17], hand_landmarks.landmark[18], hand_landmarks.landmark[19],
                               hand_landmarks.landmark[20])
        self.ListeDoigt = [self.pouce, self.doigt2, self.doigt3, self.doigt4, self.doigt5]
    
    
    def distance_pouce(self):
        """
        utliser pour calculer la distance entre le pouce et l'index
        """
        return self.pouce.distance(self.pouce.extremite, self.doigt2.extremite)
    
    def distance(self):
        return  self.distance_pouce() / self.pouce.taille()

class SLH():
    """
    Système de lissage des données de la main utilisant un filtre de Kalman.

    Attributes:
        hand (Hand): Instance de la classe Hand dont les données doivent être lissées.
        filtre (FiltreKalmanSimple): Instance du filtre de Kalman utilisé pour le lissage.

    Méthodes:
        __init__(self, hand): Initialise le système de lissage avec une main donnée.
        lisse(self, old): Lisse la mesure de distance actuelle et retourne le résultat lissé.
        intitialize(self): Initialise le système avec une mesure de distance de base.
    """
    def __init__(self,hand):
        self.hand = hand
        self.start=0
        self.constantCorrection = 00 # valeur moyenne au demarge 
        self.process_noise = 0.1
        self.measurement_noise = 0.1
        self.initial_estimate = 0
        self.filtre = FiltreKalmanSimple(self.process_noise, self.measurement_noise, self.initial_estimate)
        
    def lisse(self,old=0):
        new = abs(self.hand.distance()*100)
        if abs(int(self.filtre.update(new)) - old) <=30 : return old  
        #if new >=40:  return 10
        return abs(int(self.filtre.update(new))-self.constantCorrection)
     
    def intitialize(self):
        self.start = self.hand.distance()*100
        
class SCV():
    """
    Système de vision par ordinateur pour le traitement de données de main.

    Attributes:
        classe (): Instance d'une classe qui utlise les fonctionnalités.
        cap (cv2.VideoCapture): Capture vidéo utilisée pour la détection en temps réel.

    Méthodes:
        __init__(self, classe): Initialise le système avec une instance de classe de test.
        restratOld(self, new): Réinitialise la distance précédemment mesurée si nécessaire.
        detection(self): Détecte et traite les distances mesurées.
        start(self): Démarre le processus de capture et de traitement vidéo.
        stop(self): Arrête la capture vidéo et ferme toutes les fenêtres.
    """
    def __init__(self,classe):
        self.classe = classe
        self.old_distance = 0
        self.cpt=0
        self.cap=None
        
    def restratOld(self,new): 
        """
        Réinitialise la valeur de 'old_distance' si un changement significatif est détecté, permettant de réagir uniquement aux variations importantes.

        Args:
            new (float): Nouvelle distance mesurée entre deux points spécifiques de la main.
        """
        if abs(self.old_distance-new)>=10 : self.old_distance = new 
    
    def detection(self):
        """
        Détecte les conditions de distance spécifiques et envoie des commandes appropriées via la méthode 'fonction_SCV' de l'instance 'classe' attribuée.

        La logique de détection est basée sur des seuils prédéfinis qui déclenchent différentes réactions:
        - Distance >= 350 : Envoyer -1
        - Distance >= 200 : Envoyer 0.02
        - Distance >= 70  : Envoyer 0.01
        - Sinon           : Envoyer 0
        """

        print(self.old_distance)
        if self.old_distance >=350 : self.classe.fonction_SCV(-1)
        elif self.old_distance>=200 : self.classe.fonction_SCV(0.02)
        elif self.old_distance >=70: self.classe.fonction_SCV(0.01)
        else : self.classe.fonction_SCV(0)
        
    def start(self):
        """
        Démarre la capture vidéo et le traitement des données de main. Configure la résolution de la caméra, initialise les outils de détection de MediaPipe, et traite les images capturées en continu.
        """
        cap = cv2.VideoCapture(0)
        self.cap = cap
        cap.set(3, 1280)
        cap.set(4, 720)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        distance_point_pouce=0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if self.cpt >= 90: self.cpt=0; self.stop()
            # Obtention des résultats de la détection des mains
            results = hands.process(frame)  # Utiliser l'image couleur directement
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Affichage de la main
                    #afficher_main(frame, hand_landmarks)
                    #Creation de la main 
                    Main = Hand()
                    Main.creer(hand_landmarks)
                    
                    # Calcul de la distance entre le premier point et le pouce
                    self.restratOld(distance_point_pouce)
                    slh = SLH(Main)
                    distance_point_pouce =slh.lisse(self.old_distance)
                    self.detection()
                    # Affichage de la distance en noir
                    #cv2.putText(frame, f"Distance point 1 - pouce: {distance_point_pouce:.2f} pixels", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            else : self.cpt+=1
            # Affichage du cadre résultantq
            #cv2.imshow("Hand Tracking", frame)

            # Sortie de la boucle si la touche 'q' est enfoncée
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libération des ressources
        cap.release()
        cv2.destroyAllWindows()
        
    def stop(self):
        """
        Arrête la capture vidéo et ferme toutes les fenêtres, libérant les ressources.
        """
        self.cap.release()
        cv2.destroyAllWindows()
        
def afficher_main(frame, hand_landmarks,num_points,mp_hands):
    """
    Fonction pour afficher la main dans une fenêtre de visualisation.

    Args:
        frame (np.array): Image sur laquelle dessiner.
        hand_landmarks (mediapipe.solutions.hands.HandLandmark): Landmarks de la main détectée.
        num_points (int): Nombre de points à afficher.
        mp_hands (mediapipe.solutions.hands): Instance de la solution Hands de MediaPipe.

    Cette fonction dessine les points et les connexions de la main sur l'image.
    """

    for i, point in enumerate(hand_landmarks.landmark[:num_points]):
        cx, cy = int(point.x * frame.shape[1]), int(point.y * frame.shape[0])
        if i in [0, 2, 4, 5, 8, 9, 12, 13, 16, 17, 20]:  # Indices des extrémités des doigts
            cv2.circle(frame, (cx, cy), 10, (0, 0, 0), -1)  # Noir pour les extrémités
        else:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # Vert pour les autres points

    # Dessiner les connexions entre les points
    for connection in mp_hands.HAND_CONNECTIONS:
        x1, y1 = int(hand_landmarks.landmark[connection[0]].x * frame.shape[1]), int(
            hand_landmarks.landmark[connection[0]].y * frame.shape[0])
        x2, y2 = int(hand_landmarks.landmark[connection[1]].x * frame.shape[1]), int(
            hand_landmarks.landmark[connection[1]].y * frame.shape[0])
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
def main():
    """
    Fonction principale utilisée pour démarrer le système de vision par ordinateur (SCV) dans le cadre de tests unitaires.

    Cette fonction crée une instance de la classe testf et utilise cette instance pour initialiser et démarrer le système SCV. 
    Elle est destinée à être utilisée dans des tests pour vérifier la correcte intégration et fonctionnement du système SCV 
    avec les composants définis dans la classe testf.
    """
    instance_testf = testf()  # Création d'une instance de la classe testf
    scv = SCV(instance_testf)  # Initialisation du système SCV avec l'instance de testf
    scv.start()  # Démarrage du système SCV pour le test
    
if __name__ == "__main__":
    main()
