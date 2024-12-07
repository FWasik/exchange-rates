from rest_framework import views, status, generics
from rest_framework.response import Response
from .models import Currency, ExchangeRate
from .serializers import CurrencySerializer, ExchangeRateSerializer


class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all().order_by("code")
    serializer_class = CurrencySerializer


class ExchangeRateDetailView(views.APIView):
    def get(self, request, base_currency, target_currency):
        pair = base_currency + target_currency

        try:
            latest_rate = ExchangeRate.objects.filter(currency_pair=pair).latest(
                "timestamp"
            )
            serializer = ExchangeRateSerializer(latest_rate)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ExchangeRate.DoesNotExist:
            return Response(
                {
                    "detail": f"Exchange rate for the given currency pair {pair} does not exist."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
