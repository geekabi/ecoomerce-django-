from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [

    path('', views.dashboard, name="dashboard"),

    path('products/',
         views.product_list,
         name="products"),

     path("products/create/", views.product_create, name="product-create"),
     path("products/<int:pk>/edit/", views.product_update, name="product-update"),
      path(
        "products/<int:product_id>/variants/",
        views.product_variants,
        name="admin-product-variants",
    ),
    path(
    "variants/<int:variant_id>/update/",
    views.variant_update,
    name="admin-variant-update",
),
path(
    "attributes/create/",
    views.attribute_create,
    name="admin-attribute-create",
),

path(
    "attributes/<int:attr_id>/values/create/",
    views.attribute_value_create,
    name="admin-attribute-value-create",
),
path("adminpanel/variants/<int:variant_id>/delete/",
     views.variant_delete,
     name="admin-variant-delete"),

path("categories/", views.admin_categories_list, name="categories-list"),
path("categories/create/", views.admin_category_create, name="category-create"),
path("categories/<int:pk>/edit/", views.admin_category_edit, name="category-edit"),
path("orders/", views.admin_orders_list, name="orders"),

path(
    "orders/<int:order_id>/",
    views.admin_order_detail,
    name="order-detail"
),




   
]
