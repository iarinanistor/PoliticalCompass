import imageio
import mediapipe as mp
import numpy as np

class TestFunction:
    def fonction_SCV(self, argument):
        print(argument)

class KalmanFilter:
    def __init__(self, process_noise, measurement_noise, initial_estimate):
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.current_estimate = initial_estimate
        self.current_error_estimate = 1.0

    def update(self, measurement):
        predicted_estimate = self.current_estimate
        predicted_error_estimate = self.current_error_estimate + self.process_noise
        kalman_gain = predicted_error_estimate / (predicted_error_estimate + self.measurement_noise)
        self.current_estimate = predicted_estimate + kalman_gain * (measurement - predicted_estimate)
        self.current_error_estimate = (1 - kalman_gain) * predicted_error_estimate
        return self.current_estimate

class Finger:
    def __init__(self, base=None, point=None, point2=None, extremite=None):
        self.base = base
        self.point = point
        self.point2 = point2
        self.extremite = extremite

    def distance(self, point1, point2):
        return np.linalg.norm([point1.x - point2.x, point1.y - point2.y])

class Hand:
    def __init__(self, hand_landmarks):
        self.fingers = [Finger(hand_landmarks.landmark[i], hand_landmarks.landmark[i+1], hand_landmarks.landmark[i+2], hand_landmarks.landmark[i+3])
                        for i in range(0, 21, 4) if i + 4 < 21]

    def thumb_index_distance(self):
        return self.fingers[0].distance(self.fingers[0].extremite, self.fingers[1].extremite)

    def thumb_size(self):
        return self.fingers[0].distance(self.fingers[0].base, self.fingers[0].extremite)

    def normalized_distance(self):
        return self.thumb_index_distance() / self.thumb_size()

class SLH:
    def __init__(self, hand):
        self.hand = hand
        self.filter = KalmanFilter(0.1, 0.1, 0)

    def smooth(self):
        measurement = abs(self.hand.normalized_distance() * 100)
        return abs(int(self.filter.update(measurement)))

class SCV:
    def __init__(self, printer):
        self.printer = printer
        self.old_distance = 0
        self.counter = 0

    def restart_old(self, new):
        if abs(self.old_distance - new) >= 10:
            self.old_distance = new

    def detection(self):
        if self.old_distance >= 99:
            self.printer.fonction_SCV(-1)
        elif self.old_distance >= 70:
            self.printer.fonction_SCV(0.02)
        elif self.old_distance >= 35:
            self.printer.fonction_SCV(0.01)
        else:
            self.printer.fonction_SCV(0)

    def start(self):
        with mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as mp_hands:

            reader = imageio.get_reader('<video0>')

            try:
                for frame in reader:
                    frame_rgb = frame[:, :, :3]  # Convert to RGB
                    results = mp_hands.process(frame_rgb)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            hand = Hand(hand_landmarks)
                            slh = SLH(hand)
                            self.restart_old(slh.smooth())
                            self.detection()
                    else:
                        self.counter += 1
                        if self.counter >= 90:
                            self.counter = 0
                            break
            finally:
                reader.close()

if __name__ == "__main__":
    printer = TestFunction()
    scv = SCV(printer)
    scv.start()
