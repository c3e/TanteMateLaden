from django import template
from django.contrib.auth.models import AnonymousUser
from store.models import Drink, Account

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