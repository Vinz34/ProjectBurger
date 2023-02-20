from django.contrib import admin

# Register your models here.
from .models import BurgerOrder
admin.site.register(BurgerOrder)