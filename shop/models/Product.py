from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from common.models import BaseModel
from .Category import Category
from common.utils.date import to_jalali


class Product(BaseModel):

    name = models.CharField(max_length=200, verbose_name="نام محصول")

    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="دسته بندی"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.pk and not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})
    
    @property
    def jalali_created(self):
        return to_jalali(self.created_at)
    
    @property
    def primary_image(self):
        # سعی کن عکس اصلی را پیدا کنی، اگر نبود اولین عکس را برگردان
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image
        return self.images.first().image if self.images.exists() else None

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/")

    alt = models.CharField(max_length=200, blank=True)

    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} Image"


class Attribute(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="نام ویژگی"
    )

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"


class AttributeValue(models.Model):

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=100)

    slug = models.SlugField()

    def __str__(self):
        return f"{self.attribute.name} : {self.value}"

    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی"


class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    attributes = models.ManyToManyField(
        AttributeValue,
        through="VariantAttribute"
    )

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

class VariantAttribute(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE
    )
    value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE
    )

    class Meta:
        # یک واریانت نباید دو مقدار از یک "نوع ویژگی" (مثلاً دو رنگ) داشته باشد.
        # واریانت 123 | ویژگی رنگ | مقدار قرمز
        # واریانت 123 | ویژگی رنگ | مقدار آبی  <- این نباید ممکن باشد
        unique_together = ('variant', 'attribute') # این تضمین می‌کند که از هر ویژگی فقط یک مقدار برای هر واریانت ثبت شود
        verbose_name = "ویژگی واریانت"
        verbose_name_plural = "ویژگی‌های واریانت"

    def __str__(self):
        return f"{self.variant} - {self.attribute.name}:{self.value.value}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_attributes"
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("product", "attribute")

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"
