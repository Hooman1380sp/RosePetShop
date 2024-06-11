from django.contrib import admin
from .models import BlogTag, Blog

admin.site.register(BlogTag)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("id",)
    search_help_text = " (عنوان=title) شما میتوانید بر حسب عنوان مقالات سرچ کنید"