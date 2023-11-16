import json
import os


def load_schema(name):
    json_schemas_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_schemas")
    path = os.path.join(json_schemas_dir, name)
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
