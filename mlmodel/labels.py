"""
MIT-BIH Annotation to AAMI Label Mapping

This module maps MIT-BIH ECG annotation symbols
to AAMI standard classes for arrhythmia detection.
"""

AAMI_MAP = {
    # Normal beats
    "N": "Normal",
    "L": "Normal",
    "R": "Normal",
    "e": "Normal",
    "j": "Normal",

    # Supraventricular ectopic beats
    "A": "Abnormal",
    "a": "Abnormal",
    "J": "Abnormal",
    "S": "Abnormal",

    # Ventricular ectopic beats
    "V": "Abnormal",
    "E": "Abnormal",

    # Fusion and unknown beats
    "F": "Abnormal",
    "Q": "Abnormal"
}

def map_label(symbol):
    """
    Maps MIT-BIH annotation symbol to AAMI label.

    Args:
        symbol (str): MIT-BIH beat annotation symbol

    Returns:
        str: 'Normal' or 'Abnormal'
    """
    return AAMI_MAP.get(symbol, "Abnormal")
