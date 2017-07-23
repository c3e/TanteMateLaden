from django.contrib.auth.models import User
from .models import Account, Drink
from rest_framework import serializers


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('balance', 'free_access')


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = ('name', 'slug', 'price', 'ean', 'description', 'alcoholic', 'caffeine')