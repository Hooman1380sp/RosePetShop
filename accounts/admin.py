from django.contrib import admin
from .models import User
from django.utils.dateformat import format as date_format


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("phone_number",)
    list_display = ("id", "phone_number", "full_name", "created_formatted")
    list_filter = ("created",)

    def created_formatted(self, obj):
        return date_format(obj.created, 'Y-m-d H:i:s')
