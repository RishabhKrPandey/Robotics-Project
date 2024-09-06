import cv2

image = cv2.imread('IMAGE.jpeg')

if image is None:
    print("Image Not Found!")
else:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 0)
    _, thresholded_image = cv2.threshold(blurred_image, 220, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite('Output.jpg', image)
    cv2.imshow('Detected Bright Spots with Bounding Boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
