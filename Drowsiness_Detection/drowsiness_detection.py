import cv2
import numpy as np
import dlib
from imutils import face_utils
from playsound import playsound

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)


def compute(pta, ptb):
    dist = np.linalg.norm(pta-ptb)
    return dist


def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up/(2.0 * down)

    # checking if it is blinked
    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # detected face in face array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # the numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38],
                             landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44],
                              landmarks[47], landmarks[46], landmarks[45])

        # judge what to do for the eye blink
        if left_blink == 0 or right_blink == 0:
            sleep += 1
            drowsy = 0
            active = 0
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$sleep value: -", sleep)
            if sleep > 6:
                status = "SLEEPING!!!"
                playsound("alarm.wav")
                color = (255, 0, 0)

        elif left_blink == 1 or right_blink == 1:
            drowsy += 1
            sleep = 0
            active = 0
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$drowsy value: -", drowsy)
            if drowsy > 6:
                status = "DROWSY !"
                playsound("alarm.wav")
                color = (255, 0, 0)

        else:
            active += 1
            drowsy = 0
            sleep = 0
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$active value: -", active)
            if active > 6:
                status = "ACTIVE"
                color = (0, 255, 0)

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("frame", frame)
        cv2.imshow("Result of detector", face_frame)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break
