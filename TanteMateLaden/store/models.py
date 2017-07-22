from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    """
    Generic base class for all kinds of items
    """
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="uploads/products/", blank=True)
    ean = models.CharField(max_length=13, blank=True)  # European Article Number (EAN)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)  # price in euro

    creation_date = models.DateTimeField(auto_now_add=True)
    creating_user = models.ForeignKey(User, related_name="creator")

    last_update = models.DateTimeField(auto_now=True)
    last_update_user = models.ForeignKey(User, related_name="updater")

    def __str__(self):
        return self.name


class Drink(Item):
    volume = models.DecimalField("Menge in l", max_digits=4, decimal_places=2)
    alcoholic = models.IntegerField(null=True)  # null or % of alcohol
    caffeine = models.IntegerField(null=True)  # caffeine in mg/l

    def __str__(self):
        return "%sl %s" % (self.volume, self.name)