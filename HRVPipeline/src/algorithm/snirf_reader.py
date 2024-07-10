import cedalion.io


def load_snirf_data(path):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].data[0]  # extract snirf
    # elements[0].aux['ExGa1'] ECG
    # elements[0].aux['PPG'] PPG
    amp3d = amp3d.sel(time=amp3d.time < 20)
    amp2d = amp3d.stack(flat_channel=["channel", "wavelength"])
    return amp2d, amp2d.cd.sampling_rate
