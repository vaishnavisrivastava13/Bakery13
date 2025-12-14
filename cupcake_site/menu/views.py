from django.shortcuts import render
from .models import MenuItem
# Create your views here.
def menu_page(request):
        return render(request, "menu.html")