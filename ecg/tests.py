from django.test import TestCase
import numpy as np
from ecg.services import load_ecg_record

class ECGServiceTest(TestCase):

    def test_load_signal(self):
        signal, fs, _ = load_ecg_record("100")
        self.assertIsNotNone(signal)
        self.assertEqual(fs, 360)
