import cv2

# Load the image
img = cv2.imread("img4.1.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the edges in the image using Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Find the contours in the image
# Filter out small contours
contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour among the remaining ones
largest_contour = max(contours, key=cv2.contourArea)

# Draw a bounding box around the object in the image
x, y, w, h = cv2.boundingRect(largest_contour)
cv2.line(img, (x, y + h), (x, y), (0, 255, 0), 2)
cv2.line(img, (x, y + h), (x + w, y + h), (0, 255, 0), 2)

# Save the image with the bounding box
cv2.imwrite("img4.1.png", img)
