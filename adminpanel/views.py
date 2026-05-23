from django.shortcuts import render
from shop.models.Product import Product,ProductImage
from django.shortcuts import render, redirect
from .forms import ProductForm, ProductImageForm
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from itertools import product as cartesian_product
from django.shortcuts import get_object_or_404, redirect, render
from shop.models.Product import (
    ProductVariant,
    Attribute,
    AttributeValue,
    VariantAttribute,
)



def dashboard(request):

    context = {
        "product_count": Product.objects.count()
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )

def product_list(request):

    products = Product.objects.all()

    return render(
        request,
        "adminpanel/products/list.html",
        {"products": products}
    )



def product_create(request):
    """
    ایجاد محصول جدید فقط اطلاعات پایه را ثبت می‌کند.
    پس از ذخیره، می‌توان تصاویر یا واریانت‌ها را اضافه کرد.
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()  # محصول جدید ساخته شد
            return redirect("adminpanel:product-update", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "adminpanel/products/form.html", {
        "form": form,
        "title": "افزودن محصول",
    })



def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1, can_delete=True)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=product.images.all())

        if form.is_valid() and formset.is_valid():
            form.save()

            # ذخیره فرم‌ست عکس‌ها
            images = formset.save(commit=False)
            for img in images:
                img.product = product
                img.save()
            # حذف‌هایی که انتخاب شده‌اند
            for deleted in formset.deleted_objects:
                deleted.delete()

            return redirect("adminpanel:products")

    else:
        form = ProductForm(instance=product)
        formset = ImageFormSet(queryset=product.images.all())

    return render(request, "adminpanel/products/product_update.html", {
        "form": form,
        "formset": formset,
        "title": f"ویرایش محصول: {product.name}",
        "product": product,
    })


import uuid  # برای تولید رشته تصادفی و منحصر به فرد
from django.utils.text import slugify

def product_variants(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    attributes = Attribute.objects.prefetch_related("values")
    print("METHOD:", request.method)
    print("POST:", request.POST)

    if request.method == "POST":
        
        selected_values = request.POST.getlist("values")
        value_objects = AttributeValue.objects.filter(id__in=selected_values)

        grouped = {}
        for v in value_objects:
            grouped.setdefault(v.attribute_id, []).append(v)

        combinations = cartesian_product(*grouped.values())

        for combo in combinations:
            # --- بخش جدید: تولید SKU منحصر به فرد ---
            # ترکیب نام محصول + شناسه‌های ویژگی + یک کد رندوم کوتاه
            attr_part = "-".join([str(v.id) for v in combo])
            random_suffix = uuid.uuid4().hex[:4].upper()
            new_sku = f"SKU-{product.id}-{attr_part}-{random_suffix}"
            # ---------------------------------------

            variant = ProductVariant.objects.create(
                product=product,
                price=0,
                stock=0,
                sku=new_sku  # مقدار SKU را اینجا پاس می‌دهیم
            )

            for val in combo:
                VariantAttribute.objects.create(
                    variant=variant,
                    attribute=val.attribute,
                    value=val,
                )

        return redirect("adminpanel:admin-product-variants", product.id)

    existing_variants = ProductVariant.objects.filter(product=product)

    return render(
        request,
        "adminpanel/products/product_variants.html",
        {
            "product": product,
            "attributes": attributes,
            "variants": existing_variants,
        },
    )

def variant_update(request, variant_id):
    print("METHOD:", request.method)
    print("POST DATA:", request.POST)

    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == "POST":
        variant.price = request.POST.get("price")
        variant.stock = request.POST.get("stock")
        variant.save()

    return render(
        request,
        "adminpanel/partials/variant_row.html",
        {"v": variant},
    )





from django.utils.text import slugify

def attribute_create(request):

    name = request.POST.get("name")

    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while Attribute.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    attr = Attribute.objects.create(
        name=name,
        slug=slug
    )

    return render(
        request,
        "adminpanel/products/attribute_card.html",
        {"attr": attr}
    )


def attribute_value_create(request, attr_id):

    attr = Attribute.objects.get(id=attr_id)

    value = request.POST.get("value")

    val = AttributeValue.objects.create(
        attribute=attr,
        value=value
    )

    return render(
        request,
        "adminpanel/products/value_item.html",
        {"val": val}
    )

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["DELETE"])
def variant_delete(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    variant.delete()
    return HttpResponse(status=204)  # بدون محتوا، HTMX خودش ردیف را حذف می‌کند

from shop.models.Category import Category
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_categories_list(request):
    categories = Category.objects.all().order_by("tree_id", "lft")

    return render(request, "adminpanel/products/categories_list.html", {
        "categories": categories
    })

from  .forms import CategoryForm

@staff_member_required
def admin_category_create(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("adminpanel:categories-list")

    return render(request, "adminpanel/products/category_form.html", {
        "form": form,
        "title": "افزودن دسته جدید"
    })

@staff_member_required
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    form = CategoryForm(
        request.POST or None,
        request.FILES or None,
        instance=category
    )

    if form.is_valid():
        form.save()
        return redirect("adminpanel:categories-list")

    return render(request, "adminpanel/products/category_form.html", {
        "form": form,
        "title": "ویرایش دسته"
    })


from orders.models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def admin_orders_list(request):

    orders = Order.objects.select_related(
        "user",
        "shipping_method"
    ).order_by("-created_at")

    return render(request, "adminpanel/orders_list.html", {
        "orders": orders
    })

from django.shortcuts import get_object_or_404
from orders.models import OrderItem

@staff_member_required
def admin_order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related("user", "shipping_method", "address"),
        id=order_id
    )

    items = OrderItem.objects.select_related(
        "variant",
        "variant__product"
    ).filter(order=order)

    return render(request, "adminpanel/order_detail.html", {
        "order": order,
        "items": items
    })
