from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from .models import EmailOTP
from .utils import send_otp_email

# To use Django's auth views but customize them
from django.contrib.auth.views import LoginView
from dashboard.forms import UserRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return super().get_success_url()

class CustomRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserRegistrationForm()
        return render(request, 'dashboard/register.html', {'form': form})
        
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
            
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('home')
            
        return render(request, 'dashboard/register.html', {'form': form})


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'modern_auth/forgot_password.html')
        
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.filter(email=email).first()
            if user:
                send_otp_email(user)
                request.session['reset_email'] = email
                messages.success(request, "An OTP has been sent to your email.")
                return redirect('verify_otp')
            else:
                messages.error(request, "No account found with that email address.")
                return render(request, 'modern_auth/forgot_password.html')
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'modern_auth/forgot_password.html')

class VerifyOTPView(View):
    def get(self, request):
        if 'reset_email' not in request.session:
            return redirect('forgot_password')
        return render(request, 'modern_auth/verify_otp.html')
        
    def post(self, request):
        if 'reset_email' not in request.session:
            return redirect('forgot_password')
            
        email = request.session['reset_email']
        otp_code = request.POST.get('otp_code')
        
        try:
            user = User.objects.get(email=email)
            otp_record = EmailOTP.objects.filter(user=user, otp_code=otp_code).order_by('-created_at').first()
            
            if otp_record and otp_record.is_valid():
                otp_record.is_used = True
                otp_record.save()
                request.session['otp_verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid or expired OTP.")
                return render(request, 'modern_auth/verify_otp.html')
                
        except User.DoesNotExist:
             messages.error(request, "User error.")
             return redirect('forgot_password')

class ResetPasswordView(View):
    def get(self, request):
        if not request.session.get('otp_verified'):
            return redirect('verify_otp')
        return render(request, 'modern_auth/reset_password.html')
        
    def post(self, request):
        if not request.session.get('otp_verified'):
            return redirect('verify_otp')
            
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'modern_auth/reset_password.html')
            
        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Clean up session
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Error resetting password.")
            return render(request, 'modern_auth/reset_password.html')
