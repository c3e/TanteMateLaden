from django.contrib.auth.models import User
from django.forms import ModelForm, URLField, PasswordInput, CharField, Form
from store.models import Account

class PinChangeForm(Form):
    pin = CharField(widget=PasswordInput(), required=False)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AccountForm(ModelForm):
    avatar_url = URLField(required=False)

    class Meta:
        model = Account
        fields = ['balance', 'free_access', 'no_logs', 'avatar']
