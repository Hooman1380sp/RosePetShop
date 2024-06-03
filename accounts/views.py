from datetime import timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated

from .utils import Send_Otp_Code, Send_Otp_Code_Forgot_Link
from .permissions import IsOwnerAndAuthenticated
import random
from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserForgotPasswordSerializer,
    OtpCodeSerializer,
    EditUserProfileSerializer,
    ChangePasswordAccountSerializer,
    UserResetPasswordSerializer,
    VerifyChangePhoneNumberSerializer,
    ChangePhoneNumberSerializer
)


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    """

    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        result = cache.get(vd['phone_number'])
        if result:
            return Response(data={"message": "phone number already request, user should wait to ask again"})
        random_code = random.randint(1000, 9999)
        values = {"random_code": str(random_code),
                  "password": vd["password"],
                  "full_name": vd["full_name"],
                  "date_birth": vd["date_birth"]}
        cache.set(key=vd["phone_number"], value=values, timeout=60 * 4)
        cache.close()
        Send_Otp_Code(phone_number=vd['phone_number'], message=f"{random_code} Active Code ")
        return Response(data={"message": "ok"}, status=status.HTTP_302_FOUND)


class UserVerifyCodeView(APIView):
    serializer_class = OtpCodeSerializer
    """
    Verify view just got otp code and register user with session
    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        phone_number = vd["phone_number"]
        user_cache = cache.get(phone_number)
        if user_cache is None:
            return Response(data={"message": "code Instance is None"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        code = ser_data.validated_data.get("code")
        if code == user_cache["random_code"]:
            user = User.objects.create_user(phone_number=phone_number, password=user_cache["password"],
                                            full_name=user_cache["full_name"], date_birth=user_cache["date_birth"])
            access = AccessToken.for_user(user)
            access_token = access
            user.save()
            return Response(data={"message": "register user is successful", "JWT_Token": str(access_token)},
                            status=status.HTTP_201_CREATED)
        return Response(data={"message": "code is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    """
    page login view
    """

    def post(self, request):

        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user_phone = ser_data.validated_data.get("phone_number")
        user_password = ser_data.validated_data.get("password")
        user: User = User.objects.filter(phone_number=user_phone).first()
        if user is not None:
            if not user.is_active:
                return Response({"message": "Is Not Active Your Phone"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if user_phone == user.phone_number:
                if user.check_password(user_password) or user.password == user_password:
                    access = AccessToken.for_user(user)
                    access_token = access
                    return Response({"message": str(access_token)}, status=status.HTTP_202_ACCEPTED)
                return Response({"message": "password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "phone_number is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message": "we can.t find any user with your Specifications"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)


class UserForgotPasswordView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = UserForgotPasswordSerializer
    """
    page forget password
    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user_phone = ser_data.validated_data.get("phone_number")
        user = User.objects.filter(phone_number__iexact=user_phone).first()
        if user is not None:
            # todo (send code for user)
            random_str = get_random_string(86)
            cache.set(key=random_str, value=str(user_phone), timeout=60 * 4)
            cache.close()
            Send_Otp_Code_Forgot_Link(to=user_phone, random_str=random_str)
            return Response(data=ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "This Number is wrong "}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserResetPasswordView(APIView):
    serializer_class = UserResetPasswordSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    """
    page reset password!
    """

    def post(self, request, active_code):
        user_cache = cache.get(active_code)
        print(user_cache)
        print(type(user_cache))
        user: User = User.objects.filter(phone_number__iexact=user_cache).first()
        print(user)
        if user is not None:
            print(user.full_name)
            ser_data = UserResetPasswordSerializer(instance=user, data=request.data)
            ser_data.is_valid(raise_exception=True)
            user_password = ser_data.validated_data.get("password")
            user.set_password(user_password)
            user.save()
            cache.delete(active_code)
            cache.close()
            return Response(data={"message": "password change is successful"}, status=status.HTTP_301_MOVED_PERMANENTLY)
        return Response({"message": "A User With an unregistered Phone number"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordAccountView(APIView):
    serializer_class = ChangePasswordAccountSerializer
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    permission_classes = (IsOwnerAndAuthenticated,)

    """
    change password
    have tow field
    current_password == str
    new_password == str
    """

    def post(self, request):
        user: User = User.objects.get(id=request.user.id)
        self.check_object_permissions(request, user)
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        if user.check_password(ser_data.validated_data.get("current_password")):
            user.set_password(ser_data.validated_data.get("new_password"))
            print(ser_data.validated_data.get("current_password"))
            print(ser_data.validated_data.get("new_password"))
            user.save()
            return Response(data={"message": "change password is successful"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Password is Wrong"}, status=status.HTTP_409_CONFLICT)


class EditUserProfileView(APIView):
    serializer_class = EditUserProfileSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = (IsOwnerAndAuthenticated,)
    """
    this page for edit profile
    and get 4 field for edit(the method is partial)

    """

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        ser_data = self.serializer_class(instance=user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        self.check_object_permissions(request, user)
        ser_data = self.serializer_class(instance=user, data=request.data, partial=True)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        print(ser_data.data)
        return Response(data=ser_data.data, status=status.HTTP_206_PARTIAL_CONTENT)


# change phone number

class ChangePhoneNumberView(APIView):
    serializer_class = ChangePhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        new_phone_number = ser_data.validated_data['new_phone_number']
        result = cache.get(new_phone_number)
        if result:
            return Response(data={
                "message": "phone number already request, user should wait (4 min), to ask again"
            }, status=status.HTTP_409_CONFLICT)
        random_code = random.randint(1000, 9999)
        print(random_code)
        cache.set(key=request.user.phone_number, value={
            "new_phone_number": str(new_phone_number),
            "random_code": str(random_code)
        }, timeout=60 * 4)
        cache.close()
        Send_Otp_Code(phone_number=new_phone_number, message=f"{random_code} Active Code")
        return Response(data={"message": "ok"}, status=status.HTTP_302_FOUND)


class VerifyChangePhoneNumberView(APIView):
    serializer_class = VerifyChangePhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        cache_instance = cache.get(request.user.phone_number)
        print(vd["code"])
        print(cache_instance)
        if cache_instance["random_code"] == vd["code"]:
            user: User = User.objects.filter(id=request.user.id).first()
            user.phone_number = cache_instance["new_phone_number"]
            user.save()
            cache.close()
            return Response(data={"message": "change phone number is successful"}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"message": "change phone number isn't successful"}, status=status.HTTP_409_CONFLICT)
