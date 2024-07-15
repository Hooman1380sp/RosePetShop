from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


# TZ#$usBt22DRnC6z

class User(PermissionsMixin, AbstractBaseUser):
    full_name = models.CharField(max_length=120, null=True, blank=True, verbose_name="نام و نام خانوادگی")
    phone_number = models.CharField(max_length=11, unique=True, db_index=True)
    score = models.IntegerField(null=True, blank=True, verbose_name="امتیاز")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    is_active = models.BooleanField(default=True, verbose_name="active")
    date_birth = models.DateField(verbose_name="تاریخ تولد", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()

    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"

    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def get_user_by_score(self):
        return User.objects.order_by('score')[:10]

    class Meta:
        app_label = "accounts"
        # db_table = "User"
        db_table_comment = "custom user model with row attribute(AbstractBaseUser)"
        verbose_name = "User"
        verbose_name_plural = "Users"
