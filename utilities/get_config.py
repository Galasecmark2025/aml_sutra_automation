import ujson as json

def get_config(filename="config.json", value=""):
    try:
        with open(filename, "r", encoding="utf-8") as fp:
            config = json.load(fp)
        if value:
            return config.get(value)
        return config if config else None
    except Exception as e:
        print(f"Error occurred while reading configuration: {filename}, error: {e}")