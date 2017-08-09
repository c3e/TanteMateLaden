from requests import get
from django.core.files.base import ContentFile
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

    def save(self, commit=True):
        m = super(AccountForm, self).save(commit=False)
        if len(self.cleaned_data['avatar_url']) > 5:
            img_file = ContentFile(get(self.cleaned_data['avatar_url']).content)
            m.avatar.save(m.user.username +".download", img_file)

        return m