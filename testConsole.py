import json
import requests
import os
# os.system("rembg i -m silueta wsimg.jpg wsimgtest.jpg")

cont = 2
sub = 3

# print(f"test{cont}.{sub}")

keys = ['ShYSmkGi19ztn5G7oDBPLUbN ', 'gcLYS11Z6jrL7MQP65mZ2y7C ', 'ds4c2TkgKKNZwJ1qSJ4sCtAG ', '5awd6A82Jthc1jA383R9z3VP ', 'zMPPPMiD2GCPVMDmfDdNDeLh ', 'CHjwZxPhVxRHbKPvWQhFCnFA ', 'eoSRfgSTAN75o6AQ1YUQ87h4 ']
currentKey = 0
headers = {
    'accept': '*/*',
    'X-API-Key': keys[currentKey],
}

response = requests.get('https://api.remove.bg/v1.0/account', headers=headers)

res = json.loads(response.text)

print(res["data"]["attributes"]["api"]["free_calls"])


def has0left(key):
    headers = {
        'accept': '*/*',
        'X-API-Key': keys[currentKey],
    }

    response = requests.get(
        'https://api.remove.bg/v1.0/account', headers=headers)
    callsLeft = json.loads(response.text)["data"]["attributes"]["api"]["free_calls"]

    print(response.text, keys[currentKey])
    print(f"found {keys[currentKey]} with {callsLeft} left")

    return callsLeft == 0

while has0left(currentKey) or True:
    if currentKey == len(keys) - 1: currentKey = 0
    else: currentKey += 1

print("final key to use " + keys[currentKey])