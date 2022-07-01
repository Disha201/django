from myapp.models import Cart, Order, OrderDetails, User
from django.contrib import admin

# Register your models here.

#admin.site.register(Cart)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['name','email','password']

@admin.register(Cart)
class UserAdmin(admin.ModelAdmin):
    list_display=['product','user','quantity']

@admin.register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display=['user','order_status']

@admin.register(OrderDetails)
class UserAdmin(admin.ModelAdmin):
    list_display=['product','quantity','order']