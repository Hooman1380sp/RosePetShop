from django.db import models
from django_cleanup import cleanup
from product.models import SuppliesPetProduct


@cleanup.select
class Blog(models.Model):
    title = models.CharField(max_length=128, verbose_name="عنوان")
    description = models.TextField(max_length=4096, verbose_name="توضیحات")
    aparat_video_link = models.URLField(max_length=1024, verbose_name="لینک ویدیو آپارات")
    image = models.ImageField(upload_to="blog/", verbose_name="تصویر")
    tags = models.ManyToManyField(to='BlogTag', verbose_name="تگ ها", blank=True)
    product = models.ManyToManyField(to=SuppliesPetProduct, verbose_name="محصولات مرتبط", blank=True)

    def __str__(self):
        return f"{self.title} - {self.description[:35]}"

    class Meta:
        ordering = ['-id']
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ"

    @property
    def List_Blog(self):
        return Blog.objects.filter()


class BlogTag(models.Model):
    title = models.CharField(max_length=256, verbose_name="عنوان")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "بلاگ تگ"
        verbose_name_plural = "بلاگ تگ"