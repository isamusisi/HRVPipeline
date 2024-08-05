import cedalion.io

import cedalion
import cedalion.nirs
import cedalion.sigproc.quality as quality
import cedalion.xrutils as xrutils
import cedalion.datasets as datasets
import xarray as xr
import matplotlib.pyplot as p
from functools import reduce
import numpy as np

from cedalion import Quantity, units


def load_snirf_data(path,length):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].data[0]  # extract snirf
    # elements[0].aux['ExGa1'] ECG
    # elements[0].aux['PPG'] PPG

    snr_thresh = 14  # the SNR (std/mean) of a channel.
    # sd_threshs = [1,
    #               4.5] * units.cm  # defines the lower and upper bounds for the source-detector separation that we would like to keep
    # amp_threshs = [0.1, 3] * units.volt  # define whether a channel's amplitude is within a certain range

    # then we calculate the masks for each metric: SNR, SD distance and mean amplitude
    _, snr_mask = quality.snr(amp3d, snr_thresh)
    # _, sd_mask = quality.sd_dist(raw, data.geo3d, sd_threshs)
    # _, amp_mask = quality.mean_amp(amp3d, amp_threshs)

    # put all masks in a list
    masks = [snr_mask]

    # prune channels using the masks and the operator "all", which will keep only channels that pass all three metrics
    # amp3d, drop_list = quality.prune_ch(amp3d, masks, "all")

    # print('++++++++++++++++++++++++++++++++++++++++drop list: ', drop_list)

    amp3d = amp3d.sel(time=amp3d.time < length)
    amp2d = amp3d.stack(flat_channel=["channel", "wavelength"])
    return amp2d, amp2d.cd.sampling_rate

# [[138759.7649241254], [1606718.0151836334]] orig
# [[138759.7649241254], [1606718.0151836334]] snr thresh 8
# [[142205.5620363502], [2500636.611334468]] snr thresh 9  pruned: ['S1D2' 'S2D1' 'S3D3' 'S5D4']
# [[147093.0328464521], [2947252.811243928]]  snr thresh 10 pruned: ['S1D2' 'S2D1' 'S3D3' 'S5D4' 'S6D6' 'S8D7']
# [[143217.7327848616], [1605585.9266221395]]  snr thresh 11 pruned: ['S1D2' 'S2D1' 'S3D3' 'S4D2' 'S5D4' 'S6D6' 'S8D7']
# [[143226.0355348466], [3750354.3445572513]] snr thresh 12 pruned: ['S1D2' 'S2D1' 'S3D3' 'S4D2' 'S5D4' 'S5D6' 'S6D6' 'S8D7']
# [[144310.3982704362], [5912620.632428929]] snr thresh 13 pruned: ['S1D2' 'S2D1' 'S3D3' 'S4D2' 'S5D3' 'S5D4' 'S5D6' 'S6D5' 'S6D6' 'S8D7']
# [[146617.5650794517], [2646623.7008850696]] snr thresh 14 pruned: ['S1D1' 'S1D2' 'S2D1' 'S3D2' 'S3D3' 'S3D4' 'S4D2' 'S4D4' 'S5D3' 'S5D4' 'S5D6' 'S6D5' 'S6D6' 'S8D6' 'S8D7']
# [[146617.5650794517], [2646623.7008850696]] snr thresh 16 pruned: ['S1D1' 'S1D2' 'S2D1' 'S3D2' 'S3D3' 'S3D4' 'S4D2' 'S4D4' 'S5D3' 'S5D4' 'S5D6' 'S6D5' 'S6D6' 'S8D6' 'S8D7']
