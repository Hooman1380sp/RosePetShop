from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ContactUs, AboutUs, CleaningServicePet, WorkingHours
from .serializers import ContactUsSerializer, AboutUsSerializer, CleaningServicePetSerializer, WorkingHoursSerializer


class ContactUsView(APIView):
    serializer_class = ContactUsSerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=ContactUs.objects.last())
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class AboutUsView(APIView):
    serializer_class = AboutUsSerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=AboutUs.objects.last())
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CleaningServicePetView(APIView):
    serializer_class = CleaningServicePetSerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=CleaningServicePet.objects.last())
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class WorkingHoursGetView(APIView):
    serializer_class = WorkingHoursSerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=WorkingHours.objects.last())
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
