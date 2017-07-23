from django.contrib import admin

# Register your models here.
from .models import Drink


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "volume", "alcoholic", "caffeine")
    prepopulated_fields = {"slug": ("name", "volume")}
