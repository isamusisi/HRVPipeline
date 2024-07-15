import numpy as np
def normalize(sig):
    min_val = np.min(sig)
    max_val = np.max(sig)
    return (sig - min_val) / (max_val - min_val)