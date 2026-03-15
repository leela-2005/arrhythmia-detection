from django.test import TestCase
import numpy as np
from quality.quality_check import check_ecg_quality

class QualityCheckTest(TestCase):

    def test_good_quality_signal(self):
        signal = np.sin(np.linspace(0, 10, 3600))
        valid, sqi = check_ecg_quality(signal)
        self.assertTrue(valid)

    def test_bad_quality_signal(self):
        signal = np.random.normal(0, 5, 3600)
        valid, sqi = check_ecg_quality(signal)
        self.assertFalse(valid)
