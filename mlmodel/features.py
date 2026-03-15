import numpy as np
import neurokit2 as nk

def extract_feature_vector(ecg_signal, sampling_rate):
    try:
        ecg_signal = np.asarray(ecg_signal).astype(float)

        # ❌ Reject too short segments
        if len(ecg_signal) < sampling_rate * 3:
            return None

        # 🔧 Clean ECG
        cleaned = nk.ecg_clean(ecg_signal, sampling_rate=sampling_rate)

        # 🔧 Detect R-peaks
        peaks, info = nk.ecg_peaks(cleaned, sampling_rate=sampling_rate)

        rpeaks = info.get("ECG_R_Peaks", [])

        # ❌ Need at least 3 beats
        if len(rpeaks) < 3:
            return None

        # 🔍 HR & RR
        rr_intervals = np.diff(rpeaks) / sampling_rate
        hr = 60 / np.mean(rr_intervals)

        # 🔍 HRV features
        sdnn = np.std(rr_intervals)
        rmssd = np.sqrt(np.mean(np.diff(rr_intervals) ** 2))

        features = np.array([hr, np.mean(rr_intervals), sdnn, rmssd])

        # ❌ Invalid numbers
        if np.isnan(features).any() or np.isinf(features).any():
            return None

        return features.reshape(1, -1)

    except Exception:
        return None
