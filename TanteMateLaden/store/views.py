from rest_framework import viewsets

from .models import Account
from .serializer import AccountSerializer


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
