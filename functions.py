def load_json(jsonfile) -> dict:
    import json
    with open(jsonfile, 'r') as json_file:
        return json.load(json_file)

def save_json(jsonfile, dicionario: dict):
    import json
    with open(jsonfile, 'w') as json_file:
        json_file.write(json.dumps(dicionario))