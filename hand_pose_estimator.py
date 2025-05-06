import cv2
import numpy as np
import mediapipe as mp

class HandPoseEstimator:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
    def process_image(self, image):
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and get hand landmarks
        results = self.hands.process(image_rgb)
        
        # Draw hand landmarks on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return image, results
    
    def get_index_finger_tip(self, results):
        # Get the position of the index finger tip (landmark 8)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            index_finger_tip = hand_landmarks.landmark[8]
            return index_finger_tip
        return None
    
    def is_grabbing(self, results):
        # Check if the hand is making a grabbing gesture
        # This is a simple implementation - thumb tip close to index finger tip
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            # Calculate distance between thumb and index finger tips
            distance = ((thumb_tip.x - index_tip.x) ** 2 + 
                        (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            
            # If distance is small, consider it a grab gesture
            return distance < 0.08
        return False
