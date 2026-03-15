import numpy as np

def check_ecg_quality(signal):
    """
    Computes Signal Quality Index (SQI)

    Returns:
        valid (bool): Whether signal is acceptable
        sqi (float): Signal Quality Index
    """

    if signal is None or len(signal) == 0:
        return False, 0.0

    # Noise estimation using standard deviation
    noise_level = np.std(signal)

    # SQI calculation (simple & explainable)
    sqi = 1 / (1 + noise_level)

    # Threshold-based validation
    if sqi < 0.7:
        return False, sqi

    return True, sqi
