from rest_framework import serializers
# from rest_framework.fields import CurrentUserDefault

from .models import Account, Drink, Item, TransactionLog


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ('id', 'user', 'avatar', 'balance', 'free_access')
        read_only_fields = ('balance', 'free_access')
        depth = 1


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    creating_user = serializers.StringRelatedField(default=serializers.CurrentUserDefault())
    last_update_user = serializers.StringRelatedField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image', 'ean', 'price', 'creating_user', 'creation_date', 'last_update_user', 'last_update')
        depth = 1



class DrinkSerializer(ItemSerializer):
    class Meta:
        model = Drink
        fields = ('name', 'slug', 'price', 'image', 'ean', 'description','volume', 'alcoholic', 'caffeine', 'creating_user', 'creation_date', 'last_update_user', 'last_update')
        depth = 1

class TransactionLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_doing = serializers.StringRelatedField()
    class Meta:
        model = TransactionLog
        fields = "__all__"
