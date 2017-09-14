#!usr/bin/py

import json

with open('image_data.json') as json_data:
    data = json.load(json_data)
    print(data)