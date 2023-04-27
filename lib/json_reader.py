import os
import json


def read(json_config: str) -> dict:
    """
    Read in a json file anc return it as a dictionary.
    :param json_config: The configuration json file to read.
    :return: A dictionary containing the configuration json values.
    """
    json_file: str = f'{os.getcwd()}/{json_config}'

    with open(json_file, 'r') as file:
        data: dict = json.load(file)

    return data


def validate() -> None:
    # todo: validate proper json -> fail if criteria not met.
    pass
