"""
eadb provides functions for querying EDW databases and various APIs.
"""

import pandas as pd
import numpy as np
import pyodbc
from time import time
from math import floor, ceil
from sodapy import Socrata
from pyeach.extras.loaders import read_sql


def query_edw(server, file=None, query=None, dtypes={}, verbose=True):
    """Query the EDW and return the results in a pandas DataFrame. Either file or query args must be provided.

    Args:
        server (str): EDW server.
        file (str, optional): File with SQL query. Defaults to None.
        query (str, optional): String with SQL query. Defaults to None.
        dtypes (dict, optional): Data types to convert results. Defaults to {}.
        verbose (bool, optional): Optional to print query execution time. Defaults to True.

    Returns:
        pd.DataFrame: Results from EDW query.
    """

    if file:
        query = read_sql(file)
    else:
        pass

    # establish connection
    driver = "ODBC Driver 17 for SQL Server"
    connection_string = "DRIVER={{{}}};SERVER={};Trusted_Connection=yes".format(driver, server)
    sv_connection = pyodbc.connect(connection_string)
    cursor = sv_connection.cursor()
    
    # execute query
    start = time()
    result = cursor.execute(query)
    end = time()
    duration = end - start
    duration_min = floor((end - start) / 60)
    duration_remainder = ceil(duration - (duration_min * 60))
    if verbose:
        print(f"Query successfully executed in {duration_min}:{duration_remainder}")
    
    # extract data into data frame
    data = result.fetchall()
    cols = [c[0] for c in result.description]
    df = pd.DataFrame(np.array(data), columns=cols, dtype="object")
    
    # close connection
    sv_connection.close()

    # assign data types
    for nm, typ in dtypes.items():
        if typ == "date":
            df[nm] = pd.to_datetime(df[nm], format="%Y-%m-%d")
        elif typ == "datetime":
            df[nm] = pd.to_datetime(df[nm])
        else:
            df[nm] = df[nm].astype(typ)

    return df


def query_socrata(source, endpoint, query, token=None, usrnm=None, psswd=None):
    """Query an API using Socrata and return the results in a pandas DataFrame.

    Args:
        source (str): Web source of data (ex. data.cdc.gov).
        endpoint (str): API endpoint (ex. cwsq-ngmh).
        query (str): API query.
        token (str, optional): Unique API token if credentials are required. (Defaults to None)
        usrnm (str, optional): Unique username if credentials are required. (Defaults to None)
        psswd (str, optional): Unique password if credentials are required. (Defaults to None)

    Returns:
        _type_: _description_
    """

    creds = [token, usrnm, psswd]
    creds_provided = sum(x is not None for x in creds)

    if creds_provided > 0:
        assert creds_provided == 3, "Must provide API token, username, and password."
        # attempt query if token, username, and password are all provided
        client = Socrata(source, token, username=usrnm, password=psswd)
    else:
        client = Socrata(source, None)

    results = client.get(endpoint, query=query)

    df = pd.DataFrame.from_records(results)

    return df