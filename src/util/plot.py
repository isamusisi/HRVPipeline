import matplotlib
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as p


def plot_signal(signals, title='ppg', plot_type='line', with_x=True, x_label='Time', y_label=''):
    # f, axs = p.subplots()
    # for i, ax in enumerate(axs):
    #     signal = signals[i]
    #     ax.plot([i for i in range(len(signal))], signal)
    f, ax = p.subplots()
    x = np.arange(len(signals[0]))  # [i for i in range(len(sig))]
    for i, sig in enumerate(signals):
        if i == 0:
            if plot_type == 'bar':
                if with_x:
                    ax.bar(x, sig)
                else:
                    ax.bar(sig)
            else:
                ax.plot(x, sig)
        else:
            ax.twinx().plot(x, sig)

    p.title(title)
    p.show()


def plot_ppg(ppg, title='ppg'):
    # p.figure()
    ax = p.gca()
    # ppg.plot()
    ppg = (ppg - ppg.min()) / (ppg.max() - ppg.min())
    # normalized_ppg.plot()
    ppg = ppg.reset_index(drop=True)
    ppg.plot(y='green', color='green', ax=ax, title=title)
    # ppg.plot(y='red', color='red', ax=ax)
    # ppg.plot(y='infra_red', color='black', ax=ax)
    ppg.plot(y='peaks', color='blue', ax=ax, label=f"Peaks {ppg['peaks'].to_list().count(1)}/64")
    p.legend(loc='best')
    p.show()
