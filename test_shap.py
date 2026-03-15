import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_ecg.settings')
django.setup()

import numpy as np
from mlmodel.shap_explain import generate_shap_explanations

def test():
    # Abnormal dummy feature vector: HR, Mean R-R, SDNN, RMSSD
    fv = np.array([125, 0.4, 0.18, 0.18])
    patient_id = "test_patient"
    
    print("Generating SHAP explanations...")
    result = generate_shap_explanations(fv, patient_id)
    
    print("Result:", result)
    if result:
        print("Success! Check graphs dir for plots.")
    else:
        print("Failed.")

if __name__ == "__main__":
    test()
