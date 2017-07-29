from django import template
from store.models import Drink

register = template.Library()

@register.inclusion_tag('store/widgets/drink_list.html')
def simple_drink_list():
	drinks = Drink.objects.all()
	return {'drinks': drinks}

@register.inclusion_tag('store/widgets/drink_row.html')
def drink_row():
	drinks = Drink.objects.all()
	return {'drinks': drinks}