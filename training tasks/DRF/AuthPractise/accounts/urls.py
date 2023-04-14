from django.urls import path
from accounts.views import RegisterView, VerifyOtp



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtp.as_view(), name='verify-otp'),
]
