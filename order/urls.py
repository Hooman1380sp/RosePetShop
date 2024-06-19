from django.urls import path
from .views import (
    # Cart
    CartClearGetView, CartRemoveGetView, CartDetailGetView, CartAddPostView,
    # Order
    OrderCreateView
)

app_name = "order"

urlpatterns = [
    # Cart
    path("cart-add/", CartAddPostView.as_view()),
    path("cart-detail/", CartDetailGetView.as_view()),
    path("cart-clear/", CartClearGetView.as_view()),
    path("cart-remove/<int:product_id>/", CartRemoveGetView.as_view()),
    # order
    path('create/', OrderCreateView.as_view()),
]
