from rest_framework import serializers
# from django.core.validators import MaxValueValidator, MinValueValidator


# # cart
# class CartAddSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField(validators=[MinValueValidator(1)])
#     quantity = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
#
#
# class CartDetailSerializer(serializers.Serializer):
#     product_name = serializers.CharField(max_length=512)
#     quantity = serializers.IntegerField()
#     price = serializers.IntegerField()
#     product_id = serializers.IntegerField()
#     total_price = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    food = serializers.ListField(required=False)
    product = serializers.ListField(required=False)

