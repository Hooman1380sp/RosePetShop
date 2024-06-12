from django.contrib import admin
from .models import PetFood, PetFoodImage


class PetFoodImageInLine(admin.StackedInline):
    model = PetFoodImage


@admin.register(PetFood)
class PetFoodAdmin(admin.ModelAdmin):
    inlines = [PetFoodImageInLine]
    search_fields = ["title"]
