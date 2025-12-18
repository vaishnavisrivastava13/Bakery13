import requests
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Profile
import time


# HOME PAGE
def home_page(request):
    return render(request, 'home.html', {'active_menu': 'home'})



# =========================
# SIGNUP (PHONE NUMBER)
# =========================
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            password=password1
        )

        Profile.objects.create(
            user=user,
            phone=phone
        )

        messages.success(request, "Signup successful. Please login.")
        return redirect('login')

    return render(request, 'signup.html')


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
            messages.success(request, f"Welcome {username}")
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
# FORGOT PASSWORD (OTP)
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

            print(f"OTP for {phone} is:", otp)  # SMS later

            return redirect('verify_otp')

        except Profile.DoesNotExist:
            messages.error(request, "Phone number not registered")

    return render(request, 'forgot_password.html')

# =========================
# VERIFY OTP & RESET PASSWORD
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

        # check expiry (2 minutes = 120 seconds)
        if time.time() - otp_time > 120:
            request.session.flush()
            messages.error(request, "OTP expired. Please generate a new one.")
            return redirect('forgot_password')

        if entered_otp and int(entered_otp) == stored_otp:
            user = User.objects.get(id=request.session.get('reset_user'))
            user.password = make_password(new_password)
            user.save()

            # clear session after success
            request.session.flush()

            messages.success(request, "Password reset successful. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_otp.html')






