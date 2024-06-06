from django.urls import path
from .views import BlogDetailView, BlogListView

app_name = "blog"

urlpatterns = [
    path("list/", BlogListView.as_view()),
    path("detail/<int:id>/", BlogDetailView.as_view()),
]