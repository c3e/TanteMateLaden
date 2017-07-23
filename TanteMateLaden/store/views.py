from django.shortcuts import render
from .models import Account, Drink
from rest_framework import viewsets
from .serializer import AccountSerializer, DrinkSerializer
# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-creation_date')
    serializer_class = AccountSerializer