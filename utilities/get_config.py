import ujson as json

def get_config(filename="config.json", value=""):
    with open(filename, "r", encoding="utf-8") as fp:
        config = json.load(fp)
    if value:
        return config.get(value)
    return config if config else None