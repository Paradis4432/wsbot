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
    imgsSrcs = glob.glob(
        f"static/KO.{negocio}.{t}.*.*.png") + glob.glob(f"static/{negocio}.{t}.*.*.png")

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

# TODO: idea: add tags for each group of images


@app.route("/newImageGroup/<neg>", methods=["POST"])
def newGroup(neg=None):
    logging.debug(f"adding new group for neg: {neg}")

    with open("data.json", "r") as f:
        data = json.load(f)

    # type:
    t = request.form["type"]

    # a = request.form.get("image1KO") DELETE
    # print([request.form.get(f"image{i}KO") for i in range(1, 4)]) DELETE
    # return render_template("nuevoGrupoAgregado.html", neg=neg) DELETE

    # group
    # all groups in json neg type + 1 (len starts at 1)
    group = len(data["negs"][neg]["images"][t])
    logging.debug(f"saving images with neg {neg} type {t} group {group}")

    # images
    images = []
    # TODO remove some tabs with a function taking i as arg maybe
    for i in range(1, 4):
        # TODO fix forced 3 images
        file = request.files.get(f"image{i}")
        if file:
            # if keep original true in view dont add to data.pending .json else add
            # if keep original true in view add "KO" at start of file name
            if request.form.get(f"image{i}KO") == "on":
                filename = f"KO.{neg}.{t}.{group}.{i}.png"
                logging.debug(f"found image id {i} to have KO")
            else:
                filename = f"{neg}.{t}.{group}.{i}.png"

                # if any call left remove bg of filename
                # if anyCallLeft():
                #     logging.debug(f"attempting to remove bg of filename: {filename}")
                #     removeBG(filename)
                # else:
                # logging.debug(f"added {filename} to pending due to no more calls left")
                data["pending"].append(filename)

            file.save(os.path.join("static", filename))
            images.append(filename)
            logging.debug(f"saved image id {i}")

            # TODO pending remove bg image
            # py script takes all images in data.pending and processes them
            # under data.info save details:
            # images uploaded, imaged processed, pending to remove bg

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
button -> start image processing
set stats in main.html:
    pending
    processing
    stopNext
    currentStatus


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


test for static folder
There are several ways you can reduce the size of the "static" folder containing images, while maintaining fast access to them. Here are a few suggestions:

Optimize image files: You can use tools such as ImageOptim or TinyPNG to compress the size of your image files without reducing their quality. This can significantly reduce the file size of your images, while keeping their visual appeal intact.

Use responsive images: Instead of serving large images to all devices, you can use responsive images that adjust to the size and resolution of the device being used to view them. This can help reduce the amount of data that needs to be transferred, leading to faster load times.

Use a content delivery network (CDN): A CDN is a network of servers that store copies of your static content (such as images) and serve them to users from the server closest to their geographic location. This can help reduce the load on your server and improve access times for your users.

Lazy loading: You can use a lazy loading technique that only loads images when they are needed, such as when the user scrolls to them on the page. This can reduce the number of images that need to be loaded initially, leading to faster load times.

Implement caching: You can configure your web server or application to cache images in the user's browser, so that they don't need to be reloaded every time the user visits your site. This can significantly reduce the load time for returning visitors.

By implementing one or more of these techniques, you can reduce the size of your "static" folder while still providing fast access to your images.
|'''
