from myapp import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('products/',views.products,name='products'),
    path('single/<int:pid>/',views.single,name='single'),
    path('about/',views.about,name='about'),
    path('add-to-cart/<int:pid>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('UpdateCartQty/',views.UpdateCartQty,name='UpdateCartQty'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('search/',views.search,name='search'),
    path('remove/',views.remove,name='remove'),
    path('logout/',views.logout,name='logout'),
    path('contact/',views.contact,name='contact'),

]