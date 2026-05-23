from django.contrib import admin
from .models.Category import Category
from .models.Comment import Comment
from .models.Product import (
    Product,
    ProductImage,
    ProductVariant,
    Attribute,
    AttributeValue,
    VariantAttribute
)
admin.site.register(Comment)
admin.site.register(Category)
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value", "slug")
    list_filter = ("attribute",)
    prepopulated_fields = {"slug": ("value",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class VariantAttributeInline(admin.TabularInline):
    model = VariantAttribute
    extra = 1

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "sku", "price", "stock", "is_active")
    list_filter = ("is_active", "product")
    search_fields = ("sku",)
    inlines = [VariantAttributeInline]

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProductImageInline,
        ProductVariantInline,
    ]
