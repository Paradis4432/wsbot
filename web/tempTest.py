

from flask import Flask
from flask import render_template
import logging
import json
import os
import glob

from tools import *

data = loadData()
neg = "cholo"
t = "mochilas"
val = data["negs"][neg]["images"][t]
print(val)
for i in val:
    print(i)
    # group data["negs"][neg]["images"][t][i]
    print(data["negs"][neg]["images"][t][i]["images"])

val1 = [val[i]["images"] for i in val]
print(val1)
