from django.contrib import admin
from .models import Order, ProductOrderItem, FoodOrderItem


class ProductOrderItemInline(admin.TabularInline):
    model = ProductOrderItem
    raw_id_fields = ("product",)


class FoodOrderItemInline(admin.TabularInline):
    model = FoodOrderItem
    raw_id_fields = ("food",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "updated", "created", "is_paid")
    list_filter = ("is_paid",)
    inlines = (ProductOrderItemInline, FoodOrderItemInline)
