from django.contrib.auth.models import User
from .models import Account, Drink
from rest_framework import serializers


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ('id', 'user', 'avatar', 'balance', 'free_access')
        depth = 1


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = ('name', 'slug', 'price', 'ean', 'description', 'alcoholic', 'caffeine')