import os, sys, ujson as json

def get_actions_from_command(logger):
    """
    Usage:
    python app.py actions.json
    """
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]

            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)

                    return data.get("actions", [])

                except Exception as e:
                    logger.error(f"Failed to read action file: {e}")

            else:
                logger.error(f"File not found: {file_path}")

        return []
    except Exception as e:
        logger.error(f"Error occurred while reading command line input: {e}")