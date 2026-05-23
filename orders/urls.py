# orders/urls.py

from django.urls import path
from . import views # ویوهای مربوط به اپ orders را اینجا import می‌کنیم

app_name = 'orders' # این نام برای استفاده در reverse lookup ضروری است

urlpatterns = [
    # مسیرهای مربوط به checkout
    path('checkout/step1/', views.checkout_step1, name='checkout_step1'),
    
    # مسیر نمایش جزئیات سفارش
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path("order/<int:pk>/payment/", views.order_payment, name="order_payment"),
    path('payment/<int:pk>/', views.zarinpal_start_payment, name='zarinpal_start_payment'),
    path('payment/callback/', views.zarinpal_callback, name='zarinpal_callback'),
    path('<int:order_id>/shipping/', views.select_shipping, name='select_shipping'), 
    path('order/<int:order_id>/apply-coupon/', views.apply_coupon_view, name='apply_coupon'),
    
   
    
    # مسیر پرداخت (اگر جداگانه تعریف کنیم)
    # path('payment/<int:order_id>/', views.payment_view, name='payment'),
    
    # مسیرهای دیگر مربوط به سفارش‌ها (مثلاً لیست سفارشات کاربر)
    # path('my-orders/', views.my_orders_list, name='my_orders_list'),
]
