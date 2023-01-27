import requests

headers = {
    'accept': 'image/*',
    'X-API-Key': 'zMPPPMiD2GCPVMDmfDdNDeLh',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'image_file': open('4wsimgTest1.png', 'rb'),
    'size': (None, 'auto'),
    'bg_color': (None, 'white'),
    'type': (None, 'product'),
    'type_level': (None, '1'),
}

response = requests.post(
    'https://api.remove.bg/v1.0/removebg', headers=headers, files=files)

if response.status_code == requests.codes.ok:
    with open("test01.jpg", 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
