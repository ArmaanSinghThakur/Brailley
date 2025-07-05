import cv2
import numpy as np

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Define color ranges for sections
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

# Ask user for destination
print("Available Sections:")
for section in color_ranges:
    print(f"- {section.title()}")

selected = input("\nEnter destination: ").strip().lower()
if selected not in color_ranges:
    print("❌ Invalid section.")
    cap.release()
    exit()

selected_range = color_ranges[selected]
print(f"\n🧭 Navigating to: {selected.title()} (Line Color: {selected_range['color']})")

def decide_direction(cx, frame_center):
    if cx < frame_center - 50:
        return "⬅️ Turn Left"
    elif cx > frame_center + 50:
        return "➡️ Turn Right"
    else:
        return "⬆️ Go Straight"

destination_reached = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create color mask
    mask = cv2.inRange(hsv, selected_range["lower"], selected_range["upper"])

    # Detect large color blob in top half (as destination marker)
    top_half = mask[0:200, :]
    top_area = cv2.countNonZero(top_half)

    # Threshold depends on lighting & marker size — tune as needed
    if top_area > 15000:
        destination_reached = True

    direction = "❓ No Line Detected"

    if not destination_reached:
        # Follow line in bottom area
        bottom_mask = mask.copy()
        bottom_mask[0:300, :] = 0

        contours, _ = cv2.findContours(bottom_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                frame_center = frame.shape[1] // 2
                direction = decide_direction(cx, frame_center)

                # Draw indicators
                cv2.line(frame, (frame_center, 0), (frame_center, frame.shape[0]), (255, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

    # Show messages
    if destination_reached:
        message = f"🎉 You have reached {selected.title()}"
        cv2.putText(frame, message, (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 100), 3)
        break

    else:
        cv2.putText(frame, f"Destination: {selected.title()}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, f"Direction: {direction}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 2)

    cv2.imshow("Store Navigation", frame)
    cv2.imshow("Line Mask", mask)

    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
