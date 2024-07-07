import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# High-pass filter function
def high_pass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data


# Example multi-channel data (replace this with your actual data)
# Assuming multi_channel_data is a 2D numpy array with shape (channels, time_points)
multi_channel_data = np.random.randn(10, 1000)  # Replace with actual data
sampling_rate = 1000  # Replace with your actual sampling rate

# High-pass filter each channel
cutoff_frequency = 0.1  # Replace with your desired cutoff frequency
filtered_signals = np.array(
    [high_pass_filter(channel, cutoff_frequency, sampling_rate) for channel in multi_channel_data])

# Transpose to get shape (time_points, channels)
filtered_signals = filtered_signals.T

# Normalize the filtered signals
scaler = StandardScaler()
normalized_signals = scaler.fit_transform(filtered_signals)

# Apply PCA
n_components = 5  # Number of principal components to retain
pca = PCA(n_components=n_components)
principal_components = pca.fit_transform(normalized_signals)

# Extract the first principal component
pc1 = principal_components[:, 0]

# Plot the first principal component
plt.figure(figsize=(10, 6))
plt.plot(pc1)
plt.title('First Principal Component (Aggregated Peaks)')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()

# Detect peaks in the first principal component
threshold = 0.5  # Adjust threshold as needed
peaks, _ = find_peaks(pc1, height=threshold)

# Plot the first principal component with detected peaks
plt.figure(figsize=(10, 6))
plt.plot(pc1, label='PC1')
plt.plot(peaks, pc1[peaks], "x", label='Peaks')
plt.title('First Principal Component with Detected Peaks')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
