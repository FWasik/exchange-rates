from django.db import models
from django.utils import timezone

def get_default_time():
    return timezone.localtime(timezone.now())

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    
    def __str__(self):
        return self.code
    

class ExchangeRate(models.Model):
    currency_pair = models.CharField(max_length=6)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.DateTimeField(default=get_default_time)
    
    class Meta:
        ordering = ["-timestamp"]