from django.shortcuts import render, redirect
from .models import Address, Order, OrderItem
from shop.cart import Cart
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from .models import Order, OrderItem
from shop.models import ProductVariant
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from zarinpal import ZarinPal
from zarinpal import Config

from .models import Order

@login_required
def checkout_step1(request):

    cart = request.session.get("cart", {})
    cart_items = []
    total_price = Decimal("0")

    # ساخت آیتم‌های سبد
    for variant_id, item in cart.items():

        if isinstance(item, dict):
            qty = item.get("qty", 1)
        else:
            qty = item

        try:
            variant = ProductVariant.objects.get(id=int(variant_id))
        except ProductVariant.DoesNotExist:
            continue

        item_total = variant.price * qty
        total_price += item_total

        cart_items.append({
            "variant": variant,
            "quantity": qty,
            "total_price": item_total,
        })

    # آدرس‌های کاربر
    addresses = request.user.addresses.order_by("-is_default", "-id")

    if request.method == "POST":

        address_id = request.POST.get("address_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if not address_id:
            return render(request, "orders/checkout_step1.html", {
                "addresses": addresses,
                "cart_items": cart_items,
                "total_price": total_price,
                "error": "لطفا یک آدرس انتخاب کنید"
            })

        address = get_object_or_404(Address, id=address_id, user=request.user)

        with transaction.atomic():
            user = request.user
            if not user.profile.full_name:
                user.profile.full_name = f"{first_name} {last_name}"
                user.profile.save()


            order = Order.objects.create(
                user=request.user,
                address=address,
                total_price=total_price,
                status="pending",
            )

            for item in cart_items:

                variant = item["variant"]  
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    quantity=quantity,
                    price=variant.price
                )

        # پاک کردن سبد
        request.session["cart"] = {}
        request.session.modified = True

        return redirect("orders:select_shipping", order.id)

    return render(request, "orders/checkout_step1.html", {
        "addresses": addresses,
        "cart_items": cart_items,
        "total_price": total_price,
        "user": request.user,
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects
        .prefetch_related("items", "items__variant", "items__variant__product", "items__variant__product__images"),
        id=order_id,
        user=request.user
    )
    order.auto_fail_if_expired()
    return render(request, "orders/order_detail.html", {"order": order})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Order

@login_required
def order_payment(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    # اگر سفارش قبلاً پرداخت شده، می‌توانی به جزئیات سفارش برگردانی
    if order.status == "paid":
        return redirect("orders:order_detail", pk=order.pk)

    # فعلاً فقط نمایش روش‌های پرداخت؛ بعداً اینجا اتصال به درگاه را اضافه می‌کنی
    return render(request, "orders/order_payment.html", {
        "order": order,
    })




def zarinpal_start_payment(request, pk):

    order = get_object_or_404(Order, pk=pk)

    config = Config(
        merchant_id=settings.ZARINPAL_MERCHANT,
        sandbox=settings.ZARINPAL_SANDBOX,
    )

    zarinpal = ZarinPal(config)

    callback_url = request.build_absolute_uri('/orders/payment/callback/')

    response = zarinpal.payments.create({
        "amount":int(order.total_price)*10,
        "callback_url": callback_url,
        "description": f"Order #{order.id}",
        "metadata": {
            "mobile": request.user.phone if hasattr(request.user,'phone') else ""
        }
    })

    if response['data']['code'] == 100:

        authority = response['data']['authority']
        order.zarinpal_authority = authority
        order.save()

        payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"

        return redirect(payment_url)

    return redirect("orders:order_detail", pk=order.pk)


from django.contrib import messages

def zarinpal_callback(request):

    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    order = get_object_or_404(Order, zarinpal_authority=authority)

    if order.status == "paid":
        messages.info(request, "این سفارش قبلاً پرداخت شده ✅")
        return redirect("orders:order_detail", order_id=order.id)

    if status == "OK":

        config = Config(
            merchant_id=settings.ZARINPAL_MERCHANT,
            sandbox=settings.ZARINPAL_SANDBOX,
        )

        zarinpal = ZarinPal(config)

        response = zarinpal.verifications.verify({
            "amount": int(order.total_price)*10,
            "authority": authority,
        })

        code = response['data']['code']

        if code == 100:

            order.status = "paid"
            order.zarinpal_ref_id = response['data']['ref_id']
            order.zarinpal_card_pan = response['data']['card_pan']
            order.save()

            messages.success(request,"پرداخت با موفقیت انجام شد")

        else:
            order.status = "pending"
            order.save()

            messages.error(request,"پرداخت تایید نشد")

    else:
        order.status = "pending"
        order.save()

        messages.error(request,"پرداخت لغو شد")

    return redirect("orders:order_detail", order_id=order.pk)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, ShippingMethod

def select_shipping(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # اگر سفارشی آدرس نداشت، اول بفرستش برای انتخاب آدرس
    if not order.address:
        return redirect('orders:select_address', order_id=order.id)

    if request.method == 'POST':
        shipping_id = request.POST.get('shipping_method')
        shipping_method = get_object_or_404(ShippingMethod, id=shipping_id, is_active=True)
        
        # آپدیت سفارش
        order.shipping_method = shipping_method
        order.shipping_price = shipping_method.price
        
        # محاسبه مجدد قیمت کل (قیمت کالاها + هزینه ارسال)
        # فرض بر این است که متدی برای محاسبه قیمت کالاها دارید
        order.update_total_price()
        
        order.save()
        
        return redirect('orders:order_detail', order_id=order.id)

    shipping_methods = ShippingMethod.objects.filter(is_active=True)
    return render(request, 'orders/select_shipping.html', {
        'order': order,
        'shipping_methods': shipping_methods
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order, Coupon, CouponUsage

def apply_coupon_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        try:
            coupon = Coupon.objects.get(code__iexact=code, is_active=True)
        except Coupon.DoesNotExist:
            messages.error(request, "کد تخفیف معتبر نیست.")
            return redirect("orders:order_detail", order.id)

        if not coupon.is_valid():
            messages.error(request, "این کوپن منقضی شده یا غیرفعال است.")
            return redirect("orders:order_detail", order.id)

        if CouponUsage.objects.filter(user=request.user, coupon=coupon).exists():
            messages.error(request, "شما قبلاً از این کوپن استفاده کرده‌اید.")
            return redirect("orders:order_detail", order.id)

        discount = int((order.products_total_price * coupon.discount_percent) / 100)

        order.coupon = coupon
        order.discount_amount = discount
        order.save()
        order.update_total_price()

        CouponUsage.objects.create(user=request.user, coupon=coupon)

        messages.success(request, "کوپن با موفقیت اعمال شد.")

    return redirect("orders:order_detail", order.id)


