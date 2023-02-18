"""
Miscellaneous utility functions
"""
import json
import logging

def load_json(
    json_str: str
) -> dict:
    """
    Loads a JSON string into a dictionary. Will load JSON with a length = 0 as None
    and will also return None if there is an error loading the JSON

    Args:
        json_str (str): String in JSON format

    Returns:
        dict: JSON as a dictionary
    """
    try:
        json_dict = json.loads(json_str)
    except Exception as ex:
        logging.warning(f"Caught exception: {ex}")
        return None

    if len(json_dict) == 0:
        return None

    return json_dict
