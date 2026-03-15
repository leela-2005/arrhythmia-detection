from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class OTP(models.fields.Field):
    pass # Temporary placeholder

class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # OTP is valid for 10 minutes
        now = timezone.now()
        diff = now - self.created_at
        return not self.is_used and diff <= datetime.timedelta(minutes=10)
