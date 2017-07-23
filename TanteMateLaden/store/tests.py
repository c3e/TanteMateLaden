from django.test import TestCase
from .models import Account, TransactionLog, Item
from django.contrib.auth.models import User


# Create your tests here.
class BasicAccountTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        Item.objects.create(name="Item #1", creating_user=user, last_update_user=user)
        Item.objects.create(name="Item #2", creating_user=user, last_update_user=user)

    def test_addingFunds(self):
        user = User.objects.get(username="testuser")
        account = user.account
        account.no_logs = True

        # add 10 currency
        account.addFunds(10)
        self.assertEqual(account.balance, 10)

        # check there are no logs yet.
        self.assertEqual(TransactionLog.objects.filter(user=user).count(), 0)

        # start logging of transactions
        account.no_logs = False

        # add non numeric value
        self.assertRaises(TypeError, account.addFunds, '";-- Little Bobby Tables')

        # add negative funds
        account.addFunds(-15)
        self.assertEqual(account.balance, -5)

        # check there is one log now
        self.assertEqual(TransactionLog.objects.filter(user=user).count(), 1)

    def test_BuyItem(self):
        user = User.objects.get(username="testuser")
        account = user.account
        account.addFunds(3)

        # buy a item by id
        account.buyItem(1)
        self.assertEqual(account.balance, 1.5)

        # buy 2 items by item object
        item = Item.objects.get(name="Item #2")
        account.buyItem(item, 2)
        self.assertEqual(account.balance, -1.5)

    def test_pin(self):
        user = User.objects.get(username="testuser")
        account = user.account
        account.set_pin("1234")
        self.assertIsNot("1234", account.pin)

        self.assertTrue(account.check_pin("1234"))
        self.assertFalse(account.check_pin("123"))
        self.assertFalse(account.check_pin("12356"))
