"""bankservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from bankservice import views as service
from shop import views as shop

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', service.homepage, name="homepage"),
    path('signup', service.signup),
    path('signupp', service.signuppage),
    path('login', service.login),
    path('logout', service.logout),
    path('account', service.account, name='myaccount'),
    path('deposit', service.deposit, name='deposit'),
    path('transferpage', service.transferpage, name="mytransfer"),
    path('transfer', service.transfer, name='transfer'),
    path('confirmwallet', service.confirmWallet, name='confirmwallet'),
    path('comfirm_add', service.comfirmAdd, name='comfirm_add'),
    path('history', service.history, name='history'),
    
    path('shop', shop.shop_main, name='shop'),
    path('payment', shop.paymentmethod, name='payment'),
    path('AddWallet', shop.AddWallet, name='addwallet'),
    path('buynow', shop.buy_now, name='buy_now'),
    
    path('jordan_red', shop.jordan_red, name="jordan_red"),
    path('bag', shop.bag, name="bag"),
    path('bag2', shop.bag2, name="bag2"),
    path('shoes', shop.shoes, name="shoes"),
]
