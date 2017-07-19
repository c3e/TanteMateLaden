from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    """
    Extends the default user model with specific foo
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads/avatars/")
    free_access = models.BooleanField("Zugriff ohne Authentifizierung", default=False)
    no_logs = models.BooleanField("Keine Logs", default=False)
    pin = models.CharField("Optional Pin", max_length=64)
    balance = models.DecimalField("Guthaben in Euro",max_digits=5, decimal_places=2, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

# hook to the create/save methods of auth.models.User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()


class TransactionLog(models.Model):
    """
    Transaction log entry
    """
    user = models.ForeignKey(User)
    balance_change = models.DecimalField("Guthabenänderung in Euro",max_digits=5, decimal_places=2)
    user_authed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
