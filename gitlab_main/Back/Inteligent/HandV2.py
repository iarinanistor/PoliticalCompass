import mediapipe as mp
import numpy as np
import imageio

# Function to calculate Euclidean distance between two points
def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Initialize imageio reader to capture video from the first camera device
reader = imageio.get_reader('<video0>')

# Loop over each frame from the video stream
try:
    for frame in reader:
        image = frame[:, :, :3]

        # Process the frame with MediaPipe Hands
        results = hands.process(image)

        # Calculate distance if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image.shape[1],
                             hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image.shape[0])
                index_tip = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1],
                             hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image.shape[0])

                # Print the distance in pixels
                distance = calculate_distance(thumb_tip, index_tip)
                print(f'Distance: {distance:.2f} pixels')

except KeyboardInterrupt:
    # Close the video stream on interrupt
    reader.close()

# Release resources
hands.close()
reader.close()
