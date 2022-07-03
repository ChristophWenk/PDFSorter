import json

def read_json():
    file = open('resources/Helsana-Leistungsabrechnung-20220703', 'r')
    data = json.load(file)
    file.close()
    return data
