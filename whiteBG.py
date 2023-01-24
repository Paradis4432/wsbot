from PIL import Image

img = Image.open("wsimg.1.jpg").convert("RGBA")
x, y = img.size
card = Image.new("RGBA", (x, y), (255, 255, 255))
card.paste(img, (0, 0, x, y), img)
card.save("wsimg1.1.png", format="png")