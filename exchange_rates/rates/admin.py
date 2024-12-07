from django.contrib import admin
from .models import Currency, ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "code")


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("id", "currency_pair", "exchange_rate", "timestamp")
    list_filter = ("currency_pair", "timestamp")
    search_fields = ("currency_pair",)
    ordering = ("-timestamp",)
