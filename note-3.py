import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk

# Landmark indices
WRIST, T1, T2, T3, T4, IF1, IF2, IF3, IF4, MF1, MF2, MF3, MF4, RF1, RF2, RF3, RF4, PF1, PF2, PF3, PF4 = range(21)

# Global variables
is_recognition_started = False
opening_root = None
recognition_root = None

# Color Palette
bg_color = "#392467"
text_color = "#FFD1E3"
subtext_color = "#A367B1"
button_color = "#5D3587"

def start_recognition():
    global is_recognition_started, opening_root, recognition_root
    is_recognition_started = True
    opening_position = opening_root.geometry()  # Get the position of the opening screen
    opening_root.destroy()

    # Hand Gesture Recognition
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    recognition_root = tk.Tk()
    recognition_root.title("Hand Gesture Recognition")
    recognition_root.geometry(opening_position)  # Set the dimensions and position of the recognition screen

    # Apply the color palette
    recognition_root.configure(bg=bg_color)

    # Create a frame for the footer
    footer_frame = tk.Frame(recognition_root)
    footer_frame.pack(side=tk.BOTTOM, pady=10)

    # Create a label for displaying text in the footer
    footer_label = tk.Label(footer_frame, text="No Sign Detected", font=("Impact", 30), bg=bg_color, fg=text_color, pady=10)
    footer_label.pack(fill=tk.X)

    label = tk.Label(footer_frame, text="", font=("Helvetica", 20), bg=bg_color)
    label.pack()

    def update_label_text():
        """
        Update the label text with the recognized gesture.
        """
        try:
            success, img = cap.read()
            if not success:
                raise ValueError("Failed to capture video frame")

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            lmList = []
            text = ""

            if results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                mpDraw.draw_landmarks(img, myHands, mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(myHands.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                # Your gesture recognition logic goes here
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

                if text:
                    footer_label.config(text="Sign Detected: {}".format(text))
                else:
                    footer_label.config(text="No Sign Detected")
                
                label.config(text=text)
            else:
                footer_label.config(text="Please raise your hand")
                label.config(text="")

            # Display the video feed
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            label.img = img
            label.configure(image=img)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Schedule the next update after 10 milliseconds
            recognition_root.after(10, update_label_text)

    # Schedule the first update
    update_label_text()
    recognition_root.mainloop()

    # Release the camera when the application is closed
    cap.release()
    cv2.destroyAllWindows()

# Opening Page
opening_root = tk.Tk()
opening_root.title("ASL Classification")
opening_root.geometry("600x500")  # Set the dimensions of the opening screen

# Apply the color palette
opening_root.configure(bg=bg_color)

opening_label = tk.Label(opening_root, text="ASL Classification\nusing Deep Learning", font=("Impact", 40), pady=20, bg=bg_color, fg=text_color)
opening_label.pack()

start_button = tk.Button(opening_root, text="Start", font=("Impact", 20), command=start_recognition, bg=button_color, fg=text_color)
start_button.pack()

# Text below the start button
below_start_button_text = tk.Label(opening_root, text="""
Submitted By
RONIT BAKSHI\t\t(11115602720)
SATWIK PANDEY\t\t(11615602720)
TANMAY PARNAMI\t\t(13115602720)
UTKARSH JAIN\t\t(13615602720)
                                   
Under the guidance of
Mr. Lokesh Meena,
Assistant Professor, CSE Department""", font=("Helvetica", 12), bg=bg_color, fg=subtext_color, pady=20)
below_start_button_text.pack()

opening_root.mainloop()
