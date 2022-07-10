import json
import io


def read_json(config_file):
    config = io.open(config_file, 'r', encoding="utf-8")
    data = json.load(config)
    config.close()
    return data
