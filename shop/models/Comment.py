from django.db import models
from django.conf import settings
from .Product import Product

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    body = models.TextField("متن نظر")
    rating = models.PositiveSmallIntegerField("امتیاز", null=True, blank=True)
    is_verified_buyer = models.BooleanField(default=False, verbose_name="خریدار تایید شده")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.product}"
