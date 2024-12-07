from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "rates"

urlpatterns = [
    path("currency/", views.CurrencyListView.as_view(), name="currency-list"),
    path("currency/<str:base_currency>/<str:target_currency>/", views.ExchangeRateDetailView.as_view(), name="exchange-rate")
]
