from .imageEditManager import *
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

import logging
import json
import os
import glob
import asyncio

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="basic.log")

# TODO: arrows for images, excel loading
# fix max size done
# TODO: change upload to button no
# TODO: cambiar cargado de imagenes boton -> grupo info etc
# TODO: add button on new type

# idea: add tags for each group of images no
@app.route("/")
def index():
    data = loadData()

    return render_template("main.html", data=[len(data["pendingRmBg"]), len(data["processingRmBg"]),
                                              len(data["pendingAddArr"]), len(data["processingAddArr"]), data["currentStatus"], data["stopNext"]])


@app.route("/getKeys")
def getKeysFromExternalFile():
    return getKeys()


@app.route("/negocios")
def negocios():
    data = loadData()

    n = [name for name in data["negs"]]
    logging.debug(f"rendering negocios with negs: {n}")

    return render_template("negocios.html", neg=n)


@app.route("/negocios/<negocio>")
def renderNegocio(negocio=None):
    logging.debug("rendering negocios")
    data = loadData()
    t = data["negs"][negocio]["types"]
    logging.debug(f"rendering tempNeg for: {negocio} with types {t}")

    return render_template("tempNeg.html", neg=negocio, types=t)


@app.route("/images/<neg>/<t>")
def renderImages(neg=None, t=None):
    logging.debug(f"rendering images for negocio: {neg} in type: {t}")

    data = loadData()
    imgsSrcs = data["negs"][neg]["images"][t]

    logging.debug("rendering images: " + str(imgsSrcs))

    return render_template("tempImagesNegocio.html", neg=neg, t=t, srcs=imgsSrcs)


@app.route("/excel/<negocio>")
def getExcel(negocio=None):
    return 0

@app.route("/test", methods=["POST"])
def test():
    x = request.form
    return "test"

@app.route("/nuevoTipo/<neg>/<name>", methods=['POST'])
def newType(neg=None, name=None):
    logging.debug(f"creating new type: {name}")

    try:
        data = loadData()

        data["negs"][neg]["types"].append(name)
        data["negs"][neg]["images"][name] = {}

        saveData(data)
    except Exception as e:
        logging.error("error adding new type: " + name)
        return "error"

    logging.debug("new type added")

    return "agregado"


def getUniqueId():
    data = loadData()
    last_id = int(data["lastID"], 16)
    new_id = last_id + 1
    data["lastID"] = hex(new_id)[2:].upper()
    saveData(data)
    return hex(new_id)[2:].upper()  # convert new_id to a hexadecimal string


@app.route("/newImageGroup/<neg>", methods=["POST"])
def newGroup(neg=None):
    logging.debug(f"adding new group for neg: {neg}")
    uniqueID = getUniqueId()

    data = loadData()

    t = request.form["type"]

    # a = request.form.get("image1KO") DELETE
    # group
    # all groups in json neg type + 1 (len starts at 1)
    group = len(data["negs"][neg]["images"][t])
    logging.debug(f"saving images with neg {neg} type {t} group {group}")

    images = []
    # TODO remove some tabs with a function taking i as arg maybe
    for i in range(1, 4):
        # TODO fix forced 3 images
        file = request.files.get(f"image{i}")
        if not file:
            logging.debug(f"got no images on upload of file {i}")
            continue
        # if keep original true in view dont add to data.pending .json else add
        # if keep original true in view add "KO" at start of file name
        filename = ""
        if request.form.get(f"image{i}KO") == "on":
            filename += "KO."
        if request.form.get(f"image{i}ARR") == "on":
            filename += "ARR."
        filename += f"{neg}.{t}.{group}.{i}.png"

        # if image{i}ARR add to data.pendingAddArr else dont add arrows

        if request.form.get(f"image{i}KO") == "on":
            logging.debug(f"found image id {i} to have KO")
        else:
            data["pendingRmBg"].append(filename)
            logging.debug(f"added {filename} to pendingRmBg")
            
        if request.form.get(f"image{i}ARR") == "on":
            logging.debug(f"adding image {i} to pending arrows")
            data["pendingAddArr"].append(filename)
        else:
            logging.debug(f"{filename} found to not have ARR")

        file.save(os.path.join("static", filename))
        images.append(filename)
        logging.debug(f"saved image id {i}")

    # file saved, add name in json
    data["negs"][neg]["images"].setdefault(t, {})[group] = {
        "images": images,
        "medida0": request.form.get("medida0") or "not found",
        "medida1": request.form.get("medida1") or "not found",
        "medida2": request.form.get("medida2") or "not found",
        "costo": request.form.get("costo") or "not found",
        "venta_menor": request.form.get("venta_menor") or "not found",
        "venta_mayor": request.form.get("venta_mayor") or "not found",
        "stock": request.form.get("stock") or "not found",
        "descripcion": request.form.get("descripcion") or "not found",
        "uniqueID": uniqueID
    }

    logging.debug(f"saved image name in json as {neg}.{t}.{group}.{i}")

    saveData(data)

    logging.debug("json saved")
    # TODO save data in excel send status to front process images once saved
    return render_template("nuevoGrupoAgregado.html", neg=neg)


@app.route("/processPending")
async def processImages():
    logging.debug("starting processing images")
    asyncio.create_task(startProcessing())
    return "empezando"


@app.route("/reset")
def reset():
    logging.debug("reseting")
    data = loadData()
    data["stopNext"] = False
    data["currentStatus"] = "OK"
    saveData(data)

    return "reseteando"


@app.route("/download/<img>")
def download(img=None):
    logging.debug(f"downloading image {img}")
    return send_file(os.path.join("static", img), mimetype='image/jpeg', as_attachment=True)


'''
test for static folder
There are several ways you can reduce the size of the "static" folder containing images, while maintaining fast access to them. Here are a few suggestions:

Optimize image files: You can use tools such as ImageOptim or TinyPNG to compress the size of your image files without reducing their quality. This can significantly reduce the file size of your images, while keeping their visual appeal intact.

Use responsive images: Instead of serving large images to all devices, you can use responsive images that adjust to the size and resolution of the device being used to view them. This can help reduce the amount of data that needs to be transferred, leading to faster load times.

Use a content delivery network (CDN): A CDN is a network of servers that store copies of your static content (such as images) and serve them to users from the server closest to their geographic location. This can help reduce the load on your server and improve access times for your users.

Lazy loading: You can use a lazy loading technique that only loads images when they are needed, such as when the user scrolls to them on the page. This can reduce the number of images that need to be loaded initially, leading to faster load times.

Implement caching: You can configure your web server or application to cache images in the user's browser, so that they don't need to be reloaded every time the user visits your site. This can significantly reduce the load time for returning visitors.

By implementing one or more of these techniques, you can reduce the size of your "static" folder while still providing fast access to your images.
|'''
