from django.db import models

from django.contrib.auth.models import User


class Account(models.Model):
    """
    Extends the default user model with specific foo
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads/avatars/")
    free_access = models.BooleanField("Zugriff ohne Authentifizierung")
    no_logs = models.BooleanField("Keine Logs")
    pin = models.CharField("Optional Pin", max_length=64)
    balance = models.DecimalField("Guthaben in Euro",max_digits=5, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class TransactionLog(models.Model):
    """
    Transaction log entry
    """
    user = models.ForeignKey(User)
    balance_change = models.DecimalField("Guthabenänderung in Euro",max_digits=5, decimal_places=2)
    user_authed = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
