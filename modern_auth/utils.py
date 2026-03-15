import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP
from django.contrib.auth.models import User

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user: User):
    otp_code = generate_otp()
    
    # Invalidate previous OTPs
    EmailOTP.objects.filter(user=user, is_used=False).update(is_used=True)
    
    # Save new OTP
    EmailOTP.objects.create(user=user, otp_code=otp_code)

    # Send email
    subject = "Smart ECG - Password Reset OTP"
    message = f"Hello {user.username},\n\nYour OTP for password reset is: {otp_code}\n\nIt is valid for 10 minutes.\n\nThank you,\nSmart ECG Team"
    
    send_mail(
        subject,
        message,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@smartecg.com'),
        [user.email],
        fail_silently=False,
    )
