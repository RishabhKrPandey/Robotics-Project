import cv2
import mediapipe as mp
import keyboard  # Use the keyboard library for key simulation
import time

cap = cv2.VideoCapture(0)  # Change to 0 if you have only one camera.
# Setting video capture resolution for the webcam to 1280x720 (px)
cap.set(3, 1280)
cap.set(4, 720)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def write_text(img, text, x, y):
    """ Writing (overlaying) text on the OpenCV camera view. """
    font = cv2.FONT_HERSHEY_SIMPLEX
    pos = (x, y)
    fontScale = 1
    fontColor = (255, 255, 255)  # White.
    lineType = 2
    cv2.putText(img, text, pos, font, fontScale, fontColor, lineType)

def steering_wheel():
    """ Uses the slope of the distance between middle fingers to create a virtual steering wheel for gaming. """
    prev_frame_time = 0
    new_frame_time = 0
    frame_skip = 5  # Process every 5th frame
    frame_count = 0

    # Flags to prevent repeated activation
    blue_nitro_active = False
    yellow_nitro_active = False

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break  # Exit the loop if the image capture fails

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Skip processing for this frame

        cv2.waitKey(1)  # Continuously refreshes the webcam frame every 1ms.
        img = cv2.flip(img, 1)
        img.flags.writeable = True  # Make the image writeable again
        results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # Processing video.

        landmarks = results.multi_hand_landmarks  # Fetches all the landmarks (points) on the hand.
        if landmarks:
            new_frame_time = time.time()
            fps = str(int(1 / (new_frame_time - prev_frame_time)))
            write_text(img, fps, 150, 500)
            prev_frame_time = new_frame_time

            if len(landmarks) >= 1:  # If at least one hand is in view.
                left_hand_landmarks = landmarks[1].landmark if len(landmarks) > 1 else landmarks[0].landmark
                right_hand_landmarks = landmarks[0].landmark if len(landmarks) > 1 else landmarks[0].landmark

                shape = img.shape
                width = shape[1]
                height = shape[0]

                left_mFingerX, left_mFingerY = (left_hand_landmarks[11].x * width), (left_hand_landmarks[11].y * height)
                right_mFingerX, right_mFingerY = (right_hand_landmarks[11].x * width), (right_hand_landmarks[11].y * height)

                # Avoid division by zero
                if right_mFingerX != left_mFingerX:
                    slope = ((right_mFingerY - left_mFingerY) / (right_mFingerX - left_mFingerX))
                else:
                    slope = 0  # Default to 0 if hands are aligned vertically

                sensitivity = 0.3
                if abs(slope) > sensitivity:
                    if slope < 0:
                        print("Turn left.")
                        write_text(img, "Left.", 360, 360)
                        keyboard.release("w")
                        keyboard.release("a")
                        keyboard.press("a")
                    elif slope > 0:
                        print("Turn right.")
                        write_text(img, "Right.", 360, 360)
                        keyboard.release("w")
                        keyboard.release("a")
                        keyboard.press("d")
                else:
                    print("Keeping straight.")
                    write_text(img, "Straight.", 360, 360)
                    keyboard.release("a")
                    keyboard.release("d")
                    keyboard.press("w")

                # Check for thumb gestures for nitro activation
                right_thumb_x = right_hand_landmarks[4].x  # Right thumb tip X coordinate
                left_thumb_x = left_hand_landmarks[4].x  # Left thumb tip X coordinate

                # Define the threshold for gesture detection
                if right_thumb_x < 0.4 and not blue_nitro_active:  # Right thumb towards the left side
                    print("Activating Blue Nitro.")
                    keyboard.press("space")  # Simulate pressing space for blue nitro
                    time.sleep(0.1)  # Hold the key for a short duration
                    keyboard.release("space")  # Release the key
                    blue_nitro_active = True  # Set the flag to prevent repeated activation
                elif right_thumb_x >= 0.4:
                    blue_nitro_active = False  # Reset the flag when the gesture is not detected

                if left_thumb_x > 0.6 and not yellow_nitro_active:  # Left thumb towards the right side
                    print("Activating Yellow Nitro.")
                    keyboard.press("space")
                    keyboard.press("space")# Simulate pressing 'x' for yellow nitro
                    time.sleep(0.1)  # Hold the key for a short duration
                    keyboard.release("space")  # Release the key
                    yellow_nitro_active = True  # Set the flag to prevent repeated activation
                elif left_thumb_x <= 0.6:
                    yellow_nitro_active = False  # Reset the flag when the gesture is not detected

            else:
                print("No hands detected.")
                write_text(img, "No hands detected.", 360, 360)

            for hand_landmarks in landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Recognition", img)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    steering_wheel()