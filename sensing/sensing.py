#imports
import cv2
import mediapipe as mp
import time
from utils.moves import Moves

# Actual Class

class Sensing:
    def __init__(self) -> None:
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands  # type: ignore
        self.draw = mp.solutions.drawing_utils  # type: ignore
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.9, min_tracking_confidence=0.9)
        # Open webcam
        self.cap = cv2.VideoCapture(0)
        # Variables to track motion for horizontal slap / turn detection
        self.prev_x = None
        self.prev_time = None
        self.slap_cooldown = 0
    def fingers_up(self, hand_landmarks) -> list[int]: #Can bitmask if bhaiya asks for optimization
        """
        Order:[Thumb,Index,Middle, Ring, Pinky]
        Note Thumb is up if tip is to the LEFT  of the inner knuckle (right-hand, mirrored cam)
        """
        tips =[4, 8, 12, 16, 20]
        fingers = []
        if hand_landmarks.landmark[tips[0]].x< hand_landmarks.landmark[tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        for tip in tips[1:]:
            if hand_landmarks.landmark[tip].y <hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
    def thumb_pointing_down(self, hand_landmarks) -> bool:
        tip_y  = hand_landmarks.landmark[4].y
        base_y = hand_landmarks.landmark[2].y 
        return tip_y > base_y
    
    def all_fingers_horizontal(self, hand_landmarks, frame_width) -> str |None: #either direction or none
        tips  =[8, 12, 16, 20]
        knuckles  = [5,9, 13, 17]
        tip_x_avg= sum(hand_landmarks.landmark[i].x for i in tips) / 4
        knuckle_x_avg =sum(hand_landmarks.landmark[i].x for i in knuckles) / 4
        delta = tip_x_avg -knuckle_x_avg
        threshold= 0.12
        if delta >threshold:
            return "right"
        elif delta< -threshold:
            return "left"
        return None

    def detect_move(self, all_hand_landmarks, frame_width) -> Moves | None:
        if not all_hand_landmarks:
            return None
        # --- PICK FLAG: requires exactly 2 hands, all fingers up on both ---
        if len(all_hand_landmarks) == 2:
            both_open = all(self.fingers_up(lm) == [1, 1, 1, 1, 1] or self.fingers_up(lm) == [0,1,1,1,1] for lm in all_hand_landmarks)
            if both_open:
                return Moves.PICK_FLAG
        # Single-hand gestures — use the first (most confident) hand
        lm = all_hand_landmarks[0]
        up = self.fingers_up(lm)
        four_fingers_up = up[1:] 
        four_fingers_down = all(f == 0 for f in four_fingers_up)
        if up == [0, 0, 0, 0, 0]:
            return Moves.DROP_FLAG
        if up == [1, 0, 0, 0, 0]:
            return Moves.JUMP_UP
        if four_fingers_down and self.thumb_pointing_down(lm):
            return Moves.ROLL_UNDER
        if up == [1, 1, 1, 1, 1]:
            return Moves.STOP
        direction = self.all_fingers_horizontal(lm, frame_width)
        if direction == "left":
            return Moves.TURN_LEFT
        if direction == "right":
            return Moves.TURN_RIGHT
        if up == [1, 1, 1, 0, 0]:
            return Moves.SHOOT
        return None
    def run(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            frame = cv2.flip(frame, 1)
            h, w, i = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)
            label = "No Gesture"
            current_time = time.time()
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                move = self.detect_move(results.multi_hand_landmarks, w)
                if move is not None:
                    label =Moves.makeStr(move)
            else:
                prev_x = None
                prev_time = None
            
            cv2.putText(frame, label, (20, 60),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.imshow("Gesture Recognition",frame)
            # ESC to exit
            if cv2.waitKey(1) & 0xFF == 27:
                self.destroy()
                break
    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()