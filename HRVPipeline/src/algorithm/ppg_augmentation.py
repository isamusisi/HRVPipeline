import numpy as np


import xarray as xr

def add_noise(ppg_signals, snr_db):
    """
    Adds Gaussian noise to PPG signals to achieve a target SNR.

    Parameters:
    ppg_signals (xr.DataArray): 2D DataArray with dimensions (channels, samples)
    snr_db (float): Target Signal-to-Noise Ratio in dB

    Returns:
    xr.DataArray: PPG signals with added noise
    """
    # Convert DataArray to NumPy array for calculations
    ppg_array = ppg_signals.values

    # Calculate signal power
    signal_power = np.mean(ppg_array ** 2, axis=1, keepdims=True)

    # Convert SNR from dB to linear scale
    snr_linear = 10 ** (snr_db / 10)

    # Calculate noise power
    noise_power = signal_power / snr_linear

    # Generate Gaussian noise
    noise = np.sqrt(noise_power) * np.random.normal(size=ppg_array.shape)

    # Add noise to the signals
    noisy_array = ppg_array + noise

    # Create a new DataArray for the noisy signals
    noisy_signals = xr.DataArray(noisy_array, dims=ppg_signals.dims, coords=ppg_signals.coords)

    return noisy_signals

def add_artefacts(ppg_signals, artifact_probability=0.01, artifact_magnitude=0.05):
    """
    Adds motion artifacts to PPG signals.

    Parameters:
    ppg_signals (xr.DataArray): 2D DataArray with dimensions (channels, samples)
    artifact_probability (float): Probability of an artifact occurring at any sample point
    artifact_magnitude (float): Magnitude of the artifacts to be added

    Returns:
    xr.DataArray: PPG signals with added motion artifacts
    """
    # Convert DataArray to NumPy array for calculations
    ppg_array = ppg_signals.values

    # Copy the signals to avoid modifying the original data
    augmented_array = np.copy(ppg_array)

    # Number of channels and samples
    num_channels, num_samples = ppg_array.shape

    # Add artifacts to each channel
    for channel in range(num_channels):
        for i in range(num_samples):
            if np.random.rand() < artifact_probability:
                # Randomly choose between a spike or sinusoidal artifact
                if np.random.rand() < 0.5:
                    # Add a spike
                    augmented_array[channel, i] += artifact_magnitude * (np.random.rand() - 0.5)
                else:
                    # Add a sinusoidal artifact
                    frequency = np.random.uniform(0.1, 1.0)  # Random frequency between 0.1 and 1.0 Hz
                    duration = np.random.randint(10, 50)  # Random duration between 10 and 50 samples
                    t = np.arange(duration)
                    sinusoid = artifact_magnitude * np.sin(2 * np.pi * frequency * t / num_samples)
                    end_idx = min(i + duration, num_samples)
                    augmented_array[channel, i:end_idx] += sinusoid[:end_idx - i]

    # Create a new DataArray for the augmented signals
    augmented_signals = xr.DataArray(augmented_array, dims=ppg_signals.dims, coords=ppg_signals.coords)

    return augmented_signals


def add_artefacts_b(ppg_signals, artifact_probability=0.1, artifact_magnitude=0.7):
    """
    Adds smoother motion artifacts to PPG signals.

    Parameters:
    ppg_signals (xr.DataArray): 2D DataArray with dimensions (channels, samples)
    artifact_probability (float): Probability of an artifact occurring at any sample point
    artifact_magnitude (float): Magnitude of the artifacts to be added

    Returns:
    xr.DataArray: PPG signals with added smoother motion artifacts
    """
    # Convert DataArray to NumPy array for calculations
    ppg_array = ppg_signals.values

    # Copy the signals to avoid modifying the original data
    augmented_array = np.copy(ppg_array)

    # Number of channels and samples
    num_channels, num_samples = ppg_array.shape

    # Add artifacts to each channel
    for channel in range(num_channels):
        for i in range(num_samples):
            if np.random.rand() < artifact_probability:
                # Add a sinusoidal artifact with lower frequency for smoother transition
                frequency = np.random.uniform(0.01, 0.1)  # Lower frequency between 0.01 and 0.1 Hz
                duration = np.random.randint(50, 200)  # Longer duration between 50 and 200 samples
                t = np.arange(duration)
                sinusoid = artifact_magnitude * np.sin(2 * np.pi * frequency * t)
                end_idx = min(i + duration, num_samples)
                augmented_array[channel, i:end_idx] += sinusoid[:end_idx - i]

    # Create a new DataArray for the augmented signals
    augmented_signals = xr.DataArray(augmented_array, dims=ppg_signals.dims, coords=ppg_signals.coords)

    return augmented_signals


def add_artefacts_c(ppg_signals, artifact_probability=0.05, artifact_magnitude=1.0):
    """
    Adds more prominent motion artifacts to PPG signals.

    Parameters:
    ppg_signals (xr.DataArray): 2D DataArray with dimensions (channels, samples)
    artifact_probability (float): Probability of an artifact occurring at any sample point
    artifact_magnitude (float): Magnitude of the artifacts to be added

    Returns:
    xr.DataArray: PPG signals with added more prominent motion artifacts
    """
    # Convert DataArray to NumPy array for calculations
    ppg_array = ppg_signals.values

    # Copy the signals to avoid modifying the original data
    augmented_array = np.copy(ppg_array)

    # Number of channels and samples
    num_channels, num_samples = ppg_array.shape

    # Add artifacts to each channel
    for channel in range(num_channels):
        i = 0
        while i < num_samples:
            if np.random.rand() < artifact_probability:
                # Add a sinusoidal artifact with variable frequency and duration for smoother transition
                frequency = np.random.uniform(0.01, 0.2)  # Frequency between 0.01 and 0.2 Hz
                duration = np.random.randint(100, 300)  # Duration between 100 and 300 samples
                t = np.arange(duration)
                phase = np.random.uniform(0, 2 * np.pi)  # Random phase shift
                sinusoid = artifact_magnitude * np.sin(2 * np.pi * frequency * t + phase)
                end_idx = min(i + duration, num_samples)
                augmented_array[channel, i:end_idx] += sinusoid[:end_idx - i]

                # Introduce random baseline shifts to simulate motion
                baseline_shift = artifact_magnitude * (np.random.rand() - 0.5)
                augmented_array[channel, i:end_idx] += baseline_shift

                i += duration  # Skip the duration of the artifact to avoid overlapping
            else:
                i += 1

    # Create a new DataArray for the augmented signals
    augmented_signals = xr.DataArray(augmented_array, dims=ppg_signals.dims, coords=ppg_signals.coords)

    return augmented_signals


def add_artefacts_d(ppg_signals, artifact_probability=0.05, artifact_magnitude=0.7):
    """
    Adds level shift motion artifacts to PPG signals.

    Parameters:
    ppg_signals (xr.DataArray): 2D DataArray with dimensions (channels, samples)
    artifact_probability (float): Probability of an artifact occurring at any sample point
    artifact_magnitude (float): Magnitude of the level shift artifacts to be added

    Returns:
    xr.DataArray: PPG signals with added level shift motion artifacts
    """
    # Convert DataArray to NumPy array for calculations
    ppg_array = ppg_signals.values

    # Copy the signals to avoid modifying the original data
    augmented_array = np.copy(ppg_array)

    # Number of channels and samples
    num_channels, num_samples = ppg_array.shape

    # Add level shift artifacts to each channel
    for channel in range(num_channels):
        i = 0
        while i < num_samples:
            if np.random.rand() < artifact_probability:
                # Determine the duration of the level shift
                duration = np.random.randint(100, 300)  # Duration between 100 and 300 samples
                end_idx = min(i + duration, num_samples)

                # Generate a level shift
                level_shift = artifact_magnitude * (np.random.rand() - 0.5)
                augmented_array[channel, i:end_idx] += level_shift

                # Skip the duration of the artifact to avoid overlapping
                i += duration
            else:
                i += 1

    # Create a new DataArray for the augmented signals
    augmented_signals = xr.DataArray(augmented_array, dims=ppg_signals.dims, coords=ppg_signals.coords)

    return augmented_signals

