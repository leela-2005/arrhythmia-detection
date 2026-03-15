import joblib
import numpy as np

from ecg.services import load_ecg_record
from mlmodel.windowing import create_windows
from mlmodel.features import extract_feature_vector
from sklearn.ensemble import RandomForestClassifier


def train_model():
    RECORDS = ["100", "101", "102", "103"]

    X = []
    y = []

    for record in RECORDS:
        print(f"Processing record {record}")
        signal, _, _ = load_ecg_record(record)

        windows = create_windows(signal)
        print(f"Windows created: {len(windows)}")

        for w in windows[:30]:  # limit for demo
            features = extract_feature_vector(w)
            if features is not None:
                X.append(features)
                y.append(0)  # Normal class (demo)

    X = np.array(X)
    y = np.array(y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, "mlmodel/ecg_model.pkl")
    print("✅ Model trained and saved successfully")
