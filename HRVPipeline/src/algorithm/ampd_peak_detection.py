import numpy as np


def ampd(signal):
    # Ensure the signal is a numpy array
    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1:
        raise ValueError("Input signal must be a one-dimensional array")

    # Detrend signal using a linear fit
    time = np.arange(len(signal))
    fit_polynomial = np.polyfit(time, signal, 1)
    fit_signal = np.polyval(fit_polynomial, time)
    dtr_signal = signal - fit_signal

    # Initialize variables
    N = len(dtr_signal)
    L = int(np.ceil(N / 2.0)) - 1
    LSM = np.ones((L, N)) + np.random.rand(L, N)

    # Generate Local Scalogram Matrix (LSM)
    for k in range(1, L + 1):
        for i in range(k + 1, N - k):
            if dtr_signal[i] > dtr_signal[i - k] and dtr_signal[i] > dtr_signal[i + k]:
                LSM[k - 1, i] = 0

    # Find the optimal scale (l) with the minimum G
    G = np.sum(LSM, axis=1)
    l = np.argmin(G) + 1

    # Use only the first 'l' rows of LSM
    LSM = LSM[:l, :]

    # Calculate standard deviation along the columns
    S = np.std(LSM, axis=0)

    # Find peaks where standard deviation is zero
    peaks = np.where(S == 0)[0]

    return peaks


def ampd2(signal):
    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1:
        raise ValueError("Input signal must be a one-dimensional array")

    # Detrend signal using a linear fit
    time = np.arange(len(signal))
    fit_polynomial = np.polyfit(time, signal, 1)
    fit_signal = np.polyval(fit_polynomial, time)
    dtr_signal = signal - fit_signal

    # Initialize variables
    N = len(dtr_signal)
    L = int(np.ceil(N / 2.0)) - 1
    LSM = np.ones((L, N))

    # Generate Local Scalogram Matrix (LSM) using vectorized operations
    for k in range(1, L + 1):
        LSM[k - 1, k:N - k] = (dtr_signal[k:N - k] > dtr_signal[0:N - 2 * k]) & (
                dtr_signal[k:N - k] > dtr_signal[2 * k:N])

    # Find the optimal scale (l) with the minimum G
    G = np.sum(LSM, axis=1)
    l = np.argmin(G) + 1

    # Use only the first 'l' rows of LSM
    LSM = LSM[:l, :]

    # Calculate standard deviation along the columns
    S = np.std(LSM, axis=0)

    # Find peaks where standard deviation is zero
    peaks = np.where(S == 0)[0]

    return peaks
