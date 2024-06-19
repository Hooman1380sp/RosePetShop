from django.db import models
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model

from home.models import PetFood
from product.models import SuppliesPetProduct

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name="orders", verbose_name="کاربر")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده/نشده")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ('-is_paid', '-created')
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ ها"

    def __str__(self):
        return f"Order {self.id} by {self.user.full_name} - {self.user.phone_number}"

    @cached_property
    def get_total_price(self):
        """
        Total cost of all the items in an order
        """
        total = sum([item.cost for item in self.product_order_items.all()])
        total += sum([item.cost for item in self.food_order_items.all()])
        return total


class ProductOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="product_order_items", verbose_name="سفارش")
    product = models.ForeignKey(SuppliesPetProduct, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.PositiveIntegerField(verbose_name="قیمت")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def cost(self):
        return self.quantity * self.price


class FoodOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="food_order_items", verbose_name="سفارش")
    food = models.ForeignKey(to=PetFood, on_delete=models.CASCADE, verbose_name="غذا")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.PositiveIntegerField(verbose_name="قیمت")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.quantity} - {self.food.title}"

    @property
    def cost(self):
        return self.quantity * self.price
