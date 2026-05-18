#imports
import cv2
import mediapipe as mp
import time
from utils.moves import Moves

# Actual Class

class Sensing:
    def __init__(self) -> None:
        pass
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