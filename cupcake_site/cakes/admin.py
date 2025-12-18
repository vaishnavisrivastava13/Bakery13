from django.contrib import admin
from .models import Cake

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'is_best_seller','description')
