from rest_framework import status
from rest_framework.generics import ListAPIView
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.shortcuts import get_object_or_404

from .utils import get_client_ip
from .paginations import PageNumberPaginationSize10
from .models import SuppliesPetProduct, SuppliesPetCategory, SuppliesPetDiscount, ProductVisit
from .serializers import (
    SuppliesPetProductListSerializer,
    SuppliesPetCategorySerializer,
    SuppliesPetProductDetailSerializer,
    SuppliesPetProductDiscountListSerializer)


# product

class SuppliesPetProductListView(ListAPIView):
    serializer_class = SuppliesPetProductListSerializer
    model = SuppliesPetProduct
    queryset = model.objects.filter(is_available=True)
    pagination_class = PageNumberPaginationSize10


class SuppliesPetProductDetailView(APIView):
    serializer_class = SuppliesPetProductDetailSerializer

    def get(self, request, id):
        # queryset = SuppliesPetProduct.objects.filter(is_delete=False, is_active=True, id=id).first()
        object_product = get_object_or_404(SuppliesPetProduct, id=id, is_available=True)
        loaded_product = object_product
        ser_data = self.serializer_class(instance=object_product)
        # get user ip and user id  for visit-product
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id).save()
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class MostVisitProductView(APIView):
    serializer_class = SuppliesPetProductListSerializer
    pagination_class = PageNumberPaginationSize10
    # throttle_scope = 'get_request'
    """
     most visit product api (12P) => 12 number product api
    """

    def get(self, request):
        queryset = SuppliesPetProduct.objects.filter(is_available=True).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        ser_data = self.serializer_class(instance=queryset, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SuppliesPetProductDiscountListView(APIView):
    serializer_class = SuppliesPetProductDiscountListSerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=SuppliesPetDiscount.objects.filter(
            product__is_available=True), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


# category

class SuppliesPetCategoryListView(APIView):
    serializer_class = SuppliesPetCategorySerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=SuppliesPetCategory.objects.all(), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SuppliesPetProductListByCategoryView(APIView):
    """get product by id category"""
    serializer_class = SuppliesPetProductListSerializer
    pagination_class = PageNumberPaginationSize10

    def get(self, request, id):
        ser_data = self.serializer_class(instance=SuppliesPetProduct.objects.filter(
            category_id=id, is_available=True), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
