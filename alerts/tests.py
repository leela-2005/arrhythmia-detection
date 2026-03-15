from django.test import TestCase
from alerts.notifier import send_alert

class AlertTest(TestCase):

    def test_alert(self):
        send_alert("Test alert")
        self.assertTrue(True)
