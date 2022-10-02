import json


def open_file_json(data_file):
 with open(data_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def write_file_json(data_file, data_json):
    with open(data_file, 'w', encoding='utf-8') as file:
        file.write(data_json)