from django.core.management.base import BaseCommand
from rates.models import Currency, ExchangeRate
import requests
from django.utils import timezone
from decimal import Decimal
import logging

logger = logging.getLogger("commands")

class Command(BaseCommand):
    help = "Fetch and store in database latest exchange rates for currencies. Exchange rates with given pair are unique for each date"

    def fetch_exchange_rates(self, base_currency):
        try:
            response = requests.get(f"https://open.er-api.com/v6/latest/{base_currency}")
            response.raise_for_status()

        except requests.RequestException as e:
            logger.error(f"Failed to fetch rates for currency {base_currency}: {e}")
            return

        data = response.json()

        if data.get("result") == "error":
            logger.error(f"An error for currency {base_currency}: {data.get('error-type')}")
            return

        if "rates" not in data:
            logger.error(f"There are no rates for {base_currency}")
            return

        return data

    def save_exchange_rate(self, pair, rate):
        today = timezone.localtime(timezone.now()).date()
        existing_rate = ExchangeRate.objects.filter(
            currency_pair=pair,
            timestamp__date=today
        ).exists()
        
        if existing_rate:
            logger.warning(f"A rate for {pair} already exists with today's date. Skipping!")
            return
        
        ExchangeRate.objects.create(currency_pair=pair, exchange_rate=rate)
        logger.info(f"Exchange rate {rate} for {pair} was saved!")

    def handle(self, *args, **options):
        logger.info("Starting to fetch and store rates!")
        
        try:
            currencies = Currency.objects.all()

            for base_currency in currencies:
                rest_of_currencies = Currency.objects.exclude(id=base_currency.id)
                if not rest_of_currencies:
                    continue

                data = self.fetch_exchange_rates(base_currency.code)
                if not data:
                    continue

                rates = data.get("rates")

                for target_currency in rest_of_currencies:
                    pair = base_currency.code + target_currency.code
                    rate = rates.get(target_currency.code)
                    
                    if rate:
                        rounded_rate = round(Decimal(rate), 4)
                        self.save_exchange_rate(pair, rounded_rate)
                    else:
                        logger.warning(f"No rate found for {pair}!")
        
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")