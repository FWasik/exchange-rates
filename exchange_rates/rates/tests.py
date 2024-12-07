from django.test import TestCase
from rates.models import Currency, ExchangeRate
from django.core.management import call_command
import logging


class CommandsTest(TestCase):
    REQUIRED_CURRENCIES = ["EUR", "USD", "PLN", "JPY"]
    DEFAULT_PAIRS=["USDPLN", "USDJPY", "USDEUR", "PLNUSD", "PLNJPY", "PLNEUR", "EURUSD", "EURPLN", "EURJPY", "JPYUSD", "JPYEUR", "JPYPLN"]
    
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        
    def test_commands(self):
        self.assertEqual(Currency.objects.count(), 0)
        self.assertEqual(Currency.objects.count(), 0)
        
        call_command("default_currencies")
        call_command("get_exchange_rates")
        
        for curr in self.REQUIRED_CURRENCIES:
            obj = Currency.objects.filter(code=curr)
            self.assertEqual(obj.count(), 1, f"No currency {curr}")
        
        for pair in self.DEFAULT_PAIRS:
            obj = ExchangeRate.objects.filter(currency_pair=pair)
            self.assertEqual(obj.count(), 1, f"No rate for {pair}")
            

class CurrencyAPITest(TestCase):
    def setUp(self):
        Currency.objects.create(code="USD")
        Currency.objects.create(code="EUR")
        
    def test_currency_list_valid(self):
        response = self.client.get("/currency/")
        expected = [
            {
                "code": "EUR"
            },
            {
                "code": "USD"
            }
        ]
        
        self.assertEqual(response.status_code, 200, "Status codes do not match")
        self.assertListEqual(response.json(), expected, "Data does not match")
        
    def test_currency_list_invalid_action(self):
        response = self.client.post("/currency/")
        
        self.assertEqual(response.status_code, 405)
        

class ExchangeRateAPITest(TestCase):
    def setUp(self):
        ExchangeRate.objects.create(currency_pair="EURUSD", exchange_rate=1.2)
        
    def test_exchange_rate_valid(self):
        response = self.client.get("/currency/EUR/USD/")
        expected = {
            "currency_pair": "EURUSD",
            "exchange_rate": 1.2
        }
        
        self.assertEqual(response.status_code, 200, "Status codes do not match")
        self.assertDictEqual(response.json(), expected, "Data does not match")
        
    def test_exchange_rate_not_found(self):
        response = self.client.get("/currency/EUR/SOME_CODE/")
        
        self.assertEqual(response.status_code, 404)
        
    def test_exchange_rate_invalid_action(self):
        response = self.client.post("/currency/EUR/USD/")
        
        self.assertEqual(response.status_code, 405)