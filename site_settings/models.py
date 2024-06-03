from django.db import models
from django_cleanup import cleanup


@cleanup.select
class AboutUs(models.Model):
    title = models.CharField(max_length=256, verbose_name="Subject")
    image = models.ImageField(upload_to="site_settings/about/", null=True, blank=True)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'About_Us'


class ContactUs(models.Model):
    phone_number = models.CharField(max_length=15, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")
    instagram = models.CharField(max_length=60, verbose_name="Instagram")
    address = models.TextField(verbose_name="Address")

    class Meta:
        verbose_name_plural = 'Contact_Us'


@cleanup.select
class ContactUsBody(models.Model):
    title = models.CharField(max_length=256, verbose_name="Title")
    image = models.ImageField(upload_to="site_settings/contact/",
                              null=True, blank=True, verbose_name="Image")
    body = models.TextField(verbose_name="Body")
    contact_us = models.ForeignKey(to='ContactUs', on_delete=models.CASCADE, verbose_name="Contact_US")

    class Meta:
        verbose_name_plural = 'Contact_Body'