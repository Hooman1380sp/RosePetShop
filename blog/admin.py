from django.contrib import admin
from .models import BlogTag, Blog


admin.site.register(BlogTag)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    ordering = ("id",)
