""" module mam mirror image json meta """

import json
from pprint import pprint
from typing import Any, List, Tuple

import numpy as np

from ..utils.numpy_array_encoder import NumpyArrayEncoder


class ImageJsonShuffle:
    """ interface of man mirror image json """

    def __init__(self, width: int, height: int, all_row: int, all_col: int, shuffles: List[int], raw):
        try:
            self.width = width
            self.height = height
            self.all_row = all_row
            self.all_col = all_col
            self.shuffles = np.reshape(shuffles, (all_row, all_col))
            self.sub_height = int(round(height / all_row, 0))
            self.sub_width = int(round(width / all_col, 0))
            self.raw: Any = raw

            self.is_shuffles_size_too_many: bool = len(shuffles) > 10000
            self.is_shuffles_radio_size_too_many: bool = all_row > height / 10 or all_col > width / 10
            self.is_shuffles_not_match: bool = all_row * all_col != len(shuffles)

            self.must_debug: bool = self.is_shuffles_size_too_many or self.is_shuffles_not_match
        except Exception as error:
            print('ImageJsonShuffle init error')
            print(error)
            pprint(
                {
                    "width": width,
                    "height": height,
                    "all_row": all_row,
                    "all_col": all_col,
                    "shuffles": shuffles
                }
            )

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
        return json.dumps(
            {
                "width": self.width,
                "height": self.height,
                "all_row": self.all_row,
                "all_col": self.all_col,
                "shuffles": self.shuffles,
                "sub_height": self.sub_height,
                "sub_width": self.sub_width,
            },
            indent=4,
            cls=NumpyArrayEncoder)
