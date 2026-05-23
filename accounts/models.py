from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from common.utils.codes import generate_numeric_code

class UserManager(BaseUserManager):
    def create_user(self,phone,password=None, **extra_fields):
        if not phone:
           raise ValueError("شماره موبایل الزامی است.")

        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,phone,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="شماره موبایل"
    )

    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_staff = models.BooleanField(default=False, verbose_name="کارمند")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone 

class OTP(models.Model):

    phone = models.CharField(max_length=11, verbose_name="شماره موبایل")
    code = models.CharField(max_length=6, verbose_name="کد تایید")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_numeric_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone} - {self.code}"  

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="کاربر")
    full_name = models.CharField(max_length=120, blank=True, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="تصویر پروفایل")

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"

    def __str__(self):
        return self.full_name or str(self.user)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="کاربر")
    title = models.CharField(max_length=60, verbose_name="عنوان آدرس (خانه، محل کار)")
    province = models.CharField(max_length=60, verbose_name="استان")
    city = models.CharField(max_length=60, verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس کامل")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی",blank=True)
    is_default = models.BooleanField(default=False, verbose_name="آدرس پیش‌فرض")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
        ordering = ['-is_default', '-id']

    def __str__(self):
        return f"{self.title} - {self.city}"
