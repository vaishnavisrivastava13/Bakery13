"""
URL configuration for cupcake_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from home.views import home_page, signup, save_location, login_view, logout_view, forgot_password, verify_otp, search
from beverages.views import beverages, beverage_detail
from orders.views import order_page
from contact.views import contact_page
from cakes.views import cake_list, cake_detail
from cupcakes.views import cupcakes, cupcake_detail
from dessert.views import dessert, dessert_detail
from gift.views import gift_list, gift_detail
from cart.views import add_to_cart, cart_page, remove_from_cart, save_address, update_cart, checkout, order_success

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_page, name='home'),

    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('logout/', logout_view, name='logout'),

    path('search/', search, name='search'),   # ✅ SEARCH URL

    path('save-location/', save_location, name='save_location'),

    path('beverages/', beverages, name='beverages'),
    path('beverages/<int:id>/', beverage_detail, name='beverage_detail'),

    path('orders/', order_page, name='orders'),
    path('contact/', contact_page, name='contact'),

    path('cakes/', cake_list, name='cakes'),
    path('cakes/<int:id>/', cake_detail, name='cake_detail'),

    path('cupcakes/', cupcakes, name='cupcakes'),
    path('cupcakes/<int:id>/', cupcake_detail, name='cupcake_detail'),

    path('dessert/', dessert, name='dessert'),
    path('dessert/<int:id>/', dessert_detail, name='dessert_detail'),

    path('gifts/', gift_list, name='gift'),
    path('gifts/<int:id>/', gift_detail, name='gift_detail'),

    path('cart/', cart_page, name='cart'),
    path('cart/add/<str:model_name>/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/save-address/', save_address, name='save_address'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
