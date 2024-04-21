import cv2
import mediapipe as mp
import numpy as np

class testf:
    
    def __init__(self) :
        pass 
    def fonction_SCV(self,argument):
        print(argument)
        
class FiltreKalmanSimple:
    """
    filitre de bruit
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
    #systeme de lissage des donnees de la main
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
    #systeme de computere vision 
    def __init__(self,classe):
        self.classe = classe
        self.old_distance = 0
        self.cpt=0
        self.cap=None
        
    def restratOld(self,new): 
        if abs(self.old_distance-new)>=10 : self.old_distance = new 
    
    def detection(self):
        if self.old_distance >=350 : self.classe.fonction_SCV(-1)
        elif self.old_distance>=200 : self.classe.fonction_SCV(0.02)
        elif self.old_distance >=60: self.classe.fonction_SCV(0.01)
        else : self.classe.fonction_SCV(0)
        
    def start(self):
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
                    #print("Distance point 1 - pouce:",distance_point_pouce," pixels")
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
        self.cap.release()
        cv2.destroyAllWindows()
        
def afficher_main(frame, hand_landmarks,num_points,mp_hands):
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
    instance_testf = testf()  
    scv = SCV(instance_testf) 
    scv.start()
    
if __name__ == "__main__":
    main()
