from django.contrib.auth import views
from django.urls import path
from .views import (Home, ProductAdmin, CreatProduct, UpdateProduct,
                    DeleteProduct, Profile, Users)

app_name = "account"

urlpatterns = [
    path('', Home.as_view(), name="dashboard"),
    path('products/', ProductAdmin.as_view(), name="products"),
    path('products/create_product/', CreatProduct.as_view(), name="product_create"),
    path('products/update_product/<int:pk>', UpdateProduct.as_view(), name="product_update"),
    path('products/delete_product/<int:pk>', DeleteProduct.as_view(), name="product_delete"),
    path('profile/', Profile.as_view(), name="profile"),
    path('users/', Users.as_view(), name="users"),
]
