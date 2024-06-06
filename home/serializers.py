from accounts.models import User
from rest_framework import serializers


class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "score")
