from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    """
    Generic base class for all kinds of items
    """
    name = models.CharField(max_length=32)
    description = models.TextField()
    ean = models.CharField(max_length=13)  # European Article Number (EAN)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # price in euro

    creation_date = models.DateTimeField(auto_now_add=True)
    creating_user = models.ForeignKey(User, related_name="creator")

    last_update = models.DateTimeField(auto_now=True)
    last_update_user = models.ForeignKey(User, related_name="updater")

    class Meta:
        abstract = True


class Drink(Item):
    volume = models.FloatField()
    alcoholic = models.IntegerField(null=True)  # null or % of alcohol
    caffeine = models.IntegerField(null=True)  # caffeine in mg/l
