"""
eawrangle offers convenient functions for data manipulations.
"""

import numpy as np
import pandas as pd


def bucket_continuous(x, inclusive=True, buckets=["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-64", "65+"]):
    """Place a value in a predefined bucket. Example: creating age buckets. This function assumes that the last bucket does not have a right boundary and that the buckets are increasing in order.

    Args:
        x (int, float): Numeric value.
        inclusive (bool, optional): If true, bucket ranges include the right hand value. (Defaults to True)
        buckets (list, optional): A list of the defined buckets. Defaults to ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-64", "65+"].

    Returns:
        str: String of the assigned bucket.
    """
    
    boundaries = [(int(a.split("-")[0]), int(a.split("-")[1])) for i, a in enumerate(buckets[:-1])]
    boundaries.append((int(buckets[-1].strip("+")), np.inf))

    for i, b in enumerate(boundaries):
        if x >= b[0]:
            if inclusive:
                if x <= b[1]: return buckets[i]
            else:
                if x < b[1]: return buckets[i]
        else:
            pass
