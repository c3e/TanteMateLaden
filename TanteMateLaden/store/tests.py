from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Account, TransactionLog, Item
from collections import OrderedDict
from django.dispatch import receiver
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory, APITestCase
from rest_framework import status

# Create your tests here.
class BasicAccountTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        Item.objects.create(name="Item #1", slug="item-1", creating_user=user, last_update_user=user)
        Item.objects.create(name="Item #2", slug="item-2", creating_user=user, last_update_user=user)

    def test_addingFunds(self):
        user = User.objects.get(username="testuser")
        account = user.account
        account.no_logs = True

        # add 10 currency
        account.addFunds(10, user_doing=user)
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

        # add funds as str
        account.addFunds("15")
        self.assertEqual(account.balance, 10.0)

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


class BasicAPITests(APITestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        useracc = user.account
        useracc.free_access = True
        useracc.save()
        admin = User.objects.create(username="admin", is_staff=True, is_superuser=True)
        Item.objects.create(name="Item #1", slug="item-1", creating_user=user, last_update_user=user)
        Item.objects.create(name="Item #2", slug="item-2", creating_user=user, last_update_user=user)

    def test_getAccounts(self):
        url = reverse('account-list')
        response = self.client.get(url, {}, format='json')
        data = [OrderedDict([('id', 2), ('user', 'admin'), ('avatar', None), ('balance', '0.00'), ('free_access', False)]),
                OrderedDict([('id', 1), ('user', 'testuser'), ('avatar', None), ('balance', '0.00'), ('free_access', True)])]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_getItems(self):
        url = reverse('item-list')
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)

    def test_getLogs(self):
        url = reverse('transactionlog-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_buyItemFreeAccess(self):
        url = reverse('buy-item', kwargs={'user_id': 1, 'item_slug': 'item-1', 'item_amount': 1})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, Decimal))

    def test_buyItemNoAccess(self):
        url = reverse('buy-item', kwargs={'user_id': 2, 'item_slug': 'item-1', 'item_amount': 1})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, 403)
