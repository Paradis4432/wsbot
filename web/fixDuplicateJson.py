import os
import hashlib

import os
import hashlib

#from .tools import *
from tools import *
data = loadData()

dups = []
def check_duplicate_images(image_list):
    images = []
    for image_file in image_list:
        with open(f"./static/{image_file}", "rb") as f:
            image_content = f.read()
            image_hash = hashlib.md5(image_content).hexdigest()
            if image_hash in images:
                print(f"Found a duplicate image: {image_file}")
                return image_file

            else:
                images.append(image_hash)



def main():
    neg = "marian"
    types = data["negs"][neg]["images"].keys()
    print(types)

    for _type in types:
        for group in data["negs"][neg]["images"][_type].keys():
            image_list = data["negs"][neg]["images"][_type][group]["images"]
            dup = check_duplicate_images(image_list)
            if dup == "None": continue
            try:
                os.remove(f"./static/{dup}")
                if dup in data["negs"][neg]["images"][_type][group]["images"]: data["negs"][neg]["images"][_type][group]["images"].remove(dup)
                if dup in data["pendingAddArr"]: data["pendingAddArr"].remove(dup)
                if dup in data["pendingRmBg"]: data["pendingRmBg"].remove(dup)
                if dup in data["processingAddArr"]: data["processingAddArr"].remove(dup)
                if dup in data["processingRmBg"]: data["processingRmBg"].remove(dup)
                if dup in data["processedRmBg"]: data["processedRmBg"].remove(dup)
                if dup in data["processedAddArr"]: data["processedAddArr"].remove(dup)

                print(f"Removed duplicate image: {dup}")
                saveData(data)
            except Exception as e:
                print("error removing duplicate image" )
                print(e)

        
main()
main()