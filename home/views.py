from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.shortcuts import get_object_or_404

from accounts.models import User
from .models import PetFood
from .serializers import UserScoreSerializer, PetFoodListSerializer, PetFoodDetailSerializer


# User
class UserScoreListView(ListAPIView):
    serializer_class = UserScoreSerializer
    model = User
    queryset = User.get_user_by_score


# Food
class PetFoodlistView(ListAPIView):
    serializer_class = PetFoodListSerializer
    model = PetFood
    queryset = model.objects.filter(is_available=True)


class PetFoodDetailView(RetrieveAPIView):
    serializer_class = PetFoodDetailSerializer
    model = PetFood
    queryset = model.objects.filter(is_available=True)
    lookup_field = "id"
