from flask import Flask
from flask import render_template
from flask import request

import logging
import json
import os
import glob

app = Flask(__name__)
app.debug = True

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="basic.log")


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/negocios")
def negocios():
    with open("data.json", "r") as f:
        data = json.load(f)
    n = [name for name in data["negs"]]
    logging.debug(f"rendering negocios with negs: {n}")

    return render_template("negocios.html", neg=n)


@app.route("/negocios/<negocio>")
def renderNegocio(negocio=None):
    logging.debug("rendering negocios")
    with open("data.json", "r") as f:
        data = json.load(f)
    t = data["negs"][negocio]["types"]
    logging.debug(f"rendering tempNeg for: {negocio} with types {t}")

    return render_template("tempNeg.html", neg=negocio, types=t)


@app.route("/images/<negocio>/<t>")
def renderImages(negocio=None, t=None):
    logging.debug(f"rendering images for negocio: {negocio} in type: {t}")

    # mgsSrcs = [p for p in os.listdir("static/images/"+negocio+"/"+t+"//")]
    # imgsSrcs = glob.glob("static/cholo.cint.*.*.png")
    # comprehensive list as [i for i in glob glob.. "{t}.i.*.png"] to get list of lists to render them by group
    imgsSrcs = glob.glob(f"static/{negocio}.{t}.*.*.png")

    logging.debug("rendering images: " + str(imgsSrcs))

    return render_template("tempImagesNegocio.html", neg=negocio, t=t, srcs=imgsSrcs)


@app.route("/excel/<negocio>")
def getExcel(negocio=None):
    return 0


@app.route("/nuevoTipo/<neg>/<name>", methods=['POST'])
def newType(neg=None, name=None):
    logging.debug(f"creating new type: {name}")

    try:
        with open("data.json", "r") as f:
            data = json.load(f)

        data["negs"][neg]["types"].append(name)
        data["negs"][neg]["images"][name] = {}

        with open("data.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error("error adding new type: " + name)
        return "error"

    logging.debug("new type added")

    return "agregado"


@app.route("/newImageGroup/<neg>", methods=["POST"])
def newGroup(neg=None):
    logging.debug(f"adding new group for neg: {neg}")

    with open("data.json", "r") as f:
        data = json.load(f)

    # type:
    t = request.form["type"]

    # group
    # all groups in json neg type + 1 (len starts at 1)
    group = len(data["negs"][neg]["images"][t])
    logging.debug(f"saving images with neg {neg} type {t} group {group}")

    # images
    images = []
    for i in range(1, 4):
        # TODO fix forced 3 images
        file = request.files.get(f"image{i}")
        if file:
            filename = f"{neg}.{t}.{group}.{i}.png"
            file.save(os.path.join("static", filename))
            images.append(filename)
            logging.debug(f"saved image id {i}")

            # TODO pending remove bg image 

        else:
            logging.debug(f"got no images on upload")
            return "error"

    # file saved, add name in json
    data["negs"][neg]["images"].setdefault(t, {})[group] = {
        "images": images,
        "medidas": {
            "a": request.form.get("medida0"),
            "b": request.form.get("medida1"),
            "c": request.form.get("medida2")
        }
    }
    logging.debug(f"saved image name in json as {neg}.{t}.{group}.{i}")

    with open("data.json", "w") as f:
        json.dump(data, f)

    logging.debug("json saved")
    # TODO save data in excel send status to front process images once saved
    return render_template("nuevoGrupoAgregado.html", neg=neg)


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
