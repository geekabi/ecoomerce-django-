from django import forms
from .models import Profile,Address





class PhoneForm(forms.Form):
   phone = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            "placeholder": "مثلاً 09123456789"
        })
   )

class OTPForm(forms.Form):

    code = forms.CharField(
        max_length=6,
        label="کد تایید",
        widget=forms.TextInput(attrs={
            "placeholder": "کد پیامک شده"
        })

    )

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["full_name", "email", "avatar"]    



class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            "title",
            "province",
            "city",
            "address",
            "postal_code",
            "is_default",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "province": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows":3}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }
