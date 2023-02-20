from flask import Flask
from flask import render_template
import logging
import json
import os

app = Flask(__name__)
app.debug = True

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="basic.log")


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
    logging.debug("rendering negocios")
    with open("data.json", "r") as f:
        data = json.load(f)
    t = data["negs"][negocio]["types"]
    logging.debug("rendering tempNeg for: " +
                  negocio + " with types: " + str(t))

    return render_template("tempNeg.html", neg=negocio, types=t)


@app.route("/images/<negocio>/<t>")
def renderImages(negocio=None, t=None):
    logging.debug("rendering images for negocio: " +
                  negocio + " in type: " + t)

    imgsSrcs = [p for p in os.listdir("static/images/"+negocio+"/"+t+"//")]
    logging.debug("rendering images: " + str(imgsSrcs))

    return render_template("tempImagesNegocio.html", neg=negocio, t=t, srcs=imgsSrcs)


@app.route("/excel/<negocio>")
def getExcel(negocio=None):
    return 0


@app.route("/nuevoTipo/<neg>/<name>", methods=['POST'])
def newType(neg=None, name=None):
    logging.debug("creating new type: " + name)

    try:
        with open("data.json", "r") as f:
            data = json.load(f)

        data["negs"][neg]["types"].append(name)

        with open("data.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error("error adding new type: " + name)
        return "error"

    logging.debug("new type added")

    return "agregado"


@app.rout("/newImageGroup/<neg>", methods=["POST"])
def newGroup(neg=None):
    logging.debug("adding new group for neg: " + neg)
    # type:
    t = request.form["type"]
    print(t)

    # group
    # all groups in json neg type + 1

    # images
    for i in range(1, 4):
        # TODO fix forced 3 images
        file = request.files['image{}'.format(i)]
        # file.save
        # filename = 0 1 2

    # medidas<
    m0 = request.form["medida0"]
    m1 = request.form["medida1"]
    m2 = request.form["medida2"]

    # TODO save data in excel send status to front process images once saved

'''

TODO
test in mobile

<!DOCTYPE html>
<html>
  <body>
    <label for="cameraFileInput">
      <input
        id="cameraFileInput"
        type="file"
        accept="image/*"
        capture="environment"
      />
    </label>

    <img id="pictureFromCamera" />
  </body>
</html> 

'''
