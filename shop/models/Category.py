from django.db import models
from django.utils.text import slugify
from common.models import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.urls import reverse


class Category(MPTTModel, BaseModel):

    name = models.CharField(max_length=150, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, blank=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='دسته والد'
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)

    @property
    def full_path(self):
        """
        pet-food/dog/dry-food
        """
        return "/".join(
            [c.slug for c in self.get_ancestors(include_self=True)]
        )

    def get_absolute_url(self):
        """
        /shop/category/pet-food/dog/dry-food/
        """
        return reverse(
            "shop:category_detail",
            kwargs={"path": self.full_path}
        )    
    
    @property
    def breadcrumb(self):
        return " / ".join([c.name for c in self.get_ancestors(include_self=True)])
