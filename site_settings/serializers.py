from rest_framework import serializers

from .models import ContactUs, AboutUs, CleaningServicePet


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class CleaningServicePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningServicePet
        fields = '__all__'
