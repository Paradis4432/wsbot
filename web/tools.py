import json
from PIL import Image
filename = "data.json"


def loadData():
    global filename
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def saveData(data):
    global filename
    with open(filename, "w") as f:
        json.dump(data, f)


def saveValue(path, value):
    data = loadData()
    data[path] = value
    saveData(data)

def delValue(path, name):
    
    data = loadData()
    data[path].remove(name)
    saveData(data)


def addWhiteBackground(path):
    try:
        logging.debug(f"Adding white background to {path}")
        img = Image.open(path).convert("RGBA")
        x, y = img.size
        card = Image.new("RGBA", (x, y), (255, 255, 255))
        card.paste(img, (0, 0, x, y), img)
        card.save(path, format="png")
        logging.debug("Added white background")
        return "white background"
    except Exception as e:
        logging.debug(f"error pasting white bg {e}")
        return "error "





def getAnyCallLeftInKeys():
    for i in keys:
        r = requests.get('https://api.remove.bg/v1.0/account', headers={
            'accept': '*/*',
            'X-API-Key': i,
        })
        callsLeft = json.loads(r.text)[
            "data"]["attributes"]["api"]["free_calls"]
        if callsLeft > 0:
            return True
    return False
