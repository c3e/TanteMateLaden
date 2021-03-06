from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal, InvalidOperation


class Account(models.Model):
    """
    Extends the default user model with specific foo
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads/avatars/", blank=True, null=True)
    free_access = models.BooleanField("Zugriff ohne Authentifizierung", default=False)
    no_logs = models.BooleanField("Keine Logs", default=False)
    pin = models.CharField("Optional Pin", max_length=64, blank=True, null=True)
    balance = models.DecimalField("Guthaben in Euro", max_digits=5, decimal_places=2, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s account (balance: %s)" % (self.user.username, self.balance)

    def addFunds(self, amount=0, ip=None, user_doing=None, comment="Aufladung"):
        """
        add funds to the account, negative values are allowed.
        """

        if isinstance(amount, (int, float, str)):
            try:
                amount = Decimal(amount)
            except InvalidOperation:
                raise TypeError
            if (not self.no_logs) or (user_doing is None) or (self.user != user_doing):
                log = TransactionLog.objects.create(user=self.user, balance_change=amount, ip=ip,
                                                    user_doing=user_doing, comment=comment)
            self.balance += amount
            return True
        else:
            raise TypeError

    def buyItem(self, item, amount=1, ip=None, user_doing=None, comment=None):
        """
        Buys an item(Object or id) w/ the account, changes the balance accordingly and creates a log entry if wished.models
        returns the new Balance if successful.
        """
        if isinstance(item, int):
            # get Item instance if id was given
            item = Item.objects.get(id=item)
        if isinstance(item, Item):
            if not isinstance(user_doing, User):
                user_doing = None  # Anonymous User
            if (not self.no_logs) or (user_doing is None) or (self.user != user_doing):
                log = TransactionLog.objects.create(user=self.user, balance_change=item.price*-1, ip=ip,
                                                    user_doing=user_doing, comment=comment,
                                                    item=item, item_amount=amount)
            self.balance -= item.price * amount
            return self.balance
        else:
            raise TypeError

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        """
        Returns a boolean of whether the raw_pin was correct. Handles
        hashing formats behind the scenes.
        Basically a copy of the check_password function from the User model
        """

        def setter(raw_pin):
            """
            Incase we need to update the hash and the pin was valid
            """
            self.set_pin(raw_pin)
            self.save(update_fields=["pin"])

        return check_password(raw_pin, self.pin, setter)

    def last_day(self):
        now = timezone.now()
        transactions = self.user.transactionlog_set.filter(date__year=now.year,
                         date__month=now.month,
                         date__day=now.day)
        items = transactions.exclude(item=None)
        drinks = transactions.exclude(item__drink=None)
        money_spend = items.aggregate(models.Sum('balance_change'))['balance_change__sum']
        drinks = {'transactions': drinks}
        drinks['volume'] = drinks['transactions'].aggregate(models.Sum('item__drink__volume'))['item__drink__volume__sum']
        drinks['caffeine'] = drinks['transactions'].aggregate(caffeine=models.Sum(models.F('item__drink__volume')*models.F('item__drink__caffeine')))['caffeine']

        return {'transactions': transactions, 'spend': money_spend, 'drinks':drinks}




# hook to the create/save methods of auth.models.User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()


class Item(models.Model):
    """
    Generic base class for all kinds of items
    """
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="uploads/products/", blank=True)
    ean = models.CharField(max_length=13, blank=True, null=True)  # European Article Number (EAN)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)  # price in euro
    slug = models.SlugField(max_length=64, unique=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    creating_user = models.ForeignKey(User, related_name="creator")

    last_update = models.DateTimeField(auto_now=True)
    last_update_user = models.ForeignKey(User, related_name="updater")

    def __str__(self):
        return self.name


class Drink(Item):
    volume = models.DecimalField("Menge in l", max_digits=4, decimal_places=2)
    alcohol = models.DecimalField("Alkoholgehalt in %", max_digits=3, decimal_places=1, null=True)  # null or % of alcohol
    caffeine = models.IntegerField("Koffeingehalt in mg/l", null=True)  # caffeine in mg/l

    def __str__(self):
        return "%sl %s" % (self.volume, self.name)

class TransactionLog(models.Model):
    """
    Transaction log entry
    """
    user = models.ForeignKey(User)
    user_doing = models.ForeignKey(User, related_name="transactions_did", blank=True, null=True)
    balance_change = models.DecimalField("Guthabenänderung in Euro", max_digits=5, decimal_places=2, default=0)
    item = models.ForeignKey(Item, blank=True, null=True, default=None)
    item_amount = models.IntegerField(blank=True, null=True, default=None)
    comment = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)