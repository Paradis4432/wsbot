import cv2
import numpy as np
n = "img21.1.png"
# Load the image
img = cv2.imread(n)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the product in the image using edge detection
edges = cv2.Canny(gray, 50, 150)
cv2.imwrite("a" + n, edges)

# Find the contours in the image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#print(contours)

# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)


# Draw a box around the largest contour
x, y, w, h = cv2.boundingRect(largest_contour)
cv2.line(img, (x, y + h), (x, y), (0, 255, 0), 2)
cv2.line(img, (x, y + h), (x + w, y + h), (0, 255, 0), 2)

# Display the image with the box
#cv2.imshow("Image with Box", img)
cv2.imwrite("Tnew" + n, img)
cv2.waitKey(0)
cv2.destroyAllWindows()