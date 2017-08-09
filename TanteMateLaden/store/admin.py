from django.contrib import admin

# Register your models here.
from .models import Account, Drink

admin.site.register(Account)

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "volume", "alcoholic", "caffeine")
    prepopulated_fields = {"slug": ("name", "volume")}

