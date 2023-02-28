""" File Helper """

import os


def mkdir(path: str) -> None:
    """ make dir recursive """
    os.makedirs(path, exist_ok=True)
