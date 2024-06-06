from django.urls import path
from .views import UserScoreListView

app_name = "home"

urlpatterns = [
    path("user-score/", UserScoreListView.as_view()),
]