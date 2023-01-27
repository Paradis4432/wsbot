import requests

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': '<REFER-AUTH-API-TOKEN-IN-INTRODUCTION>',
    'x-ebg-param': '<REFER-PIXELBIN-SIGNATURE-GENERATION>',
    'x-ebg-signature': '<REFER-PIXELBIN-SIGNATURE-GENERATION>',
}

json_data = {
    'url': 'https://cdn.pixelbin.io/v2/old-scene-ccdc01/original/2-Figure2-1-(1)-transformed.webp',
    'filenameOverride': True,
}

response = requests.post('https://api.pixelbin.io/service/platform/assets/v1.0/upload/url', headers=headers, json=json_data)