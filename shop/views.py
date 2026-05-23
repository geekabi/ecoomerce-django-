# shop/views.py
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models.Category import Category
from .models.Product import Product,ProductVariant   # فرض بر اینکه Product را داری/خواهی ساخت
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .cart import Cart


class CategoryDetailView(ListView):
    model = Product
    template_name = "shop/category_detail.html"
    context_object_name = "products"
    paginate_by = 20  # دلخواه، برای صفحه‌بندی

    def dispatch(self, request, *args, **kwargs):
        # در اینجا category را پیدا می‌کنیم و در self.category ذخیره می‌کنیم
        self.category = self.get_category_from_path()
        return super().dispatch(request, *args, **kwargs)

    def get_category_from_path(self):
        """
        path = "pet-food/dog/dry-food"
        """

        path = self.kwargs.get("path", "").strip("/")
        if not path:
            raise Http404("Category path is empty")

        slugs = path.split("/")  # ['pet-food', 'dog', 'dry-food']

        # قدم اول: دسته سطح ریشه با slug اول
        qs = Category.objects.filter(parent__isnull=True)
        category = get_object_or_404(qs, slug=slugs[0])

        # قدم‌های بعدی: هر سطح را در فرزندان قبلی پیدا کن
        for slug in slugs[1:]:
            category = get_object_or_404(
                category.children.all(),
                slug=slug
            )

        return category

    def get_queryset(self):
        """
        محصولات همه زیرشاخه‌ها + خود دسته
        """
        # تمام نوادگان + خود دسته
        categories = self.category.get_descendants(include_self=True)
        return Product.objects.filter(
            category__in=categories,
            is_active=True  # اگر چنین فیلدی داری
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        ctx["breadcrumbs"] = self.category.get_ancestors(include_self=True)
        return ctx


# shop/views.py



def home(request):

    products = Product.objects.filter(is_active=True)[:8]

    return render(request, "shop/home.html", {
        "products": products
    })



def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)
    comments = product.comments.filter(
    is_approved=True,
    parent__isnull=True
            ).select_related("user").prefetch_related("replies")


    variants = (
        ProductVariant.objects
        .filter(product=product)
        .prefetch_related("variantattribute_set__value__attribute")
    )

    context = {
        "product": product,
        "variants": variants,
        "comments": comments
    }

    return render(request, "shop/product_detail.html", context)




# shop/views.py

def cart_add(request): # دیگر variant_id را در ورودی URL نمی‌گیریم
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id') # گرفتن ID از رادیو باتن
        qty = int(request.POST.get('qty', 1))
        
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart = Cart(request)
        cart.add(variant=variant, qty=qty)
        
        return redirect('shop:cart_detail')



def cart_remove(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart = Cart(request)
    cart.remove(variant)
    return redirect('shop:cart_detail')


from django.views.decorators.http import require_GET

@require_GET
def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"cart": cart})


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from shop.models import Product
from orders.models import OrderItem
from shop.models.Comment import Comment


@login_required
def add_comment(request, product_id):
    if request.method != "POST":
        return redirect("products:product_detail", product_id)

    product = get_object_or_404(Product, id=product_id)

    body = request.POST.get("body")
    rating = request.POST.get("rating")
    parent_id = request.POST.get("parent_id")

    if not body.strip():
        messages.error(request, "متن کامنت نمی‌تواند خالی باشد.")
        return redirect("products:product_detail", product_id)

    # تعیین والد برای پاسخ به کامنت
    parent = None
    if parent_id:
        parent = Comment.objects.filter(
            id=parent_id,
            product=product,
            is_approved=True,
        ).first()

    # تشخیص آیا کاربر واقعا این محصول رو خریده؟
    is_verified_buyer = OrderItem.objects.filter(
        order__user=request.user,
        order__status="paid",
        variant__product=product
    ).exists()

    # ساخت کامنت
    Comment.objects.create(
        product=product,
        user=request.user,
        body=body,
        rating=rating if rating else None,
        parent=parent,
        is_verified_buyer=is_verified_buyer,
        is_approved=False,  # اگر می‌خواهی بدون تایید نمایش داده شود True کن
    )

    messages.success(request, "نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده می‌شود.")

    return redirect("shop:product-detail", slug=product.slug)
