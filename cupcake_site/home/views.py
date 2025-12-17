from django.shortcuts import render
import requests
from django.http import JsonResponse
# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def save_location(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url).json()

    address = response.get('address', {})

    city = (
        address.get('city') or
        address.get('town') or
        address.get('village') or
        "Your Area"
    )

    request.session['user_location'] = city

    return JsonResponse({'city': city})