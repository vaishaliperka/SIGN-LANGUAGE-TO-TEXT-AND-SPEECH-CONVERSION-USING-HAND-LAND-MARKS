import cv2
import time
import pyttsx3  # Added for speech
import HandTrackingModule as htm

# Initialize camera
hCam, wCam = 480, 640
cap = cv2.VideoCapture(0)
cap.set(4, hCam)
cap.set(3, wCam)
detector = htm.handDetector(detectionCon=0.7)

# Initialize TTS engine
engine = pyttsx3.init()

# Sentence building
sentence = ""
current_letters = []
last_letter_time = time.time()

# Button click tracker
button_clicked = None

def mouse_callback(event, x, y, flags, param):
    global button_clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if 20 <= x <= 120 and 400 <= y <= 440:
            button_clicked = "predict"
        elif 140 <= x <= 240 and 400 <= y <= 440:
            button_clicked = "space"
        elif 260 <= x <= 360 and 400 <= y <= 440:
            button_clicked = "clear"
        elif 380 <= x <= 480 and 400 <= y <= 440:
            button_clicked = "delete"
        elif 500 <= x <= 600 and 400 <= y <= 440:
            button_clicked = "speak"

cv2.namedWindow("ASL Detection")
cv2.setMouseCallback("ASL Detection", mouse_callback)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    posList = detector.findPosition(img, draw=True)

    result = ""
    if len(posList) != 0:
        fingers = []
        finger_tips = [8, 12, 16, 20]
        finger_dips = [6, 10, 14, 18]
        finger_pips = [7, 11, 15, 19]

        for tip, dip, pip in zip(finger_tips, finger_dips, finger_pips):
            if posList[tip][2] < posList[pip][2]:
                fingers.append(1)
            elif posList[tip][1] + 25 < posList[dip][1]:
                fingers.append(0.5)
            else:
                fingers.append(0)

        thumb_tip = posList[4]
        thumb_ip = posList[3]
        thumb_mcp = posList[2]
        thumb_right = thumb_tip[1] > thumb_mcp[1] + 15
        thumb_left = thumb_tip[1] < thumb_mcp[1] - 15
        thumb_up = thumb_tip[2] < thumb_ip[2] - 10
        thumb_down = thumb_tip[2] > thumb_ip[2] + 10

        # Letter prediction logic (unchanged)
        if (posList[3][2] > posList[4][2]) and (posList[3][1] > posList[6][1]) and (posList[4][2] < posList[6][2]) and fingers.count(0) == 4:
            result = "A"
        elif (posList[3][1] > posList[4][1]) and fingers.count(1) == 4 and thumb_up:
            result = "B"
        elif (posList[3][1] > posList[6][1]) and fingers.count(0.5) >= 1 and (posList[4][2] > posList[8][2]):
            result = "C"
        elif (fingers[0]==1) and fingers.count(0) == 3 and (posList[3][1] > posList[4][1]):
            result = "D"
        elif (posList[3][1] < posList[6][1]) and fingers.count(0) == 4 and posList[12][2] < posList[4][2]:
            result = "E"
        elif (fingers.count(1) == 3) and (fingers[0]==0) and (posList[3][2] > posList[4][2]):
            result = "F"
        elif (fingers[0]==0.25) and fingers.count(0) == 3:
            result = "G"
        elif (fingers[0]==0.25) and (fingers[1]==0.25) and fingers.count(0) == 2:
            result = "H"
        elif (posList[4][1] < posList[6][1]) and fingers.count(0) == 3:
            if (len(fingers)==4 and fingers[3] == 1):
                result = "I"
        elif (posList[4][1] < posList[6][1] and posList[4][1] > posList[10][1] and fingers.count(1) == 2):
            result = "K"
        elif (fingers[0]==1) and fingers.count(0) == 3 and (posList[3][1] < posList[4][1]):
            result = "L"
        elif (posList[4][1] < posList[16][1]) and fingers.count(0) == 4:
            result = "M"
        elif (posList[4][1] < posList[12][1]) and fingers.count(0) == 4:
            result = "N"
        elif (posList[4][2] < posList[8][2]) and (posList[4][2] < posList[12][2]) and (posList[4][2] < posList[16][2]) and (posList[4][2] < posList[20][2]):
            result = "O"
        elif (posList[4][1] > posList[12][1]) and posList[4][2] < posList[6][2] and fingers.count(0) == 4:
            result = "T"
        elif (posList[4][1] > posList[12][1]) and posList[4][2] < posList[12][2] and fingers.count(0) == 4:
            result = "S"
        elif (fingers[2] == 0) and (posList[4][2] < posList[12][2]) and (posList[4][2] > posList[6][2]):
            if (len(fingers)==4 and fingers[3] == 0):
                result = "P"
        elif (fingers[1] == 0) and (fingers[2] == 0) and (fingers[3] == 0) and (posList[8][2] > posList[5][2]) and (posList[4][2] < posList[1][2]):
            result = "Q"
        elif (posList[8][1] < posList[12][1]) and (fingers.count(1) == 2) and (posList[9][1] > posList[4][1]):
            result = "R"
        elif (posList[4][1] < posList[6][1] and posList[4][1] < posList[10][1] and fingers.count(1) == 2 and posList[3][2] > posList[4][2] and (posList[8][1] - posList[11][1]) <= 50):
            result = "U"
        elif (posList[4][1] < posList[6][1] and posList[4][1] < posList[10][1] and fingers.count(1) == 2 and posList[3][2] > posList[4][2]):
            result = "V"
        elif (posList[4][1] < posList[6][1] and posList[4][1] < posList[10][1] and fingers.count(1) == 3):
            result = "W"
        elif (fingers[0] == 0.5 and fingers.count(0) == 3 and posList[4][1] > posList[6][1]):
            result = "X"
        elif (fingers.count(0) == 3) and (posList[3][1] < posList[4][1]):
            if (len(fingers)==4 and fingers[3] == 1):
                result = "Y"

    current_time = time.time()
    if button_clicked == "predict" and result:
        current_letters.append(result)
        last_letter_time = current_time
        button_clicked = None
    elif button_clicked == "space":
        if current_letters:
            sentence += ''.join(current_letters) + " "
            current_letters = []
        last_letter_time = current_time
        button_clicked = None
    elif button_clicked == "clear":
        sentence = ""
        current_letters = []
        button_clicked = None
    elif button_clicked == "delete":
        if current_letters:
            current_letters.pop()
        elif sentence:
            sentence = sentence[:-1]
        button_clicked = None
    elif button_clicked == "speak":
        full_sentence = sentence + ''.join(current_letters)
        if full_sentence.strip():
            engine.say(full_sentence)
            engine.runAndWait()
        button_clicked = None

    # Display prediction box
    cv2.rectangle(img, (28, 255), (178, 425), (0, 225, 0), cv2.FILLED)
    cv2.putText(img, result, (55, 400), cv2.FONT_HERSHEY_COMPLEX, 5, (255, 0, 0), 15)

    # Sentence text (yellow)
    cv2.putText(img, f"Sentence: {sentence}{''.join(current_letters)}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Draw buttons
    cv2.rectangle(img, (20, 400), (120, 440), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Predict", (30, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(img, (140, 400), (240, 440), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Space", (155, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(img, (260, 400), (360, 440), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Clear", (275, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(img, (380, 400), (480, 440), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Delete", (390, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(img, (500, 400), (600, 440), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Speak", (515, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.imshow("ASL Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
