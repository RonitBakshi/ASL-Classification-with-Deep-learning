import cv2
import mediapipe as mp
 
WRIST = 0
T1 = 1
T2 = 2
T3 = 3
T4 = 4
IF1 = 5
IF2 = 6
IF3 = 7
IF4 = 8
MF1 = 9
MF2 = 10
MF3 = 11
MF4 = 12
RF1 = 13
RF2 = 14
RF3 = 15
RF4 = 16
PF1 = 17
PF2 = 18
PF3 = 19
PF4 = 20
# ctrl + c : Stop execution 
# ctrl + l : Clear Terminal

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success , img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:
        myHands = results.multi_hand_landmarks[0]

        mpDraw.draw_landmarks(img, myHands, mpHands.HAND_CONNECTIONS)

        for id,lm in enumerate(myHands.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id,cx,cy])

        text = ''

        if lmList[PF1][1]-lmList[WRIST][1]:

            tan = (lmList[PF1][2]-lmList[WRIST][2])/(lmList[PF1][1]-lmList[WRIST][1])

            if  -0.9 < tan < 0.9: # Hand is Sideways
                IFU = lmList[IF2][1] > lmList[IF4][1]
                MFU = lmList[MF2][1] > lmList[MF4][1]
                RFU = lmList[RF2][1] > lmList[RF4][1]
                PFU = lmList[PF2][1] > lmList[PF4][1]

                if RFU and PFU:
                    if lmList[T4][2]-lmList[IF4][2] > 40:
                        text = 'C'
                    elif lmList[T4][2]-lmList[IF4][2] < 25:
                        text = 'O'
                else:
                    if MFU and IFU:
                        if lmList[MF4][2] - lmList[IF2][2] > 15:
                            text = 'P'
                        else:
                            text = 'H'
                    elif not MFU and IFU: 
                        if lmList[WRIST][2] < lmList[T1][2]:  
                            text = 'Q'
                        else: 
                            text = 'G'
            else: # Straight Hand
                IFU = lmList[IF1][2] > lmList[IF4][2]
                MFU = lmList[MF1][2] > lmList[MF4][2]
                RFU = lmList[RF1][2] > lmList[RF4][2]
                PFU = lmList[PF1][2] > lmList[PF4][2]
                TU = lmList[T4][1] > lmList[T2][1]

                if not PFU and not RFU and not MFU and not IFU and TU:
                    text = 'A'
                elif PFU and RFU and MFU and IFU and not TU:
                    text = 'B'
                elif not PFU and not RFU and not MFU and IFU and not TU:
                    if lmList[IF4][2] - lmList[IF3][2] > 0:
                        text = 'X'
                    else:
                        text = 'D'
                elif not PFU and not RFU and not MFU and not IFU and not TU:
                    if lmList[T4][2] > lmList[IF4][2]:
                        text = 'E'
                    elif lmList[T4][2] < lmList[IF2][2]:
                        if lmList[T3][1] < lmList[IF3][1] and lmList[T4][1] > lmList[MF3][1]:
                            text = 'T'
                        elif lmList[T4][1] < lmList[MF4][1]:
                            text = 'N'
                    elif lmList[T4][1] < lmList[MF2][1]:
                        text = 'S'
                    else:
                        text = 'M'
                elif PFU and RFU and MFU and not IFU and not TU:
                    text = 'F'
                elif PFU and not RFU and not MFU and not IFU and not TU:
                    text = 'I'
                elif not PFU and not RFU and MFU and IFU:
                    if lmList[MF4][1] > lmList[IF4][1]:
                        text = 'R'
                    elif lmList[T4][1] > lmList[MF1][1]:
                        text = 'K'
                    elif lmList[IF4][1] - lmList[MF4][1] > 24:
                        text = 'V'
                    else:
                        text = 'U'
                elif not PFU and not RFU and not MFU and IFU and TU:
                    text = 'L'
                elif not PFU and RFU and MFU and IFU and not TU:
                    text = 'W'
                elif PFU and not RFU and not MFU and not IFU and TU:
                    text = 'Y'

        cv2.putText(img,text,(100,100),cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 5)

    cv2.imshow("Image",img)

    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()