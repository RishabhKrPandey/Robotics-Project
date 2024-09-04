import cv2

cap = cv2.VideoCapture(0)

# preprocessing for our project
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # cv2.imshow("cam-recording", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # preprocessing the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15,15), 0)
    _, thresh = cv2.threshold(blurred, 200,225, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow('detected led', frame)


cap.release()
cv2.destroyAllWindows()


