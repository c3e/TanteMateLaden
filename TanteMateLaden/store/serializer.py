from rest_framework import serializers

from .models import Account, Drink, Item


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ('id', 'user', 'avatar', 'balance', 'free_access')
        read_only_fields = ('balance', 'free_access')
        depth = 1


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    creating_user = serializers.StringRelatedField()
    last_update_user = serializers.StringRelatedField()
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image', 'ean', 'price', 'creating_user', 'creation_date', 'last_update_user', 'last_update')
        depth = 1


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    creating_user = serializers.StringRelatedField()
    last_update_user = serializers.StringRelatedField()

    class Meta:
        model = Drink
        fields = ('name', 'slug', 'price', 'image', 'ean', 'description', 'alcoholic', 'caffeine', 'creating_user', 'creation_date', 'last_update_user', 'last_update')
        depth = 1
