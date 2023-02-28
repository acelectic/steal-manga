""" module mam mirror image json meta """

import json
import numpy as np
from typing import List, Tuple


class Coord:
    """ coord interface """

    def __init__(self, key: str, col: int, row: int, new_row: int, new_col: int, sort: int, top: int, left: int, bottom: int, right: int):
        self.new_row = new_row
        self.new_col = new_col
        self.key = key
        self.col = col
        self.row = row
        self.sort = sort
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def __str__(self) -> str:
        return json.dumps({
            "key": self.key,
            "col": self.col,
            "row": self.row,
            "sort": self.sort,
            "top": self.top,
            "left": self.left,
            "bottom": self.bottom,
            "right": self.right,
        }, indent=4)


class ImageJsonShuffle:
    """ interface of man mirror image json """

    def __init__(self, width: int, height: int, all_row: int, all_col: int, shuffles: List[int]):
        self.width = width
        self.height = height
        self.all_row = all_row
        self.all_col = all_col
        self.shuffles = np.reshape(shuffles, (all_row, all_col))
        self.sub_height = int(round(height / all_row, 0))
        self.sub_width = int(round(width / all_col, 0))

    def get_coord_from_index(self, sort_index: int) -> Tuple[int, int]:
        """ for get new coordinates from index """
        row = 0
        col = 0
        for row_i, row_item in enumerate(self.shuffles):
            for col_i, col_item in enumerate(row_item):
                if col_item == sort_index:
                    row = row_i + 1
                    col = col_i + 1
        return row, col

    def __str__(self) -> str:
        return json.dumps({
            "width": self.width,
            "height": self.height,
            "all_row": self.all_row,
            "all_col": self.all_col,
            "shuffles": self.shuffles,
            "sub_height": self.sub_height,
            "sub_width": self.sub_width,
        }, indent=4)
