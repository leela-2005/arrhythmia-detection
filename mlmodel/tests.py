from django.test import TestCase
import numpy as np
from mlmodel.features import extract_feature_vector

class FeatureExtractionTest(TestCase):

    def test_feature_extraction(self):
        signal = np.sin(np.linspace(0, 10, 3600))
        features = extract_feature_vector(signal)
        self.assertIsNotNone(features)
