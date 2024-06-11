from rest_framework import serializers

from .models import SuppliesPetProduct, SuppliesPetCategory, SuppliesPetImage, SuppliesPetDiscount


# product
class SuppliesPetProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = SuppliesPetProduct
        fields = ("title", "description", "images", "made_by_country", "unit", "price", "color", "id")

    def get_images(self, obj):
        return SuppliesPetImageSerializer(instance=SuppliesPetImage.objects.filter(
            product_id=obj.id), many=True).data


class SuppliesPetImageSerializer(serializers.ModelSerializer):
    """
    we need several picture for product and.
    we get list image related the product
    """

    class Meta:
        model = SuppliesPetImage
        fields = ("image", "product")


class SuppliesPetProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = SuppliesPetProduct
        fields = ("title", "description", "images", "made_by_country", "unit", "price", "color")

    def get_images(self, obj):
        return SuppliesPetImageSerializer(instance=SuppliesPetImage.objects.filter(
            product_id=obj.id), many=True).data


class SuppliesPetProductDiscountListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuppliesPetDiscount
        fields = ("discount_price", "product")
        depth = 1

# category

class SuppliesPetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesPetCategory
        fields = ("image", "title", "id")

