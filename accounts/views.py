from django.shortcuts import render, redirect
from .forms import PhoneForm,OTPForm,ProfileForm
from .models import OTP
from django.contrib.auth import get_user_model
from common.utils.sms import send_sms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Address
from .forms import AddressForm
from django.shortcuts import redirect, get_object_or_404
from orders.models import Order

def login_view(request):

    if request.method == "POST":
        form = PhoneForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]

            otp = OTP.objects.create(phone=phone)

            send_sms(phone, f"کد ورود شما: {otp.code}")

            request.session["phone"] = phone

            return redirect("accounts:verify")

    else:
        form = PhoneForm()

    return render(request, "accounts/login.html", {"form": form})


User = get_user_model()
def verify_view(request):

    phone = request.session.get("phone")

    if not phone:
        return redirect("login")

    if request.method == "POST":
        form = OTPForm(request.POST)

        if form.is_valid():

            code = form.cleaned_data["code"]

            otp = OTP.objects.filter(phone=phone, code=code).last()

            if otp:

                user, created = User.objects.get_or_create(phone=phone)

                login(request, user)

                return redirect("/")

    else:
        form = OTPForm()

    return render(request, "accounts/verify.html", {"form": form})


@login_required
def dashboard_view(request):
    profile = request.user.profile
    return render(request, "accounts/dashboard.html", {
        "profile": profile
    })
    
    

@login_required
def profile_edit_view(request):

    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("accounts:dashboard")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {"form": form})

class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = "accounts/address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy("accounts:address_list")

    def form_valid(self, form):
        form.instance.user = self.request.user

        if form.cleaned_data.get("is_default"):
            Address.objects.filter(user=self.request.user).update(is_default=False)

        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy("accounts:address_list")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if form.cleaned_data.get("is_default"):
            Address.objects.filter(user=self.request.user).update(is_default=False)

        return super().form_valid(form)

@login_required
def set_default_address(request, pk):

    address = get_object_or_404(Address, id=pk, user=request.user)

    # همه آدرس‌ها را غیر پیش‌فرض کن
    Address.objects.filter(user=request.user).update(is_default=False)

    # این آدرس را پیش‌فرض کن
    address.is_default = True
    address.save()

    return redirect("accounts:address_list")

def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    for order in orders:
        order.auto_fail_if_expired()
        

    return render(request, "accounts/order_list.html", {"orders": orders})


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect("/")
