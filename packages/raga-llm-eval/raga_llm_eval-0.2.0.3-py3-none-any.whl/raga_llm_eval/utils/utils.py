"""
Helper functions
"""

import json

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types"""

    def default(self, obj):
        """
        A function to handle default JSON encoding for special object types.

        :param obj: The object to be encoded into JSON.
        :return: The JSON representation of the object.
        """
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
