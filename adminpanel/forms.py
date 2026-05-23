from django import forms
from shop.models.Product import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows":4}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image", "alt", "is_primary"]


from django import forms
from shop.models.Category import Category
from mptt.forms import TreeNodeChoiceField

class CategoryForm(forms.ModelForm):

    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        required=False,
        level_indicator="— "
    )

    class Meta:
        model = Category
        fields = [
            "name",
            "parent",
            "image",
            "is_active",
            "order"
        ]
