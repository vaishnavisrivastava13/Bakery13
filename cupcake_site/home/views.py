import requests
import random
import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import Profile
from beverages.models import Beverage
from dessert.models import Dessert
from cupcakes.models import Cupcake
from cakes.models import Cake
from gift.models import Gift


# =========================
# HOME PAGE
# =========================
def home_page(request):
    return render(request, 'home.html', {'active_menu': 'home'})


# =========================
# SEARCH (GLOBAL SEARCH)
# =========================
def search(request):
    query = request.GET.get('q')

    beverages = []
    desserts = []
    cupcakes = []
    cakes = []
    gifts = []

    if query:
        beverages = Beverage.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        desserts = Dessert.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        cupcakes = Cupcake.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        cakes = Cake.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        gifts = Gift.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'search_results.html', {
        'query': query,
        'beverages': beverages,
        'desserts': desserts,
        'cupcakes': cupcakes,
        'cakes': cakes,
        'gifts': gifts,
    })



# SIGNUP
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # PASSWORD CHECK
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # USER EXISTS CHECK
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        # CREATE USER
        User.objects.create_user(
            username=username,
            password=password
        )

        # AUTHENTICATE & LOGIN
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Account created successful 🎉")

        # REDIRECT TO HOME
        return redirect("home")

    return render(request, "signup.html")
# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {username} 🍰")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


# =========================
# SAVE LOCATION
# =========================
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


# =========================
# FORGOT PASSWORD
# =========================
def forgot_password(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        try:
            profile = Profile.objects.get(phone=phone)
            user = profile.user

            otp = random.randint(100000, 999999)

            request.session['reset_otp'] = otp
            request.session['reset_user'] = user.id
            request.session['otp_time'] = time.time()

            print(f"OTP for {phone} is:", otp)

            return redirect('verify_otp')

        except Profile.DoesNotExist:
            messages.error(request, "Phone number not registered")

    return render(request, 'forgot_password.html')


# =========================
# VERIFY OTP
# =========================
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('password')

        stored_otp = request.session.get('reset_otp')
        otp_time = request.session.get('otp_time')

        if not stored_otp or not otp_time:
            messages.error(request, "OTP expired. Please try again.")
            return redirect('forgot_password')

        if time.time() - otp_time > 120:
            request.session.flush()
            messages.error(request, "OTP expired. Please generate a new one.")
            return redirect('forgot_password')

        if entered_otp and int(entered_otp) == stored_otp:
            user = User.objects.get(id=request.session.get('reset_user'))
            user.password = make_password(new_password)
            user.save()

            request.session.flush()

            messages.success(request, "Password reset successful. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_otp.html')
