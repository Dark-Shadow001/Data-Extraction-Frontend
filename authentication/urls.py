from django.urls import path
from .views import LoginView, RegistrationView, ResetPasswordEmailView, ResetPasswordFormView, ResetPasswordView, GenerateOTP, ValidateOTP
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('register', RegistrationView.as_view(), name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("resetpasswordemail", ResetPasswordEmailView.as_view(),
         name="resetPasswordEmail"),
    path("resetpasswordform/<str:username>",
         ResetPasswordFormView.as_view(), name="resetPasswordForm"),
    path("resetpassword", ResetPasswordView.as_view(), name="resetPassword"),
    path("generateOTP", GenerateOTP.as_view(), name="generateOTP"),
    path("validateOTP/<str:otpId>", ValidateOTP.as_view(), name="validateOTP"),
]
