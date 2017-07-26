"""TanteMateLaden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework import routers

# noinspection PyUnresolvedReferences
from store import views

from django.conf.urls import url, include
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'drinks', views.DrinkViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'transactions', views.TransactionLogViewSet, 'transactionlog')
router.register(r'buy', views.BuyItemView, 'buyitem')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/buy/item/(?P<item_slug>[\w-]+)/$', views.BuyItemView),
    url(r'^api/buy/item/(?P<item_slug>[\w-]+)/(?P<item_amount>[0-9]+)/$', views.BuyItemView),
    url(r'^api/buy/item/(?P<user_id>[0-9\w-]+)/(?P<item_slug>[\w-]+)/$', views.BuyItemView),
    url(r'^api/buy/item/(?P<user_id>[0-9\w-]+)/(?P<item_slug>[\w-]+)/(?P<item_amount>[0-9]+)/$', views.BuyItemView),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
