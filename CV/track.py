import numpy as np
import cv2


cap=cv2.VideoCapture(0)

def nothing(x):
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("max", "Trackbars", 100, 500, nothing)
cv2.createTrackbar("min", "Trackbars", 0, 500, nothing)










     
def detect_cubes(image):
    global max,min
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Use Canny Edge Detector to detect edges
    edges = cv2.Canny(blurred, min, max)
    cv2.imshow("Cubes edges", edges)
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Iterate through the contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02  * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # If the polygon has 4 vertices, we assume it's a square (2D projection of a cube face)
        if len(approx) <=8 and len(approx) >=4 and (cv2.contourArea(contour)>200):
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            # Draw the contour (cube face) on the original image
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 5)
            #hull = cv2.convexHull(contour)
            #cv2.drawContours(image, [hull], -1, (0, 255, 0), 2)
    return image

# Load image from file
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    max = cv2.getTrackbarPos("max", "Trackbars")
    min = cv2.getTrackbarPos("min", "Trackbars")

    # Detect cubes
    output_image = detect_cubes(frame)

    # Display the output
    cv2.imshow("Cubes Detected", output_image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
