import cv2

# Load the image
img = cv2.imread("KO.ARR.cholo.test.10.3.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the edges in the image using Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Find the contours in the image
contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours
MIN_CONTOUR_AREA = 200  # Adjust as needed
contours = [c for c in contours if cv2.contourArea(c) > MIN_CONTOUR_AREA]

# Draw bounding boxes around the remaining contours
for c in contours:
    # Get the bounding rectangle coordinates
    x, y, w, h = cv2.boundingRect(c)
    # Draw the bounding box
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 1)

# Find the largest contour among the remaining ones
largest_contour = max(contours, key=cv2.contourArea)

# Draw a bounding box around the object in the image
x, y, w, h = cv2.boundingRect(largest_contour)
cv2.line(img, (x, y + h), (x, y), (0, 255, 0), 2)
cv2.line(img, (x, y + h), (x + w, y + h), (0, 255, 0), 2)

# Save the image with the bounding box
cv2.imwrite("1.KO.ARR.cholo.test.10.3.png", img)
