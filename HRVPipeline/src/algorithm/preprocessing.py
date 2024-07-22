import scipy.signal as signal
import numpy as np
import xarray as xr
import neurokit2 as nk


def resample_xarray(xarray, new_sr):
    duration = xarray.time.values[-1] - xarray.time.values[0]
    new_length = int(duration * new_sr)

    resampled_data = signal.resample(xarray.values, new_length)
    new_time = np.linspace(xarray.time.values[0], xarray.time.values[-1], new_length)
    #print('resample_xarray :', xarray.coords)
    cords = {**xarray.coords}
    cords.pop('samples', None)
    res = xr.DataArray(resampled_data, dims=xarray.dims, coords={**cords, 'time': new_time})
    #print('0 ++++++++++++++++++++++++++++++++++++++++++ resampled_xarray :', res.coords)
    #print('1 ++++++++++++++++++++++++++++++++++++++++++ resampled_xarray :', np.shape(res.flat_channel),
    #      np.shape(xarray.flat_channel), res.flat_channel[0])
    #print('2 ++++++++++++++++++++++++++++++++++++++++++ resampled_xarray :', np.shape(res.values),
    #      np.shape(xarray.values))
    return res


def bandpass_filter(data, cutoff_freqs, fs):
    nyquist = 0.5 * fs
    low, high = cutoff_freqs[0] / nyquist, cutoff_freqs[1] / nyquist
    #print('Bandpass filter params:', low, high, nyquist, fs)
    b, a = signal.butter(2, [low, high], btype='band')
    return signal.filtfilt(b, a, data)


# Band-pass filter using heartpy
def filter_signal(data, sr):
    # return hp.filter_signal(data, [0.5, 3], sample_rate=sr, order=2, filtertype='bandpass')
    return nk.signal_filter(data, sr, 0.5, 3, order=2)


def preprocess_snirf_data(amp2d, sampling_rate):
    filtered_data_list = []
    channel_name_list = []
    #print('1 -------------channels ', amp2d.values[0], amp2d.flat_channel.values[0])
    for i, fc in enumerate(amp2d.flat_channel.values):
        channel_data = amp2d.sel(flat_channel=fc)
        filtered_data = filter_signal(channel_data.values, sampling_rate)
        # filtered_data = channel_data.values
        channel_data.values = filtered_data
        filtered_data_list.append(filtered_data)
        # print('-------------channel ', i, ': ', fc, channel_data)
        channel_name_list.append(fc)
    # cords = {**amp2d.coords, }
    # amp2d.assign_coords(coords=cords).flat_channel..values = filtered_data_list
    amp2d.values = np.transpose(filtered_data_list)
    #print('2 -------------channels ', amp2d.values[0], amp2d.flat_channel.values[0], filtered_data_list[0])
    ## amp2d.values = filtered_data_list;
    #print('3 ++++++++++++++++++++++++++++++++++++++++++ resampled_xarray :', amp2d.coords)
    #print('4 ++++++++++++++++++++++++++++++++++++++++++ resampled_xarray :', np.shape(amp2d.flat_channel),
    #      amp2d.flat_channel[0])
    #print('5 ++++++++++++++++++++++++++++++++++++++++++ resampled_xarray :', np.shape(amp2d.values))
    return amp2d
# return xarray
