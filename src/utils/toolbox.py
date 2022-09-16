import os
import json
import logging

logger = logging.getLogger(__name__)


def get_path(current_file: str, relative_path: str = "") -> str:
    '''
    current_file must be __file__
    '''
    return os.path.join(os.path.dirname(os.path.realpath(current_file)), relative_path)


def load_json_file(json_file_path):
    """
    Loads a JSON file content into a dict object.
    :param json_file_path: path to the JSON file
    :return: The dict object with the JSON content
    """

    with open(json_file_path, "r") as json_file:
        content = json.load(json_file)

    return content
