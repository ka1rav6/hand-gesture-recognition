#imports
import cv2
import mediapipe as mp
import time
from utils.moves import Moves

# Actual Class

class Sensing:
    def __init__(self) -> None:
        # Initialize MediaPipe
        mp_hands = mp.solutions.hands  # type: ignore
        draw = mp.solutions.drawing_utils  # type: ignore
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.9, min_tracking_confidence=0.9)
        # Open webcam
        cap = cv2.VideoCapture(0)
        # Variables to track motion for horizontal slap / turn detection
        prev_x = None
        prev_time = None
        slap_cooldown = 0
    def fingers_up(self, hand_landmarks) -> list[int] | None: #Can bitmask if bhaiya asks for optimization
        pass
    def thumb_pointing_down(self, hand_landmarks) -> bool:
        pass
    def all_fingers_horizontal(self, hand_landmarks, frame_width) -> str |None: #either direction or none
        pass
    def detect_move(self, all_hand_landmarks, frame_width) ->Moves | None:
        pass
    def main_loop(self):
        pass