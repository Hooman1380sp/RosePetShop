from django.urls import path
from .views import (
    # product
    SuppliesPetProductListView,
    SuppliesPetProductDetailView,
    MostVisitProductView,
    SuppliesPetProductDiscountListView,
    # category
    SuppliesPetProductListByCategoryView,
    SuppliesPetCategoryListView)

app_name = "product"

urlpatterns = [
    # product
    path("list/", SuppliesPetProductListView.as_view()),
    path("detail/<int:id>/", SuppliesPetProductDetailView.as_view()),
    path('most-visit/', MostVisitProductView.as_view()),
    path("discount/", SuppliesPetProductDiscountListView.as_view()),
    # category
    path('category-list/', SuppliesPetCategoryListView.as_view()),
    path('category-product-list/<int:id>/', SuppliesPetProductListByCategoryView.as_view()),
]