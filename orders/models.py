from django.db import models
from accounts.models import User,Address
from shop.models.Product import ProductVariant
from datetime import timedelta


class ShippingMethod(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان روش ارسال")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="هزینه ارسال")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return f"{self.title} ({self.price} تومان)"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('failed', 'لغو شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    zarinpal_authority = models.CharField(max_length=255,blank=True,null=True)
    zarinpal_ref_id = models.CharField(max_length=255,blank=True,null=True)
    zarinpal_card_pan = models.CharField(max_length=255,blank=True,null=True)

    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="روش ارسال")
    shipping_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="هزینه ارسال نهایی")
    coupon = models.ForeignKey(
    "Coupon",
    null=True,
    blank=True,
    on_delete=models.SET_NULL
                    )
    discount_amount = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return f"Order #{self.id} - {self.user.phone}"
    
    def update_total_price(self):
        items_total = sum(item.price * item.quantity for item in self.items.all())
        self.total_price = items_total + (self.shipping_price or 0) -  (self.discount_amount or 0)
        self.save()

    @property
    def products_total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())   

    @property
    def total_price_before_discount(self):
        return sum(item.price * item.quantity for item in self.items.all()) + (self.shipping_price or 0)
    

    def auto_fail_if_expired(self):
        if self.status == "pending":
            if timezone.now() > self.created_at + timedelta(minutes=15):
                self.status = "failed"
                self.save()
        


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=0)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.variant} - {self.quantity} عدد"
    

from django.db import models
from django.conf import settings
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField()  # مثلا 20 یعنی 20%
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        if not self.is_active:
            return False

        if self.expires_at and self.expires_at < timezone.now():
            return False

        return True

class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'coupon')

