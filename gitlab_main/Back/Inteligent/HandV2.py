import imageio
import mediapipe as mp
import numpy as np

class testf():
    
    def __init__(self) :
        pass 
    def fonction_SCV(self,argument):
        print(argument)
        
class FiltreKalmanSimple:
    def __init__(self, process_noise, measurement_noise, initial_estimate):
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.current_estimate = initial_estimate
        self.current_error_estimate = 1

    def update(self, measurement):
        predicted_estimate = self.current_estimate
        predicted_error_estimate = self.current_error_estimate + self.process_noise
        kalman_gain = predicted_error_estimate / (predicted_error_estimate + self.measurement_noise)
        self.current_estimate = predicted_estimate + kalman_gain * (measurement - predicted_estimate)
        self.current_error_estimate = (1 - kalman_gain) * predicted_error_estimate
        return self.current_estimate

class Doigt:
    def __init__(self, base=None, point=None, point2=None, extremite=None):
        self.base = base
        self.point = point
        self.point2 = point2
        self.extremite = extremite

    def distance(self, point1, point2):
        return np.linalg.norm([point1.x - point2.x, point1.y - point2.y])

class Hand:
    def __init__(self, hand_landmarks, mp_hands):
        self.doigts = []
        for i in range(0, 21, 4):
            if i + 4 < 21:
                self.doigts.append(Doigt(hand_landmarks.landmark[i],
                                         hand_landmarks.landmark[i+1],
                                         hand_landmarks.landmark[i+2],
                                         hand_landmarks.landmark[i+3]))

    def distance_pouce_index(self):
        return self.doigts[0].distance(self.doigts[0].extremite, self.doigts[1].extremite)

    def pouce_taille(self):
        return self.doigts[0].distance(self.doigts[0].base, self.doigts[0].extremite)

    def distance(self):
        return self.distance_pouce_index() / self.pouce_taille()

class SLH:
    def __init__(self, hand):
        self.hand = hand
        self.filtre = FiltreKalmanSimple(0.1, 0.1, 0)

    def lisse(self):
        new = abs(self.hand.distance() * 100)
        return abs(int(self.filtre.update(new)))

class SCV():
    #systeme de computere vision 
    def __init__(self,classe):
        self.classe = classe
        self.old_distance = 0
        self.cpt=0
        
    def restratOld(self,new): 
        if abs(self.old_distance-new)>=10 : self.old_distance = new 

    def detection(self):
        if self.old_distance >=99 : self.classe.fonction_SCV(-1)
        elif self.old_distance>=70 : self.classe.fonction_SCV(0.02)
        elif self.old_distance >=35: self.classe.fonction_SCV(0.01)
        else : self.classe.fonction_SCV(0)
    
    def stop(self):
        self.mp_hands.close()
        self.reader.close()
                    
    def start(self):
        mp_hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )


        reader = imageio.get_reader(0)


        try:
            if self.cpt >= 90: self.cpt=0; self.stop()
            for frame in reader:
                frame_rgb = frame[:, :, :3]  # Convert to RGB
                results = mp_hands.process(frame_rgb)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand = Hand(hand_landmarks, mp_hands)
                        slh = SLH(hand)
                        self.restratOld(slh.lisse())
                        self.detection()
                else : self.cpt+=1
        finally:
            mp_hands.close()
            reader.close()

if __name__ == "__main__":
    printer = testf()
    scv = SCV(printer)
    scv.start()
