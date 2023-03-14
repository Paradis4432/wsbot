

import pandas as pd
from flask import Flask
from flask import render_template
import logging
import json
import os
import glob

from tools import *

data = loadData()


neg = "marian"
t = "Gorras_rotas"
firsts = [data["negs"][neg]["images"][t][x]["images"][0]
          for x in data["negs"][neg]["images"][t].keys()]
# print(firsts)

names = ["test.asd.0.1.png", "test.asd.0.2.png", "test.asd.0.3.png"]

path = "./static/"


import json
import pandas as pd

# old
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


create_excel_from_json(data)