def create_windows(signal, window_size=1800, step=1800):
    """
    Splits ECG signal into fixed-size windows
    """
    windows = []
    for i in range(0, len(signal) - window_size, step):
        windows.append(signal[i:i + window_size])
    return windows
