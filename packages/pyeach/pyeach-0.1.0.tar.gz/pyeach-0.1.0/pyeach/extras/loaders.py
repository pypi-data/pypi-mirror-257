"""
loaders provides supplemental functions for reading and loading various data file types.
"""


import pandas as pd
import numpy as np
from shapefile import Reader


def read_sql(fpath):
    """Opens the query from fpath and returns the contents as a string.

    Args:
        fpath (str): Path to desired SQL file.

    Returns:
        str: Query in string form.
    """
    with open(fpath, "r") as f:
        query = f.read()
        f.close()
    return query


def read_txt(fpath, to_df=True, enc="utf-8-sig"):
    """Opens the contents from fpath and returns the contents as a dataframe or string.

    Args:
        path (str): Path to desired file.
        to_df (bool, optional): If true, return the contents of the file in a pandas dataframe. Otherwise, return the contents as a string. Defaults to True.
        enc (str, optional): The type of encoding that the file is encoded in. Defaults to "utf-8-sig".

    Returns:
        {pd.DataFrame, str}: The contents of the file in a pandas dataframe or a string.
    """
    with open(fpath, "r", encoding=enc) as f:
        data = f.readlines()
        f.close()

    if to_df:
        col_names = data.pop(0).strip().split(",")
        data = [row.strip().split(",") for row in data]
        data = [d for d in data if len(d) == len(col_names)]
        data = pd.DataFrame(data, columns=col_names)
    else:
        pass
    
    return data


def fetch_shapefile(fpath, geoms=None, inv=False):
    """Load the shapefile from fpath and filter the contents for geometries that are in geoms.

    Args:
        fpath (str): File path to desired shapefile.
        geoms (list, optional): List of geometry IDs to filter for. (Defaults to None)
        inv (bool, optional): If true, inverse the filter to remove geometry IDs in geoms. (Defaults to False)

    Returns:
        dict: Filtered contents of shapefile.
    """
    geodata = Reader(fpath).__geo_interface__

    if geoms:
        idx = list(reversed(np.arange(0, len(geodata["features"]), 1)))
        for i in idx:
            geoid = geodata["features"][i]["properties"]["GEOID"]
            if geoid in geoms:
                if inv: del geodata["features"][i]
            else:
                if not inv: del geodata["features"][i]
    
    return geodata