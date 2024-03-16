from typing import List
import numpy as np
import xarray as xr
from xarray import DataArray
import pandas as pd


def read_log(path) -> DataArray:
    with open(path) as in_data:
        t = in_data.read()
        x = np.fromstring(t, sep="\n")
        data = xr.DataArray(x, dims=["green"])
    return data


def read_ppg(path) -> DataArray:
    ppg = pd.read_csv(path, sep=",", index_col=0)[["green", "red", "infra_red"]]

    # return ppg.to_xarray()
    return ppg
