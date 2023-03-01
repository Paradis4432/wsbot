import json
import requests
import logging

from tools import *

# general values
keys = ['ShYSmkGi19ztn5G7oDBPLUbN', 'gcLYS11Z6jrL7MQP65mZ2y7C', 'ds4c2TkgKKNZwJ1qSJ4sCtAG',
        '5awd6A82Jthc1jA383R9z3VP', 'zMPPPMiD2GCPVMDmfDdNDeLh', 'eoSRfgSTAN75o6AQ1YUQ87h4']
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

    return True
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
        # status = removeBG(pending)
        status = "success"

        if status == "success":
            logging.debug(f"successfully processed file {pending}")
            continue

        logging.debug(f"stopping imageEdit")
        saveValue("stopNext", True)
        saveValue("currentStatus", "ERROR")
        return


def startProcessing():
    global currentKey
    # if stopNext: log and stop
    data = loadData()
    if data["stopNext"]:
        logging.debug("found stop next to be true, stopping.")
        return

    conts = 0
    const = len(keys) + 2
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

    data = loadData()

    if len(data["pending"]) == 0:
        logging.debug("no pending found, returning")
        return

    pendingFiles = data["pending"]
    data["processing"] = pendingFiles
    data["pending"] = []

    saveData(data)

    logging.debug(f"processing {len(pendingFiles)} {pendingFiles} files")
    status = processFiles(pendingFiles)

    data = loadData()
    if data["stopNext"]:
        logging.debug("found stop next to be true, stopping.")
        return

    with open("data.json", "r") as f:
        data = json.load(f)
        processed = data["processing"]
        data["processing"] = []
        data["processed"].extend(processed)
    saveData(data)

# add arrows to img