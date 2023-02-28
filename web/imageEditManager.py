import json


# general values
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="imageEdit.log")
keys = ['ShYSmkGi19ztn5G7oDBPLUbN', 'gcLYS11Z6jrL7MQP65mZ2y7C', 'ds4c2TkgKKNZwJ1qSJ4sCtAG',
        '5awd6A82Jthc1jA383R9z3VP', 'zMPPPMiD2GCPVMDmfDdNDeLh', 'eoSRfgSTAN75o6AQ1YUQ87h4']
currentKey = 0

# set of tools to edit image


def has0left():
    global currentKey

    response = requests.get(
        'https://api.remove.bg/v1.0/account', headers={
            'accept': '*/*',
            'X-API-Key': keys[currentKey],
        })
    callsLeft = json.loads(response.text)[
        "data"]["attributes"]["api"]["free_calls"]
    # logging.debug(response.text, keys[currentKey])
    logging.debug(f"found {keys[currentKey]} with {callsLeft} left")

    return callsLeft == 0


def getAllCallsLeft():
    # TODO
    return 0


def anyCallLeft():
    # TODO
    return True


def removeBG(path):
    path = "static/" + path
    global currentKey

    try:
        logging.debug(f"using key: {keys[currentKey]} for image {path}")
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': keys[currentKey]}
        )

        if response.status_code == requests.codes.ok:
            with open(path, 'wb') as out:
                logging.debug(f"image {path} successfully removed bg")
                out.write(response.content)
                logging.debug("and saved")
        else:
            logging.debug(f"Error: {response.status_code} {response.text}")
            return "error1"
    except Exception as e:
        logging.debug("error cleaning img:")
        logging.debug(e)
        return "error2"
    return "success"


def addWhiteBackground(path):
    try:
        img = Image.open(path).convert("RGBA")
        x, y = img.size
        card = Image.new("RGBA", (x, y), (255, 255, 255))
        card.paste(img, (0, 0, x, y), img)
        card.save(path, format="png")

        return "success"
    except Exception as e:
        logging.debug("error pasting white bg")
        logging.debug(e)
        return "error"


def main():
    # if stopNext: log and stop 
    
    with open("data.json", "r") as f:
        data = json.load(f)
        if data["stopNext"]:
            logging.debug("found stop next to be true, stopping.")
            return

    conts = 0
    while has0left():
        currentKey = (currentKey + 1) % len(keys)
        conts += 1
        if conts == len(keys) + 1:
            logging.debug("no calls left in keys")
            # stop next
            return

    logging.debug(f"using key {keys[currentKey]}")

    # status = removeBG(data["pending"][0])
    # status != success : stop next
    # else remove data pending 0

    logging.debug("starting loop")
    continueLoop = True
    while continueLoop:
        with open("data.json", "r") as f:
            data = json.load(f)

        if len(data["pending"]) == 0:
            logging.debug("no pending found, waiting")
            # wait

        pending_files = data["pending"]
        data["processing"] = pending_files
        data["pending"] = []

        with open("data.json", "w") as f:
            json.dump(data, f)

        for pending in pending_files:
            status = removeBG(pending)
            if status != "success":
                logging.debug(f"stopping imageEdit")
                with open("data.json", "r") as f:
                    data = json.load(f)
                    data["stopNext"] = True
                    data["currentStatus"] = "ERROR"
                with open("data.json", "w") as f:
                    json.dump(data, f)
                    
                continueLoop = False
                break
            


        with open("data.json", "r") as f:
            data = json.load(f)
            processed = data["processing"]
            data["processing"] = []
            data["processed"].extend(processed)
        with open("data.json", "w") as f:
            json.dump(data, f)

        # log

    return 0


# add arrows to img

