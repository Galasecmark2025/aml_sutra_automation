import os, ujson as json

def get_config(read_path, filename="config.json", value="", logger=None):
    try:
        file_path = os.path.join(read_path, filename)
        with open(file_path, "r", encoding="utf-8") as fp:
            config = json.load(fp)
        if value:
            return config.get(value)
        return config if config else None
    except Exception as e:
        logger.error(f"Error occurred while reading configuration: {filename}, error: {e}")
        return None