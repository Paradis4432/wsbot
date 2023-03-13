

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

for x in os.listdir("./static"):
    n = f"./static/{x}"
    image = Image.open(n)
    image.thumbnail((1200, 800))
    image.save(n)
    print("changed: " + n)
