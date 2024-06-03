from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "password", "date_birth", "full_name"]
        extra_kwargs = {
            "password": {"required": True, "write_only": True, "style": {"input_type": "password"}},
            "phone_number": {"required": True, "min_length": 11, "max_length": 13},
            "full_name": {"required": True, "max_length": 120},
            "date_birth": {"required": True}
        }

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError("phone number is duplicate")
        return value


class OtpCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4)

    class Meta:
        model = User
        fields = ["phone_number", "code"]
        extra_kwargs = {
            "phone_number": {"required": True, "min_length": 11, "max_length": 13},
        }

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError("phone number is duplicate")
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ("phone_number", "password")
        extra_kwargs = {
            "password": {"required": True, "write_only": True, "style": {"input_type": "password"}},
            "phone_number": {"max_length": 11},
        }


class UserForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)


class ChangePasswordAccountSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, max_length=20, min_length=8)
    current_password = serializers.CharField(write_only=True, max_length=20, min_length=8)


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["date_birth", "full_name"]


class ChangePhoneNumberSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField(max_length=13, min_length=11)


class VerifyChangePhoneNumberSerializer(serializers.Serializer):
    # new_phone_number = serializers.CharField(max_length=13, min_length=11)
    code = serializers.CharField(max_length=4, min_length=4)
