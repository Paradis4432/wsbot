from PIL import Image, ImageDraw

# Load the image
image = Image.open('KO.ARR.cholo.test.10.3.png')

# Convert the image to grayscale
image = image.convert('L')

# Find the bounding box coordinates
bbox = image.getbbox()

# Draw a rectangle around the image
draw = ImageDraw.Draw(image)
draw.rectangle(bbox, outline='red')

# Save the image
image.save('1.KO.ARR.cholo.test.10.3.png')
