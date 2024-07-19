from django.contrib import admin

from .models import AboutUs, ContactUs, CleaningServicePet, WorkingHours

admin.site.register(AboutUs)
admin.site.register(ContactUs)
admin.site.register(CleaningServicePet)
admin.site.register(WorkingHours)
