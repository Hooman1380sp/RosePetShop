from accounts.models import User
from rest_framework import serializers
from .models import PetFood, PetFoodImage


# User
class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "score")


# Food

class PetFoodListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PetFood
        fields = ("title", "description", "unit", "price", "image")

    def get_image(self, obj):
        return PetFoodImageSerializer(instance=PetFoodImage.objects.filter(food_id=obj.id), many=True).data


class PetFoodDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PetFood
        fields = ("title", "description", "unit", "price", "image")

    def get_image(self, obj):
        return PetFoodImageSerializer(instance=PetFoodImage.objects.filter(food_id=obj.id), many=True).data


class PetFoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetFoodImage
        fields = ("image",)
