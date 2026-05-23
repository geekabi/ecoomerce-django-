# shop/cart.py

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, variant, qty=1, override_qty=False):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {
                'qty': 0,
                'price': str(variant.price),   # حتماً رشته ذخیره کن چون session فقط json درمیاد
                'title': variant.product.name,
                'image': (
                variant.product.primary_image.url
                if variant.product.primary_image
                else ""
)

            }
        if override_qty:
            self.cart[variant_id]['qty'] = qty
        else:
            self.cart[variant_id]['qty'] += qty
        self.save()

    def remove(self, variant):
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        from .models import ProductVariant
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        for v in variants:
            item = self.cart[str(v.id)]
            item['variant'] = v
            item['total_price'] = int(item['qty']) * int(float(item['price']))
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['qty']) * int(float(item['price'])) for item in self.cart.values())
