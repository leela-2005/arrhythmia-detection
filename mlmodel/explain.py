import numpy as np

def explain_prediction(feature_vector, prediction):
    explanations = []

    if feature_vector is None:
        return ["Insufficient ECG data for explanation"]

    fv = np.asarray(feature_vector).reshape(-1)

    hr = fv[0]       # Heart rate
    rr = fv[1]       # RR interval
    sdnn = fv[2]     # HRV
    rmssd = fv[3]    # HRV

    # ---- Abnormal explanations ----
    if hr < 60:
        explanations.append("Bradycardia detected (low heart rate)")
    elif hr > 100:
        explanations.append("Tachycardia detected (high heart rate)")

    if rr < 0.6 or rr > 1.2:
        explanations.append("Irregular R–R intervals observed")

    if sdnn > 0.12:
        explanations.append("High heart rate variability detected")

    if rmssd > 0.12:
        explanations.append("Abnormal short-term HRV observed")

    # ---- Normal case ----
    if not explanations:
        explanations.append("Normal sinus rhythm observed")

    return explanations
