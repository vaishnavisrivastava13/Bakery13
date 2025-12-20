from django.contrib import admin
from .models import Dessert

@admin.register(Dessert)
class DessertAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'is_best_seller')
    list_filter = ('is_best_seller',)
    search_fields = ('name',)
