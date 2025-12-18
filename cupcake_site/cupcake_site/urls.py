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
from django.urls import path,include
from home.views import home_page,signup,save_location,login_view, logout_view,forgot_password,verify_otp
from beverages.views import beverages
from orders.views import order_page
from contact.views import contact_page
from cakes.views import cake_list,cake_detail
from cupcakes.views import cupcakes
from desert.views import desert
from gift.views import gift

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('forgot-password/',forgot_password, name='forgot_password'),
    path('verify-otp/',verify_otp, name='verify_otp'),
    path('logout/', logout_view, name='logout'),
    path('save-location/', save_location, name='save_location'),
    path('beverages/', beverages, name='beverages'),
    path('orders/', order_page, name='orders'),
    path('contact/', contact_page, name='contact'),
    path('cakes/', cake_list, name='cakes'),
    path('<int:id>/', cake_detail, name='cake_detail'),
    path('cupcakes/', cupcakes, name='cupcakes'),
    path('desert/', desert, name='desert'),
    path('gift/', gift, name='gift'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
