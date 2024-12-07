from django.core.management.base import BaseCommand
from rates.models import Currency
import logging

logger = logging.getLogger("commands")


class Command(BaseCommand):
    help = "Ensure required currencies exist in the database"
    REQUIRED_CURRENCIES = ["EUR", "USD", "PLN", "JPY"]

    def handle(self, *args, **options):
        logger.info("Checking required default currencies in a database!")

        for code in self.REQUIRED_CURRENCIES:
            currency, created = Currency.objects.get_or_create(code=code)

            if created:
                logger.info(f"Currency {code} created")
            else:
                logger.warning(f"Currency {code} already exists")
