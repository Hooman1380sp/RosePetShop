from django.db import models


class AboutUs(models.Model):
    address = models.TextField(max_length=1024, verbose_name="آدرس")
    description = models.TextField(max_length=4096, verbose_name="توضیحات")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'


class ContactUs(models.Model):
    phone_number = models.CharField(max_length=16, verbose_name="Phone")
    email = models.EmailField(max_length=256, verbose_name="Email")
    instagram = models.CharField(max_length=256, verbose_name="Instagram")
    whats_app = models.CharField(max_length=256, verbose_name="Whats App")
    telegram = models.CharField(max_length=256, verbose_name="Telegram")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما'


class CleaningServicePet(models.Model):
    haircut = models.TextField(max_length=4096, verbose_name="توضیحات کوتاه کردن مو سگ و گربه")
    nail_trimming = models.TextField(max_length=4096, verbose_name="توضیحات کوتاه کردن ناخن سگ و گربه")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "سرویس های پت"
        verbose_name_plural = "سرویس های پت"
