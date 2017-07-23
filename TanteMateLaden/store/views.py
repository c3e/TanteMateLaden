from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Account, Drink, Item, TransactionLog
from django.contrib.auth.models import User
from .serializer import AccountSerializer, DrinkSerializer, ItemSerializer, TransactionLogSerializer
from django.core.exceptions import PermissionDenied

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


class TransactionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    serializer_class = TransactionLogSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return TransactionLog.objects.all().order_by('-date')
        elif self.request.user.is_authenticated:
            return TransactionLog.objects.filter(user=self.request.user).order_by('-date')
        else:
            return TransactionLog.objects.none()

@api_view(['PUT', 'POST', 'GET'])
@permission_classes((AllowAny, ))
def AddFundsView(request, amount, user=None):
    """
    Add Funds to an account. Respects the no_logs of the receiving user.
    If no username provided and user authed, funds will be added to own account
    Returns the new account balance
    """
    if request.user.is_authenticated and user is None:
        user = request.user
    else:
        try:
            acc = Account.objects.get(id=int(user))
        except ValueError:  # user wasnt a account id
            user = User.objects.get(username=user)
            acc = user.account
    amount = float(amount)

    acc.addFunds(amount,
                 ip=request.META.get('REMOTE_ADDR'),
                 user_authed=request.user.is_authenticated,
                 user_doing=request.user
                 )
    acc.save()
    return Response(acc.balance)

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes((AllowAny, ))
def BuyItemView(request, user_id, item_slug, item_amount=1):
    # this may throw errors if user isnt authed.
    if user is not None:
        user = User.objects.get(id=int(user_id))
    else:
        user = request.user
    user_doing = request.user or None
    item = Item.objects.get(slug=item_slug)
    amount = int(item_amount)
    pin = request.data.get('pin', False)
    acc = user.account

    if user == user_doing:
        # we buy for ourselves, no further checks neeeded
        acc.buyItem(item, amount, request.META.get('REMOTE_ADDR'), user_doing)
    else:
        #all other cases
        if acc.free_access:
            comment = "Free access, no auth needed"
        elif pin and acc.check_pin(pin):
            comment = "Legitimated by PIN"
        elif user_doing.is_staff:
            comment = "Legitimated by admin privileges"
        else:
            raise PermissionDenied
    acc.buyItem(item, amount, request.META.get('REMOTE_ADDR'), user_doing, comment)
    acc.save()
    return Response(acc)

