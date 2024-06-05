from django.urls import path

from .views import ContactUsView, AboutUsView, CleaningServicePetView

app_name = "site"

urlpatterns = [
    path('contact-us/', ContactUsView.as_view()),
    path('about-us/', AboutUsView.as_view()),
    path('service-pet/', CleaningServicePetView.as_view())
]
