import json
import os
def add_one(number):
    return number + 1

def leer_json():
    path = os.path.join(os.path.dirname(__file__), 'data/prueba.json')
    with open(path) as f:
        data = json.load(f)
    print(data)
    return data