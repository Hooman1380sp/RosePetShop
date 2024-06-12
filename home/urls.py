from django.urls import path
from .views import UserScoreListView, PetFoodlistView, PetFoodDetailView

app_name = "home"

urlpatterns = [
    path("user-score/", UserScoreListView.as_view()),
    path("food-list/", PetFoodlistView.as_view()),
    path("food-detail/<int:id>/", PetFoodDetailView.as_view()),
]
