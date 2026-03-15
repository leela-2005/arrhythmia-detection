from django.db import models

class ECGRecord(models.Model):
    record_name = models.CharField(max_length=50)
    sqi = models.FloatField()
    prediction = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record_name
