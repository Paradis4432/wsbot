from .imageEditManager import *
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file


from PIL import Image
import logging
import json
import os
import glob
import asyncio

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="basic.log")

# TODO: fix max size done
# TODO: rezize image to 1200x800 pixels on upload done
# TODO: fix autochange of key done
# TODO: fix white background not adding done
# TODO: excel loading done
# TODO: fix img size in group edit done
# TODO: img edit done
# TODO: add another value for group done
# TODO: img remove done
# TODO: del group done
# TODO: make excel loader None proof done
# TODO: add image in certain pos done
# TODO: cambiar cargado de imagenes boton -> grupo info etc done

# TODO: del value for group

# TODO: img replace grande
# TODO: excel to json load grande 

# TODO: arrows for images no
# TODO: change upload to button no molesta esperar

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

    # firsts = [data["negs"][neg]["images"][t][x]["images"][0] for x in data["negs"][neg]["images"][t].keys()]

    logging.debug(f"rendering images: {imgsSrcs}")

    return render_template("tempImagesNegocio.html", neg=neg, t=t, srcs=imgsSrcs)


@app.route("/downloadExcel")
def download_excel():
    logging.debug("downloading excel")
    create_excel_from_json()
    return send_file("data.xlsx", as_attachment=True, download_name="data.xlsx")


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


def getImgName(request, data, i):
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

    return filename, data


def changeImageSize(file, filename):
    try:
        image = Image.open(file)
        image.thumbnail((1200, 800))
        image.save(os.path.join("static", filename))
        logging.debug(f"changed image {filename} size")
    except Exception as e:
        logging.error(f"error changing {filename} size: {e}")


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
        filename, data = getImgName(request, data, i)

        # file.save(os.path.join("static", filename))
        changeImageSize(file, filename)

        images.append(filename)
        logging.debug(f"saved image id {i}")

    # file saved, add name in json
    data["negs"][neg]["images"].setdefault(t, {})[group] = {
        "images": images,
        "alto": request.form.get("alto") or "not found",
        "largo": request.form.get("largo") or "not found",
        "ancho": request.form.get("ancho") or "not found",
        "costo": request.form.get("costo") or "not found",
        "venta_menor": request.form.get("venta_menor") or "not found",
        "venta_mayor": request.form.get("venta_mayor") or "not found",
        "stock": request.form.get("stock") or "not found",
        "descripcion": request.form.get("descripcion") or "not found",
        "uniqueID": uniqueID
    }

    logging.debug(f"saved image name in json as {neg}.{t}.{group}.{i}")

    saveData(data)

    # TODO save data in excel send status to front process images once saved
    return render_template("nuevoGrupoAgregado.html", neg=neg)


@app.route("/processPending")
async def processImages():
    logging.debug("starting processing images")
    await startProcessing()
    return "se termino de procesar las imagenes"


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

@app.route("/groupInfo/<neg>/<t>/<group>")
def showGroupInfo(neg=None, t=None, group=None):
    data = loadData()
    keys = list(data["negs"][neg]["images"][t].keys())
    print(keys)
    index = keys.index(group)
    prev_key = keys[index-1] if index > 0 else None
    next_key = keys[index+1] if index < len(keys)-1 else None
    
    print(group, prev_key, next_key)
    try:
        data = data["negs"][neg]["images"][t][group]
    except KeyError:
        logging.debug(f"no se encontro el grupo {neg}.{t}.{group}")
        return f"no se encontro el grupo <a href='/images/{neg}/{t}'>volver</a>"
    
    
    return render_template("groupInfo.html", srcs=data, neg=neg, t=t, group=group, prevG=prev_key, nextG=next_key)


@app.route("/updateValues", methods=["POST"])
def updateValues(neg=None, t=None, group=None):
    data = loadData()
    newData = request.get_json()
    neg = newData["neg"]
    t = newData["t"]
    group = newData["group"]

    for i in newData:
        if i not in ["neg", "group", "t"]:
            # data["negs"][]
            print(i)
            try:
                logging.debug(
                    f"actualizando valor {data['negs'][neg]['images'][t][group][i]} a {newData[i]}")
                data["negs"][neg]["images"][t][group][i] = newData[i]
            except Exception as e:
                return {"info": "error actualizando grupo"}

    saveData(data)

    # return {"data": request.get_json()}
    return {"info": "actualizado"}


@app.route("/addValue", methods=["POST"])
def addValue():
    newData = request.get_json()
    neg = newData["neg"]
    t = newData["t"]
    group = newData["group"]
    key = newData["key"]
    value = newData["value"]

    logging.debug(neg)
    logging.debug(t)
    logging.debug(group)
    logging.debug(key)
    logging.debug(value)

    data = loadData()
    data["negs"][neg]["images"][t][group][key] = value
    logging.debug(
        f"agregando {value} a {data['negs'][neg]['images'][t][group][key]}")
    saveData(data)

    return {"info": "se agrego nuevo key value"}


@app.route("/delImg", methods=["POST"])
def delImg():
    try:
        newData = request.get_json()
        neg = newData["neg"]
        t = newData["t"]
        group = newData["group"]
        imgName = newData["imgName"]

        logging.debug(f"deleting img {neg} {t} {group} {imgName}")

        os.remove(f"./static/{imgName}")

        data = loadData()
        data["negs"][neg]["images"][t][group]["images"].remove(imgName)
        for key in ["pendingAddArr", "pendingRmBg", "processingAddArr", "processingRmBg", "processedRmBg", "processedAddArr"]:
            if imgName in data[key]:
                data[key].remove(imgName)

        saveData(data)
        return {"info": "eliminado correctamente"}

    except Exception as e:
        logging.error(f"error deleting {imgName}: {e}")
        return {"error": str(e)}


@app.route("/saveImg", methods=["POST"])
def saveImg():
    neg = request.form["neg"]
    t = request.form["t"]
    group = request.form["group"]
    KO = request.form["KO"]
    ARR = request.form["ARR"]
    posSel = request.form['posSel']

    data = loadData()

    file = request.files["image"]

    logging.debug(
        f"save img called for neg {neg} t {t} group {group} KO {KO} ARR {ARR}")

    if not file:
        logging.debug(f"got no image")
        return {"info": "es necesario subir una imagen"}

    filename = ""

    try:
        i = 1
        keepAdding = True
        imgNames = data["negs"][neg]["images"][t][group]["images"]
        while keepAdding:
            imgExists = False
            for imgName in imgNames:
                if imgName.endswith(f"{i}.png"):
                    imgExists = True
                    i += 1
                    break
            if not imgExists:
                break

        if KO == "on":
            filename += "KO."
        if ARR == "on":
            filename += "ARR."
        filename += f"{neg}.{t}.{group}.{i}.png"

        if KO == "on":
            logging.debug(f"found image id {i} to have KO")
        else:
            data["pendingRmBg"].append(filename)
            logging.debug(f"added {filename} to pendingRmBg")
        if ARR == "on":
            logging.debug(f"adding image {i} to pending arrows")
            data["pendingAddArr"].append(filename)
        else:
            logging.debug(f"{filename} found to not have ARR")
    except Exception as e:
        logging.debug(f"error processing {filename} {e}")
        return {"info": "error procesando imagen"}

    try:
        changeImageSize(file, filename)
    except Exception as e:
        logging.debug(f"error processing {filename} {e}")
        return {"info": "error procesando cambiado de tamanio de imagen"}

    #data["negs"][neg]["images"][t][group]["images"].append(filename)
    # instead of appending check if posSel is not "last" and insert at that position
    if posSel == "last":
        data["negs"][neg]["images"][t][group]["images"].append(filename)
    else:
        data["negs"][neg]["images"][t][group]["images"].insert(int(posSel), filename)

    logging.debug(f"saved image name in json as {neg}.{t}.{group}.{i}")

    saveData(data)
    return {"info": "imagen guardada"}


@app.route("/delGroup", methods=["POST"])
def delGroup():
    newData = request.get_json()
    neg = newData["neg"]
    t = newData["t"]
    group = newData["group"]
    logging.debug(f"deleting group {group} for negocio {neg} in type {t}")

    data = loadData()
    try:
        del data["negs"][neg]["images"][t][group]
        saveData(data)
    except Exception as e:
        logging.error("error deleting group: " + group)
        return {"info": "error eliminando grupo"}

    logging.debug("group deleted")

    return {"info": "grupo eliminado"}


@app.route("/replaceImg", methods=["POST"])
def replaceImg():
    ...


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
