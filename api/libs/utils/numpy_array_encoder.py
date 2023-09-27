import json

import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    """ NumpyArrayEncoder """

    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)
