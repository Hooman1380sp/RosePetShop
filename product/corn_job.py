from django_cron import CronJobBase, Schedule
from .models import SuppliesPetDiscount
from django.utils import timezone
from datetime import timedelta


class RemoveExpiredDiscountsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # هر 60 دقیقه اجرا شود

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'product.remove_expired_discounts'  # یک کد یکتا برای این کرون

    def do(self):
        now = timezone.now()
        SuppliesPetDiscount.objects.filter(created__lt=now - timedelta(hours=24)).delete()
