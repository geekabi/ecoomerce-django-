from django.urls import path
from .views import login_view, verify_view,dashboard_view, profile_edit_view,AddressListView, AddressCreateView, AddressUpdateView,set_default_address,order_list
from .views import user_logout
app_name = "accounts"

urlpatterns = [

    path("login/", login_view, name="login"),
    path("verify/", verify_view, name="verify"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/add/", AddressCreateView.as_view(), name="address_add"),
    path("addresses/<int:pk>/edit/", AddressUpdateView.as_view(), name="address_edit"),
    path("addresses/default/<int:pk>/", set_default_address,name="address_set_default"),
    path("my-orders/", order_list, name="order_list"),
    path('logout/', user_logout, name='logout'),


]
