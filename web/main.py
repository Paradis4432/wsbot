from flask import Flask
from flask import render_template
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="basic.log")

data = 0
try:
    logging.debug("getting negocios")

    with open('data.json') as f:
        data = json.loads(f.read())

    logging.debug("got data as dict:")
    logging.debug(data)

except Exception as e:
    logging.critical("negocios not found")
    logging.critical(e)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/negocios")
def negocios():
    n = [name for name in data["negs"]]
    logging.debug("rendering negocios with negs: " + str(n))

    return render_template("negocios.html", neg=n)


@app.route("/negocios/<negocio>")
def renderNegocio(negocio=None):
    t = data["negs"][negocio]["types"]
    logging.debug("rendering tempNeg for: " + negocio + " with types: " + str(t))

    return render_template("tempNeg.html", neg=negocio, types=t)

@app.route("/fotos/<negocio>/<t>")
def renderImages(negocio=None, t=None):
    logging.debug("rendering images for negocio: " + negocio + " in type: " + t)
    return render_template("tempImagesNegocio.html", neg=negocio, t=t)


@app.route("/excel/<negocio>")
def getExcel(negocio=None):
    return 0
