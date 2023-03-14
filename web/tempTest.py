

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

path="./static/"

for name in names:
    
    p = path + name
    img = Image.open(p).convert("RGBA")
    print(img)
    x, y = img.size
    print(x,y)
    card = Image.new("RGBA", (x, y), (255, 255, 255))
    card.paste(img, (0, 0, x, y), img)
    card.save(p, format="png")
    print("saved")
