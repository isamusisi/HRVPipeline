from snirf import Snirf

def snirf_path_to_meta_path(path:str):
    assert(path.endswith(".snirf"))
    path_meta = path[-6] + "_description.json"
    return path_meta

def read_snirf(path):
    assert (path.endswith(".snirf"))
    ir_data = Snirf(path, 'r+')
    ir_data_copy=  ir_data.copy()
    ir = ir_data.nirs[0].data[0].dataTimeSeries
    #return ir_data
    ir_data.close()

    return ir_data_copy
    #ir = ir_data_copy[0].dataTimeSeries
    #return ir

import numpy as np
import plotly.graph_objects as go



if __name__ == "__main__":
    path = r"..\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"
    ir_data = read_snirf(path)
    ir = ir_data.nirs[0].data[0].dataTimeSeries
    num_series = 40
    data_array = ir

    # Create traces for each time series
    traces = []
    for i in range(num_series):
        trace = go.Scatter(x=list(range(len(data_array[:,0]))), y=data_array[:,i], mode='lines', name=f'Series {i + 1}')
        traces.append(trace)

    # Create layout
    layout = go.Layout(
        title='40 Time Series Data',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Value')
    )

    # Create figure
    fig = go.Figure(data=traces, layout=layout)
    fig.show()
