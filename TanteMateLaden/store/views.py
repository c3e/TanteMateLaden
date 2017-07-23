from rest_framework import viewsets

from .models import Account, Drink, Item
from .serializer import AccountSerializer, DrinkSerializer, ItemSerializer


# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-creation_date')
    serializer_class = AccountSerializer


class DrinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Drink.objects.all().order_by('-creation_date')
    serializer_class = DrinkSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Item.objects.all().order_by('-creation_date')
    serializer_class = ItemSerializer
