import pint

import HRVPipeline.src.util.plot as p
from src.cedalion.io import read_snirf
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import HRVPipeline.src.hrv_methods as hm
import neurokit2 as nk

if __name__ == "__main__":

    path = r"2024-04-09_007.snirf"
    ir_data = read_snirf(path)
    # print(f"---------------------------------{ir_data[0].aux['PPG']}")
    # p.plot_signal([ir_data[0].aux['ExGa1'].time])
    ira = ir_data[0].aux
    irs = ir_data[0].data
    irmd = ir_data[0].meta_data
    irml = ir_data[0].measurement_lists
    # print(f'0++++++++++++++++++++++++++++++{irml}')
    # plt.show()
    # ir = ir_data.nirs[0].data[0].dataTimeSeries
    # num_series = 40
    #
    # # Create traces for each time series
    traces = []
    for d in ira:

        data = ira[d]
        # if data.name == 'ExGa1':
        # sr = hm.get_sampling_rate(data.time.values)
        sr = 10
        print(f'1+++++++++++++++++++++++++{sr}+++{data.name}')
        print(f'2+++++++++++++++++++++++++++{data.time}')
        filt = data.to_dataframe().apply(lambda x: nk.signal_filter(x, sampling_rate=sr, lowcut=0.5, highcut=3,
                                                                         order=2))
        print(f'3+++++++++++++++++++++++++++{filt}')
        print(f'4+++++++++++++++++++++++++++{data}')
        data_array = data
        # data_array = filt
        trace = go.Scatter(x=list(range(len(data_array))), y=data_array, mode='lines', name=f'Series {data.name}')
        traces.append(trace)
    # #
    # Create layout
    # layout = go.Layout(
    #     title='40 Time Series Data',
    #     xaxis=dict(title='Time'),
    #     yaxis=dict(title='Value')
    # )
    #
    # # Create figure
    # fig = go.Figure(data=traces, layout=layout)
    # fig.show()

    # element = ir_data[0]  # there is only one NirsElement in this snirf file...
    # amp = element.data[0]  # ... which holds amplitude data
    #
    # # restrict to first 60 seconds and fill in missing units
    # amp = amp.sel(time=amp.time < 60)
    # amp = amp.pint.dequantify().pint.quantify("V")
    # geo3d = element.geo3d
    #
    # print(f"{geo3d}")
