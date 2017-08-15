from django import template
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from store.models import Drink, Account, Item, TransactionLog

register = template.Library()

@register.inclusion_tag('store/widgets/drink_list.html')
def simple_drink_list():
    drinks = Drink.objects.all()
    return {'drinks': drinks}

@register.inclusion_tag('store/widgets/drink_row.html', takes_context=True)
def drink_row(context):
    drinks = Drink.objects.all()
    return {'drinks': drinks, 'request': context['request']}

@register.inclusion_tag('store/widgets/buy_modal.html', takes_context=True)
def buy_item_modal(context, item):
    user = context['request'].user
    accounts = Account.objects.filter(free_access=True) | Account.objects.exclude(pin=None)
    if not isinstance(user, AnonymousUser):
        accounts = accounts.exclude(user = user).order_by('user__username')
    return {'item': item, 'user': user, 'accounts': accounts}

@register.inclusion_tag('store/widgets/stats_sales.html')
def stats_sales(start_date=None, end_date=None, user=None, user_doing=None):
    item_sales = Item.objects
    if start_date is not None:
        item_sales = item_sales.filter(transactionlog__date__gte=start_date)
    if end_date is not None:
        item_sales = item_sales.filter(transactionlog__date__lte=end_date)
    if user is not None:
        item_sales = item_sales.filter(transactionlog__user = user)
    if user_doing is not None:
        item_sales = item_sales.exclude(transactionlog__user = user_doing)
    item_sales = item_sales.annotate(num_sales=Count('transactionlog'))

    item_sales = item_sales.exclude(num_sales=0).order_by('-num_sales')
    total_item_logs = item_sales.aggregate(total=Count('transactionlog'))['total']
    return {'sales': item_sales, 'total_item_sales': total_item_logs}

@register.inclusion_tag('store/widgets/stats_sales.html')
def stats_sales_today(user=None, user_doing=None):
    now = timezone.now()
    today = datetime(year=now.year, month=now.month, day=now.day)
    return stats_sales(start_date=today, user=user, user_doing=user_doing)

@register.inclusion_tag('store/widgets/stats_sales.html')
def stats_sales_last_week(user=None, user_doing=None):
    now = timezone.now()
    start = now - timedelta(days=7)
    return stats_sales(start_date=start, user=user, user_doing=user_doing)

@register.inclusion_tag('store/widgets/stats_sales.html')
def stats_sales_last_month(user=None, user_doing=None):
    now = timezone.now()
    start = now - timedelta(weeks=4)
    return stats_sales(start_date=start, user=user, user_doing=user_doing)