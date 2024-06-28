from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from accounts.models import User
from .paginations import PageNumberPaginationSize10
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
    pagination_class = PageNumberPaginationSize10


class PetFoodDetailView(RetrieveAPIView):
    serializer_class = PetFoodDetailSerializer
    model = PetFood
    queryset = model.objects.filter(is_available=True)
    lookup_field = "id"
