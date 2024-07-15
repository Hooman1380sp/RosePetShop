from .models import Blog
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["title", "aparat_video_link", "tags", "description", "image", "id"]
        depth = 1

    def get_image(self, obj):
        return f'/product/media/{obj.image}'
