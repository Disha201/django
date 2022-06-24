from . import views
from django.urls import path

from django.contrib import admin


urlpatterns = [
    path('', views.index,name='index'),
    path('about/', views.about,name='about'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('register/', views.register,name='register'),
    path('products/', views.products,name='products'),
    path('single/<int:pid>', views.single,name='single'),
    path('add-to-cart/<int:pid>', views.add_to_cart,name='add-to-cart'),
    path('cart/', views.cart,name='cart'),
    path('updatecartqty/', views.updatecartqty,name='updatecartqty'),
    path('checkout/', views.checkout,name='checkout'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]