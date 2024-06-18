from typing import List
import numpy as np
# import xarray as xr
# from xarray import DataArray
import pandas as pd

from cedalion.io import read_snirf


# def read_log(path) -> DataArray:
#     with open(path) as in_data:
#         t = in_data.read()
#         x = np.fromstring(t, sep="\n")
#         data = xr.DataArray(x, dims=["green"])
#     return data


def read_ppg(path):
    ppg = pd.read_csv(path, sep=",", index_col=0)[["green", "red", "infra_red"]]

    # return ppg.to_xarray()
    return ppg


def get_snirf_data(path):
    data = read_snirf(path)

    # return ppg.to_xarray()
    return [data[0].aux[x].to_dataframe() for x in data[0].aux]


def read_snirf_ppg(path):
    data = read_snirf(path)

    return data[0].aux['PPG']
