from rest_framework import serializers

from .models import SuppliesPetProduct, SuppliesPetCategory, SuppliesPetImage, SuppliesPetDiscount


# product
class SuppliesPetProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = SuppliesPetProduct
        fields = (
            "title", "description", "discount_amount", "images", "made_by_country", "unit", "price", "color", "id")

    def get_images(self, obj):
        return SuppliesPetImageSerializer(instance=SuppliesPetImage.objects.filter(
            product_id=obj.id), many=True).data

    def get_discount_amount(self, obj):
        return DisCountAmountFieldSerializer(instance=obj.supplies_pet_product.all().first()).data


class SuppliesPetImageSerializer(serializers.ModelSerializer):
    """
    we need several picture for product and.
    we get list image related the product
    """

    class Meta:
        model = SuppliesPetImage
        fields = ("image",)


class SuppliesPetProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = SuppliesPetProduct
        fields = ("title", "description", "discount_amount", "images", "made_by_country", "unit", "price", "color")

    def get_images(self, obj):
        return SuppliesPetImageSerializer(instance=SuppliesPetImage.objects.filter(
            product_id=obj.id), many=True).data

    def get_discount_amount(self, obj):
        return DisCountAmountFieldSerializer(instance=obj.supplies_pet_product.all().first()).data


class SuppliesPetProductDiscountListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = SuppliesPetDiscount
        fields = ("discount_price", "product", "images")
        depth = 1

    def get_images(self, obj: SuppliesPetDiscount):
        return SuppliesPetImageSerializer(instance=SuppliesPetImage.objects.filter(
            product_id=obj.product.id), many=True).data


class DisCountAmountFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesPetDiscount
        fields = ("discount_price",)


# category

class SuppliesPetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesPetCategory
        fields = ("image", "title", "id")
