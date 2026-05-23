from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("category/<path:path>/",views.CategoryDetailView.as_view(),name="category_detail"),
    path("",views.home,name="home"),
    path("products/<path:slug>/",views.product_detail,name="product-detail"),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/', views.cart_add, name="cart_add"), # بدون پارامتر در URL
    path('cart/remove/<int:variant_id>/', views.cart_remove, name="cart_remove"),
    path("add/<int:product_id>/", views.add_comment, name="add_comment"),

]

