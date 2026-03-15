import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ecg_model.pkl")
model = joblib.load(MODEL_PATH)

def hqcnn_predict(feature_vector):
    """
    feature_vector shape must be (1, n_features)
    """
    feature_vector = np.asarray(feature_vector)

    # 🔒 SAFETY: force 2D
    if feature_vector.ndim == 3:
        feature_vector = feature_vector.reshape(feature_vector.shape[0], -1)

    if feature_vector.ndim != 2:
        raise ValueError("Feature vector must be 2D")

    pred = model.predict(feature_vector)[0]
    return "Abnormal" if pred == 1 else "Normal"
