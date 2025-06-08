import cv2
import mediapipe as mp
import numpy as np
import pyfirmata
import time


board = pyfirmata.Arduino('COM5')  # Change COM port as needed
servo_pin1 = board.get_pin('d:9:s')  # Servo 1 on pin 9 (right hand)
servo_pin2 = board.get_pin('d:10:s')  # Servo 2 on pin 10 (left hand)
it = pyfirmata.util.Iterator(board)
it.start()
time.sleep(1)  


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,  # Detect 2 hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


cap = cv2.VideoCapture(0)


MIN_DISTANCE = 20
MAX_DISTANCE = 150
MIN_ANGLE = 0
MAX_ANGLE = 180

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue


    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    height, width = frame.shape[:2]
    
    
    angle1 = 90  
    angle2 = 90  
    
    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
           
            hand_type = handedness.classification[0].label  
            
           
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]

            
            thumb_x, thumb_y = int(thumb.x * width), int(thumb.y * height)
            index_x, index_y = int(index.x * width), int(index.y * height)

            
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 0), 2)

        
            distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
            
            
            angle = np.clip(np.interp(distance, [MIN_DISTANCE, MAX_DISTANCE], [MIN_ANGLE, MAX_ANGLE]), MIN_ANGLE, MAX_ANGLE)
            
            
            if hand_type == "Right":
                angle1 = angle
                color = (0, 255, 0)  
            else:
                angle2 = angle
                color = (0, 0, 255)  
            
            
            cv2.putText(frame, f'{hand_type}: {int(angle)} deg', 
                        (thumb_x, thumb_y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    
    servo_pin1.write(angle1)
    servo_pin2.write(angle2)
    
    
    cv2.putText(frame, f'Right Servo: {int(angle1)} deg', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'Left Servo: {int(angle2)} deg', (50, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Dual Hand Servo Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
board.exit()
