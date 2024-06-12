from django.db import models
from django_cleanup import cleanup


class PetFood(models.Model):
    title = models.CharField(max_length=256, verbose_name="عنوان",
                             help_text="عنوان یا نام غذای خود را در این بخش وارد کنید")
    description = models.TextField(max_length=4096, verbose_name="توضیحات",
                                   help_text="توضیحات و شرح جزییات غذای خود را در این بخش بنویسید")
    unit = models.DecimalField(decimal_places=4, max_digits=9,verbose_name="واحد اندازه بسته غذا",
                               help_text="مقدار به کیلو یا گرم بنویسید و عدد صحیح یا اعشاری بنویسید!")
    is_available = models.BooleanField(default=True, verbose_name="غذا موجود هست/نیست")
    price = models.PositiveIntegerField(verbose_name="قیمت")

    class Meta:
        ordering = ["-id"]
        verbose_name = "غذا"
        verbose_name_plural = "غذاها"

    def __str__(self):
        return self.title


@cleanup.select
class PetFoodImage(models.Model):
    image = models.ImageField(upload_to="home/Pet_Food/", verbose_name="تصویر")
    food = models.ForeignKey(to=PetFood, on_delete=models.CASCADE, verbose_name="غذا")

    class Meta:
        verbose_name = "تصاویر غذا"
        verbose_name_plural = "تصاویر غذاها"

    def __str__(self):
        return str(self.id)