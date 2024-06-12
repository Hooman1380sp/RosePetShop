from django.db import models
from django.utils.html import mark_safe
from django_cleanup import cleanup

from accounts.models import User


@cleanup.select
class SuppliesPetCategory(models.Model):
    title = models.CharField(max_length=512, verbose_name="عنوان")
    image = models.ImageField(upload_to="product/", verbose_name="تصویر")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته بندی ها"
        verbose_name_plural = "دسته بندی"

    @property
    def admin_image(self):
        return mark_safe('<img style="height:150px;" src="%s" />' % self.image.url)

    def __str__(self):
        return self.title


class SuppliesPetProduct(models.Model):
    """
    product is any type to split by category`s

    """

    title = models.CharField(max_length=512, verbose_name="عنوان")
    description = models.TextField(max_length=1024, verbose_name="توضیحات")
    color = models.CharField(max_length=512, verbose_name="رنگ محصول")
    unit = models.CharField(max_length=512, verbose_name="وزن", null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name="قیمت")
    made_by_country = models.CharField(max_length=256, verbose_name="ساخت کشور")
    is_available = models.BooleanField(default=True, verbose_name="موجود در انبار هست/نیست")
    category = models.ForeignKey(to=SuppliesPetCategory, on_delete=models.CASCADE,
                                 verbose_name="دسته بندی",
                                 related_name="supplies_pet_category",
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ["-created"]
        verbose_name = "لوازم جانبی"
        verbose_name_plural = "لوازم جانبی ها"

    def __str__(self):
        return self.title


class SuppliesPetDiscount(models.Model):
    """
    SuppliesPetDiscount has for special price one day (24h).
    and after 24h by corn job deleted the record automatically
    """

    product = models.ForeignKey(to=SuppliesPetProduct, on_delete=models.CASCADE,
                                verbose_name="محصول", related_name="supplies_pet_product")
    discount_price = models.PositiveIntegerField(verbose_name="قیمت ویژه")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "محصول تخفیف ‌دار"
        verbose_name_plural = "محصولات تخفیف ‌دار"

    def __str__(self):
        return f"{self.product.title} - {self.discount_price}"


@cleanup.select
class SuppliesPetImage(models.Model):
    image = models.ImageField(upload_to="product/supplies_image/", verbose_name="تصویر")
    product = models.ForeignKey(to=SuppliesPetProduct, on_delete=models.CASCADE,
                                verbose_name="محصول",
                                related_name="supplies_pet_image")

    @property
    def admin_image(self):
        return mark_safe('<img style="height:125px;" src="%s" />' % self.image.url)


class ProductVisit(models.Model):
    product = models.ForeignKey(to=SuppliesPetProduct,
                                on_delete=models.CASCADE, verbose_name="محصول", related_name="productvisit")
    ip = models.CharField(max_length=32, verbose_name="آی پی کاربر")
    user = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="کاربر")

    def __str__(self):
        return f"{self.product.title[:50]} - {self.ip}"

    class Meta:
        verbose_name = "بازدید محصولات"
        verbose_name_plural = "بازدید های محصولات"
