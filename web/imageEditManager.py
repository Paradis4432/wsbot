import json
import requests
import logging
import cv2

from .tools import *

# general values
keys = ['ShYSmkGi19ztn5G7oDBPLUbN', 'gcLYS11Z6jrL7MQP65mZ2y7C', 'ds4c2TkgKKNZwJ1qSJ4sCtAG',
        '5awd6A82Jthc1jA383R9z3VP', 'zMPPPMiD2GCPVMDmfDdNDeLh', 'eoSRfgSTAN75o6AQ1YUQ87h4']


def getKeys():
    return keys


currentKey = 0


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
        logging.debug(f"error cleaning img: {e}")
        return "error2"
    return "success"


def processFiles(pendingFiles):
    for pending in pendingFiles:
        status = removeBG(pending)

        if status == "success":
            logging.debug(f"successfully processed file {pending}")
            continue

        logging.debug(f"stopping imageEdit for rm bg")
        saveValue("stopNext", True)
        saveValue("currentStatus", "ERROR RMBG")
        return


def addArrows(pendingFiles):
    status = "success"
    for pending in pendingFiles:

        try:
            # add arrows to pending
            img = cv2.imread(f"./static/{pending}")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 20, 100)
            contours, _ = cv2.findContours(
                edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.line(img, (x, y + h), (x, y), (0, 255, 0), 2)
            cv2.line(img, (x, y + h), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite(f"./static/{pending}", img)

            logging.debug(f"successfully added arrows to {pending}")
        except Exception as e:
            logging.debug(f"error adding arrows to {pending}: {e}")
            logging.debug(f"stopping imageEdit for add arrows")
            saveValue("stopNext", True)
            saveValue("currentStatus", "ERROR ARROWS")
            return "errorArrows"


async def processPendingFiles(pendingKey, processingKey, processedKey, processFunc, processMsg):
    data = loadData()
    if len(data[pendingKey]) > 0:
        logging.debug(f"found {len(data[pendingKey])} {pendingKey}")
        pendingFiles = data[pendingKey]
        data[processingKey] = pendingFiles
        data[pendingKey] = []
        saveData(data)

        logging.debug(f"{processMsg} {len(pendingFiles)} {pendingFiles} files")
        processFunc(pendingFiles)

        data = loadData()
        if data["stopNext"]:
            logging.debug(
                f"found stop next to be true in {pendingKey}, stopping.")
            return

        with open("data.json", "r") as f:
            data = json.load(f)
            processed = data[processingKey]
            data[processingKey] = []
            data[processedKey].extend(processed)
        saveData(data)


async def startProcessing():
    global currentKey
    logging.debug("not processing keys")
    return 
    # if stopNext: log and stop
    data = loadData()
    if data["stopNext"]:
        logging.debug("found stop next to be true, stopping.")
        return

    conts = 0
    while has0left():
        currentKey = (currentKey + 1) % len(keys)
        conts += 1
        if conts < len(keys) + 1:
            continue
        logging.debug("no calls left in keys")
        saveValue("stopNext", True)
        saveValue("currentStatus", "NoCallsLeftInKeys")
        continueLoop = False
        return

    logging.debug(f"using key {keys[currentKey]}")

    # await processPendingFiles("pendingRmBg", "processingRmBg", "processedRmBg", processFiles, "processingRmBg")

    # await processPendingFiles("pendingAddArr", "processingAddArr", "processedAddArr", addArrows, "processingAddArr")


def getAllCallsLeft():
    calls = 0
    for i in keys:
        r = requests.get('https://api.remove.bg/v1.0/account', headers={
            'accept': '*/*',
            'X-API-Key': i,
        })
        callsLeft = json.loads(r.text)[
            "data"]["attributes"]["api"]["free_calls"]
        calls += callsLeft
    logging.debug(f"found a total of {calls} calls left")
    return calls


def resizeImage():
    # for filename in os.listdir(input_dir):
    # if filename.endswith('.jpg') or filename.endswith('.png'):  # check if the file is an image
    #    with Image.open(os.path.join(input_dir, filename)) as im:
    #        im.thumbnail(max_size)  # resize the image to fit within the maximum size
    #        im.save(os.path.join(output_dir, filename))  # save the resized image to the output folder
    ...
