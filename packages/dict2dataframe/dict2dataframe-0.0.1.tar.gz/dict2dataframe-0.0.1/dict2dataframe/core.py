#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
Core operations.
"""

from typing import Union
import pandas as pd

from dict2dataframe.handlers import JSON


def dict2dataframe(data: Union[dict, list]) -> pd.DataFrame:
    """
    Convert JSON data into a Pandas DataFrame.

    Parameters
    ----------
    data : dict or list of dict
        The JSON data to be converted. If a single dictionary is provided,
        it will be converted to a DataFrame. If a list of dictionaries is
        provided, each dictionary will be treated as a row in the DataFrame.

    Returns
    -------
    pandas.DataFrame
        A DataFrame representation of the JSON data.

    Notes
    -----
    This function assumes that the JSON data is either a single dictionary
    or a list of dictionaries. It uses the `JSON` class with `dump_objects`
    set to `False` to convert the JSON data into a DataFrame.

    Examples
    --------
    >>> data = {"values": [{"a": 1, "b": {"x": 10, "y": 20 }, "c": 2, "d": [{"z": 30 } ] }, {"a": 5, "b": {"x": 15, "y": 25 }, "c": 6, "d": [{"z": 35 } ] }, {"a": 9, "b": {"x": 20, "y": 30 }, "c": 10, "d": [{"z": 40 } ] } ] }
    >>> df = JSON(dict_list=data['values'], dump_objects=False).to_dataframe()
    >>> print(df)
       a   c  b_x  b_y  d_z
    0  1   2   10   20   30
    1  5   6   15   25   35
    2  9  10   20   30   40
    """
    dict_list = data if isinstance(data, list) else [data]

    df = JSON(dict_list=dict_list, dump_objects=False).to_dataframe()

    return df
