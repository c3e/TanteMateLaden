from requests import get
from PIL import Image
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
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

    def clean_avatar(self):
        cleaned_data = self.cleaned_data['avatar']
        if cleaned_data not in [None, False]:
            if cleaned_data.size > 5242880:  #8MB
                raise ValidationError("Bild zu groß (>8MB", 'FILE_TO_LARGE')
        return cleaned_data

    def clean(self):
        #run the standard clean method first
        cleaned_data = super(AccountForm, self).clean()
        if cleaned_data['avatar_url'] is not "":
            print(cleaned_data['avatar'])
            img_file = ContentFile(get(self.cleaned_data['avatar_url']).content)
            try:
                img = Image.open(img_file)
                avatar = cleaned_data['avatar']
                avatar.save("downloaded_avatar", img_file, save=False)
                self.clean_avatar()
            except OSError:
                #linked url looks not like an image
                raise ValidationError('URL ist kein Bild', 'URL_NO_IMAGE')
            except AttributeError:
                raise ValidationError('Erst einmalig ein Bild uploaden', 'NO_PREV_IMAGE')
        return cleaned_data
