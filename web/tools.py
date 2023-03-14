import json
from PIL import Image
filename = "data.json"
import pandas as pd

def loadData():
    global filename
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def create_excel_from_json():
    data = loadData()
    # Load the JSON input into a Python object

    # Create an empty list to hold all the rows of the Excel file
    rows = []

    # Loop through each item in the "negs" dictionary
    for grupo, items in data["negs"].items():
        for tipo, details in items["images"].items():
            for index, item in details.items():
                # Create a new row for each item in the Excel file
                row = [
                    tipo,
                    index,
                    ", ".join(item["images"]),
                    item["alto"],
                    item["largo"],
                    item["ancho"],
                    item["costo"],
                    item["venta_menor"],
                    item["venta_mayor"],
                    item["stock"],
                    item["descripcion"],
                    item["uniqueID"]
                ]
                # Add the row to the list of rows
                rows.append(row)

    # Create a Pandas DataFrame from the list of rows
    df = pd.DataFrame(rows, columns=[
        "tipo",
        "grupo",
        "imágenes",
        "alto",
        "largo",
        "ancho",
        "costo",
        "venta_menor",
        "venta_mayor",
        "stock",
        "descripcion",
        "uniqueID"
    ])

    # Write the DataFrame to an Excel file
    writer = pd.ExcelWriter("data.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.save()


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
    img = Image.open(path).convert("RGBA")
    x, y = img.size
    card = Image.new("RGBA", (x, y), (255, 255, 255))
    card.paste(img, (0, 0, x, y), img)
    card.save(path, format="png")


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
