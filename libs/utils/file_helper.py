""" File Helper """

import os


def mkdir(path: str) -> None:
    """ make dir recursive """
    os.makedirs(path, exist_ok=True)


def get_env(key: str, required: bool = False) -> str | None:
    """
        get env and validate
    """
    value = os.getenv(key)
    if required:
        assert value is not None
    return value
