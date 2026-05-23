from django.contrib import admin
from .models import Order,ShippingMethod,Coupon

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at")



@admin.register(ShippingMethod)
class ShiippingMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price","is_active")   


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "is_active", "discount_percent","expires_at")     

