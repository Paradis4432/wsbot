from PIL import Image

img = Image.open("test01.jpg")
x, y = img.size

box = (0,0,x/2, y/2)
img2 = img.crop(box)

img2.save("test01crop.jpg")
img2.show()