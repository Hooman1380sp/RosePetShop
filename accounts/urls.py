from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserForgotPasswordView,
    EditUserProfileView,
    ChangePasswordAccountView,
    UserVerifyCodeView,
    UserResetPasswordView,
    ChangePhoneNumberView,
    VerifyChangePhoneNumberView
)

urlpatterns = [
    path("", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("verify/", UserVerifyCodeView.as_view(), name="verify"),
    path("forgot-password/", UserForgotPasswordView.as_view(), name="forget_pass"),
    path("edit-profile/", EditUserProfileView.as_view(), name="edit_profile"),
    path("account/reset-pass/<active_code>/", UserResetPasswordView.as_view()),
    path("change-password/", ChangePasswordAccountView.as_view(), name="change_password"),
    path("change-phone/", ChangePhoneNumberView.as_view(), name="change_phone"),
    path("verify-phone/", VerifyChangePhoneNumberView.as_view(), name="verifay_phone"),

]
