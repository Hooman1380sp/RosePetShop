from django.core.management.base import BaseCommand
from ...models import SuppliesPetDiscount
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'remove product special price for 24 hour,(remove after 24!)'

    def handle(self, *args, **options):
        now = timezone.now()
        SuppliesPetDiscount.objects.filter(created__lt=now - timedelta(hours=24)).delete()
        self.stdout.write("whole expired product(during discount) removed")