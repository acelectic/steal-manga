""" File Helper """

import os
from typing import List


def mkdir(path: str) -> None:
    """ make dir recursive """
    os.makedirs(path, exist_ok=True)


def get_env(key: str, required: bool = True) -> str | None:
    """
        get env and validate
    """
    value = os.getenv(key)
    if required:
        assert value is not None
    return value


def get_env_str_array(key: str, required: bool = True) -> List[str]:
    """
        get env and validate
    """
    value: str | None = os.getenv(key)
    if required:
        assert value is not None

    if value is not None:
        return [x for x in value.split(',') if x is not None and x != '']
    else:
        return []
