import os
import wfdb
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from django.conf import settings

# -----------------------------
# Load ECG record
# -----------------------------
def load_ecg_record(record_name, base_path=None):
    path = os.path.join(base_path, record_name) if base_path else record_name
    record = wfdb.rdrecord(path)

    # IMPORTANT: physical signal
    signal = record.p_signal[:, 0]
    fs = record.fs

    return signal, fs, record.sig_name


# -----------------------------
# Abnormal beat detection
# -----------------------------
ABNORMAL_SYMBOLS = {'V', 'A', 'L', 'R', 'F', 'E', 'S', 'a', 'J'}

import os
import wfdb

def get_abnormal_sample(record_name, base_path):
    atr_path = os.path.join(base_path, f"{record_name}.atr")

    # ✅ If annotation file does not exist, skip
    if not os.path.exists(atr_path):
        return None

    try:
        record_path = os.path.join(base_path, record_name)
        ann = wfdb.rdann(record_path, 'atr')

        # Return first abnormal beat sample
        for sample, symbol in zip(ann.sample, ann.symbol):
            if symbol != "N":
                return sample

        return None

    except Exception:
        return None



# -----------------------------
# Extract abnormal ECG window
# -----------------------------
def extract_abnormal_window(signal, abnormal_sample, fs, window_sec=5):
    half = int((window_sec * fs) / 2)
    start = max(0, abnormal_sample - half)
    end = min(len(signal), abnormal_sample + half)
    return signal[start:end]


# -----------------------------
# Generate ECG graph
# -----------------------------
def generate_ecg_graph(signal, record_id):
    graphs_dir = os.path.join(settings.MEDIA_ROOT, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)

    file_name = f"{record_id}.png"
    file_path = os.path.join(graphs_dir, file_name)

    plt.figure(figsize=(12, 4))
    plt.plot(signal, linewidth=1)
    plt.title("ECG Signal")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return f"graphs/{file_name}"


# -----------------------------
# Get Beats by Class (Visualizer)
# -----------------------------
def get_beats_by_class(record_name, base_path):
    """
    Extracts heartbeat segments from an MIT-BIH record and groups them by AAMI class.
    Returns a dictionary: {'N': [data...], 'S': [...], ...}
    Each data item is a list of voltage values (JSON serializable).
    """
    try:
        record_path = os.path.join(base_path, record_name)
        
        # Read signal and annotations
        # sampfrom/sampto could be used for pagination, but let's read all for now (MIT-BIH records are short ~30m)
        record = wfdb.rdrecord(record_path)
        ann = wfdb.rdann(record_path, 'atr')
        
        signal = record.p_signal[:, 0] # Lead I
        fs = record.fs
        
        # AAMI Classes Mapping
        # N: Normal
        # S: Supraventricular (SVEB)
        # V: Ventricular (VEB)
        # F: Fusion
        # Q: Unknown / Paced / Other
        
        classes = {
            'N': ['N', 'L', 'R', 'e', 'j'],
            'S': ['A', 'a', 'J', 'S'],
            'V': ['V', 'E'],
            'F': ['F'],
            'Q': ['/', 'f', 'Q']
        }
        
        results = {'N': [], 'S': [], 'V': [], 'F': [], 'Q': []}
        
        # Window size: 0.6s total (0.2s before, 0.4s after) is standard for beats
        # Or let's do 1 second: 0.3s before, 0.7s after to see context
        before = int(0.3 * fs)
        after = int(0.5 * fs) # 0.8s total window
        
        # Limit number of beats per class to avoid crashing the browser with 2000 beats
        limit_per_class = 20
        counts = {k: 0 for k in results.keys()}
        
        for sample, symbol in zip(ann.sample, ann.symbol):
            beat_type = None
            for key, symbols in classes.items():
                if symbol in symbols:
                    beat_type = key
                    break
            
            if not beat_type:
                beat_type = 'Q' # Default to unknown if not in AAMI map
            
            if counts[beat_type] >= limit_per_class:
                continue
                
            # Extract window
            if sample > before and sample + after < len(signal):
                segment = signal[sample - before : sample + after]
                
                # Check for NaNs or flatlines? simple check:
                if len(segment) > 0:
                    results[beat_type].append(segment.tolist())
                    counts[beat_type] += 1
                    
        return results

    except Exception as e:
        print(f"Error loading beats for {record_name}: {e}")
        return {'N': [], 'S': [], 'V': [], 'F': [], 'Q': []}

