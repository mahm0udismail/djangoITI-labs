from django.urls import path
from .views import category_list_create, producer_list_create, product_list_create

urlpatterns = [
    path('categories/', category_list_create, name='category-list-create'),
    path('producers/', producer_list_create, name='producer-list-create'),
    path('products/', product_list_create, name='product-list-create'),
]
