import json

def read_json():
    file = open('resources/config_files/Helsana-Leistungsabrechnung.json', 'r')
    data = json.load(file)
    file.close()
    return data
