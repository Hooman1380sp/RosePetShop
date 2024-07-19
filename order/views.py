from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from product.models import SuppliesPetProduct, SuppliesPetDiscount
from home.models import PetFood
# from .cart import CartProduct, CartFood
# from .serializers import CartAddSerializer, CartDetailSerializer
from .serializers import OrderSerializer
from .models import FoodOrderItem, Order, ProductOrderItem


# # Cart
# class CartAddPostView(APIView):
#     """
#     get fild (product_id and quantity) and get product of database for some operation
#     """
#     serializer_class = CartAddSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def post(self, request):
#         Type = request.query_params.get('Type', None)
#         if Type == "Product":
#             ser_data = self.serializer_class(data=request.data)
#             ser_data.is_valid(raise_exception=True)
#             vd = ser_data.validated_data
#             print(vd)
#             product = get_object_or_404(SuppliesPetProduct, id=vd['product_id'])
#             cart = CartProduct(request=request)
#             cart.add(product=product, quantity=vd["quantity"])
#             return Response(data=ser_data.data, status=status.HTTP_200_OK)
#         elif Type == "Food":
#             ser_data = self.serializer_class(data=request.data)
#             ser_data.is_valid(raise_exception=True)
#             vd = ser_data.validated_data
#             print(vd)
#             food = get_object_or_404(PetFood, id=vd['product_id'])
#             cart = CartFood(request=request)
#             cart.add(food=food, quantity=vd["quantity"])
#             return Response(data=ser_data.data, status=status.HTTP_200_OK)
#         else:
#             return Response(data={"message": "something is wrong"}, status=status.HTTP_409_CONFLICT)
#
#
# class CartDetailGetView(APIView):
#     """
#     get whole detail just with get request for user (user must authoriz)!
#     """
#     serializer_class = CartDetailSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         Type = request.query_params.get('Type', None)
#         if Type == "Product":
#             cart = CartProduct(request)
#             items = cart.get_items()
#             print(items)
#             serializer = self.serializer_class(items, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif Type == "Food":
#             cart = CartFood(request)
#             items = cart.get_items()
#             print(items)
#             serializer = self.serializer_class(items, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(data={"message": "something is wrong"}, status=status.HTTP_409_CONFLICT)
#
#
# class CartRemoveGetView(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request, product_id):
#         Type = request.query_params.get('Type', None)
#         if Type == "Product":
#             product = SuppliesPetProduct.objects.get(id=product_id, is_available=True)
#             cart = CartProduct(request)
#             cart.remove(product)
#             return Response({'status': 'Product Removed'}, status=status.HTTP_200_OK)
#         elif Type == "Food":
#             food = PetFood.objects.get(id=product_id, is_available=True)
#             cart = CartFood(request)
#             cart.remove(food)
#             return Response({'status': 'Food Removed'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Product or Food. not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class CartClearGetView(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         cart = CartProduct(request)
#         cart.clear()
#         return Response({'status': 'cart cleared'}, status=status.HTTP_200_OK)
#
#
# # order
#
#
# class OrderCreateView(APIView):
#     def get(self, request):
#         cart_product = CartProduct(request)
#         cart_food = CartFood(request)
#
#         # Create a new order
#         order = Order.objects.create(user=request.user)
#
#         # Add product items to order
#         product_items = cart_product.get_items()
#         if product_items:
#             for item in product_items:
#                 product = get_object_or_404(SuppliesPetProduct, id=item['product_id'], is_available=True)
#                 discount = SuppliesPetDiscount.objects.filter(product=product,
#                                                               product__is_available=True).first()
#                 price = discount.discount_price if discount else product.price
#                 ProductOrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=price)
#
#         # Add food items to order
#         food_items = cart_food.get_items()
#         if food_items:
#             for item in food_items:
#                 food = get_object_or_404(PetFood, id=item['product_id'], is_available=True)
#                 FoodOrderItem.objects.create(order=order, food=food, quantity=item['quantity'], price=food.price)
#
#         # Clear the cart after creating the order
#         # we can clear with cart product (whole session cart!)
#         cart_product.clear()
#
#         return Response({'message': 'Order created successfully!'}, status=status.HTTP_201_CREATED)


# order


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        order = Order.objects.create(user=request.user)
        vd = ser_data.validated_data

        # Process food items
        food_items = vd.get('food_order_items')
        print(food_items)
        if food_items:
            for item in food_items:
                FoodOrderItem.objects.create(order=order,
                                             food_id=item["food_id"],
                                             quantity=item["quantity"],
                                             price=item["price"])
        # Process product items
        product_items = vd.get('product')
        print(product_items)
        if product_items:
            for item in product_items:
                ProductOrderItem.objects.create(order=order,
                                                product_id=item["product_id"],
                                                quantity=item["quantity"],
                                                price=item["price"]
                                                )

        return Response({'message': 'Order created successfully!'}, status=status.HTTP_201_CREATED)
