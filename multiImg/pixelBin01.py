import asyncio

from pixelbin import PixelbinClient, PixelbinConfig
from pixelbin.utils.url import url_to_obj

pxUrl = "https://cdn.pixelbin.io/v2/holy-haze-14b003/erase.bg()/wsimg.jpeg"
obj = url_to_obj(pxUrl)
print(obj)



def a():    # create client with your API_TOKEN
    config = PixelbinConfig({
        "domain": "https://api.pixelbin.io",
        "apiSecret": "41b02c7b-25c9-4f0f-882f-9690908f15f9",
    })

    # Create a pixelbin instance
    pixelbin:PixelbinClient = PixelbinClient(config=config)

    # Sync method call
    try:
        result = pixelbin.assets.listFiles()
        print(result)
    except Exception as e:
        print(e)
