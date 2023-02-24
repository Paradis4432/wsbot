

from flask import Flask
from flask import render_template
import logging
import json
import os
import glob



neg="cholo"
t = "mochilas"
with open("data.json", "r") as f:
    data = json.load(f)
group = len(data["negs"][neg]["images"][t])
print(group)
