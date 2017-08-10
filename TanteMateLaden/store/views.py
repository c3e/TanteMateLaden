from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from .models import Account, Drink, Item, TransactionLog
from .forms import AccountForm, UserForm, PinChangeForm
from .serializer import AccountSerializer, DrinkSerializer, ItemSerializer, TransactionLogSerializer
from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.http import Http404
from django.shortcuts import render, redirect

# REST API VIEWS


@permission_classes((DjangoModelPermissionsOrAnonReadOnly,))
class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-creation_date')
    serializer_class = AccountSerializer

    def create(self, request):
        user = User(username=request.data.get('username'))
        user.set_password(request.data.get('password'))
        user.save()
        return user.account

    @detail_route(methods=['post', 'get'], url_path='add/funds/(?P<amount>[0-9.]+)', permission_classes=[AllowAny])
    def AddFunds(self, request, amount, pk=None):
        """
        Add Funds to an account. Respects the no_logs of the receiving user.
        If no username provided and user authed, funds will be added to own account
        Returns the new account balance
        """
        try:
            acc = Account.objects.get(pk=int(pk))
        except ValueError:  # wasnt a account id
            user = User.objects.get(username=user)
            acc = user.account
        amount = float(amount)

        acc.addFunds(amount,
                     ip=request.META.get('REMOTE_ADDR'),
                     user_doing=request.user
                     )
        acc.save()
        return Response({'balance': acc.balance})


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


@api_view(['POST', 'GET', 'PUT', 'PATCH'])
@permission_classes((AllowAny,))
def BuyItemView(request, item_slug, user_id=None, item_amount=1):
    # this may throw errors if user isnt authed.
    if user_id is not None:
        user = User.objects.get(id=int(user_id))
    else:
        user = request.user
    user_doing = request.user or None
    item = Item.objects.get(slug=item_slug)
    amount = int(item_amount)
    pin = request.query_params.get('pin', False)
    acc = user.account

    if user == user_doing:
        # we buy for ourselves, no further checks neeeded
        acc.buyItem(item, amount, request.META.get('REMOTE_ADDR'), user_doing)
    else:
        # all other cases
        if acc.free_access:
            comment = "Free access, no auth needed"
        elif pin and acc.check_pin(pin):
            comment = "Legitimated by PIN"
        elif user_doing.is_staff:
            comment = "Legitimated by admin privileges"
        else:
            raise PermissionDenied
        acc.buyItem(item, amount, request.META.get(
            'REMOTE_ADDR'), user_doing, comment)
    acc.save()
    return Response({'balance': acc.balance, 'user': acc.user.username, 'item': item.name}, status.HTTP_202_ACCEPTED)


def templateView(request):
    """ just the empty layout template for development"""
    return render(request, 'layout.html')


def signup(request):
    """ register a new account, auth him and return to / """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def indexView(request):
    """right now just the empty layout template"""
    return render(request, 'layout.html')


def accountView(request):
    userform = UserForm(instance=request.user, prefix="user")
    accountform = AccountForm(instance=request.user.account, prefix="acc")
    pwform = PasswordChangeForm(request.user, prefix="pw")
    pinform = PinChangeForm(prefix="pin")
    if request.method == 'POST':
        if 'user-username' in request.POST:
            userform = UserForm(request.POST, instance=request.user, prefix="user")
            accountform = AccountForm(request.POST, request.FILES, instance=request.user.account, prefix="acc")
            pinform = PinChangeForm(request.POST, prefix="pin")
            if userform.has_changed() and userform.is_valid():
                userform.save()
            if accountform.has_changed() and accountform.is_valid():
                accountform.save()
                messages.success(request, 'Benutzerprofil aktualisiert')
            if pinform.has_changed() and pinform.is_valid():
                pin = pinform.cleaned_data['pin']
                request.user.account.set_pin(pin)
                messages.success(request, 'Neuer Pin gespeichert')
        else:
            pwform = PasswordChangeForm(request.user,request.POST, prefix="pw")
            if pwform.is_valid():
                pwform.save()
                messages.success(request, 'Neues Passwort gespeichert')

    # set balance read only
    accountform.fields['balance'].widget.attrs['readonly'] = True
    return render(request, 'store/account/index.html', {'userform': userform,
                                                        'accform': accountform,
                                                        'pwform': pwform,
                                                        'pinform': pinform})
