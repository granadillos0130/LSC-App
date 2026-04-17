import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        landmarks = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])

        return frame, landmarks

    def normalize(self, landmarks):
        if not landmarks:
            return []
        
        base_x, base_y, base_z = landmarks[0]
        normalized = [[l[0] - base_x, l[1] - base_y, l[2] - base_z] for l in landmarks]

        max_dist = max(np.sqrt(x**2 + y**2 + z**2) for x, y, z in normalized)
        if max_dist == 0:
            return []
        
        normalized = [[x/max_dist, y/max_dist, z/max_dist] for x, y, z in normalized]
        return np.array(normalized).flatten().tolist()