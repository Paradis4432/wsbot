# rembg i wsimg.jpg wsimg1.jpg              removes background
# scp me.jpg root@50.116.47.159:/root/fisica/   moves to server

# Requires "requests" to be installed (see python-requests.org)
# import requests

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('wsimg.jpg', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'ShYSmkGi19ztn5G7oDBPLUbN'},
)
if response.status_code == requests.codes.ok:
    with open('wsimg.1.jpg', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)


'''
try:
        p = "images/img" + str(cont) + "." + str(subcont) + ".png"
        print("rembg i -m u2net " + p + " " + p)
        os.system("rembg i -m u2net " + p + " " + "images1/Timg" +
                  str(cont) + "." + str(subcont) + ".png")

    except Exception as e:
        print("error cleaning img:")
        print(e)

    try:
        img = Image.open("images1/Timg" + str(cont) + "." +
                         str(subcont) + ".png").convert("RGBA")
        x, y = img.size
        card = Image.new("RGBA", (x, y), (255, 255, 255))
        card.paste(img, (0, 0, x, y), img)
        card.save("images1/Timg" + str(cont) + "." +
                  str(subcont) + ".png", format="png")
    except Exception as e:
        print("error cleaning img:")
        print(e)
'''