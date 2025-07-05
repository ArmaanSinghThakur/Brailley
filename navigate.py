import time

import cv2
import numpy as np
import pyttsx3 as pyttsx


speak= pyttsx.init()


speak= pyttsx.init()

voices= speak.getProperty('voices')
voice_id= "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_enUS_MarkM"
speak.setProperty("voice", voice_id)
speak.setProperty("rate", 140)

def say(text):
    print("Assistant:", text)
    speak.say(text)
    speak.runAndWait()


# CAMERA SETUP
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# SECTION LINE COLORS IN HSV
color_ranges = {
    "groceries": {
        "color": "blue",
        "lower": np.array([100, 150, 50]),
        "upper": np.array([130, 255, 255])
    },
    "pharmacy": {
        "color": "red",
        "lower": np.array([0, 120, 70]),
        "upper": np.array([10, 255, 255])
    },
    "bakery": {
        "color": "yellow",
        "lower": np.array([20, 100, 100]),
        "upper": np.array([30, 255, 255])
    },
    "checkout": {
        "color": "green",
        "lower": np.array([40, 70, 70]),
        "upper": np.array([90, 255, 255])
    }
}

def check_section(selected):

    if selected not in color_ranges:
        print("❌ Invalid section. Exiting.")
        cap.release()
        exit()

    selected_range = color_ranges[selected]
    return selected_range


# CORE FUNCTION
def decide_direction(cx, frame_center):

    if cx < frame_center - 70:
        return "Turn Left"

    elif cx > frame_center + 70:
        return " Turn Right"
    else:
        return " Go Straight"

# MAIN LOOP
def navigate(selected_range,destination_reached, selected):
    navi= True
    while navi:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get only the selected line color
        mask = cv2.inRange(hsv, selected_range["lower"], selected_range["upper"])


        top_half = mask[0:200, :]
        top_area = cv2.countNonZero(top_half)
        if top_area > 15000:
            destination_reached = True
        if not destination_reached:
            # Follow line in bottom area
            bottom_mask = mask.copy()
            bottom_mask[0:300, :] = 0
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            direction = "No Line Detected"
            cx = None

            if contours:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    frame_center = frame.shape[1] // 2
                    direction = decide_direction(cx, frame_center)

                    cv2.line(frame, (frame_center, 0), (frame_center, frame.shape[0]), (255, 255, 255), 2)
                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                    time.sleep(0.5)

            say(direction)
            # Show info
        if destination_reached:
            message = f"You have reached {selected.title()}"
            say(message)
            time.sleep(2)
            break

        else:
            cv2.putText(frame, f"Destination: {selected.title()}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)



        cv2.imshow("Store Navigator", frame)
        cv2.waitKey(1)
        cv2.imshow("Line Mask", mask)
        cv2.waitKey(1)
        key = cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


