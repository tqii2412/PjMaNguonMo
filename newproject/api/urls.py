from django.urls import path
from .views import *

urlpatterns = [
    # User URLs
    path('users/', get_users, name='get_users'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:pk>/', user_detail, name='user_detail'),

    # Admin URLs
    path('admins/', get_admins, name='get_admins'),
    path('admins/create/', create_admin, name='create_admin'),
    path('admins/<int:pk>/', admin_detail, name='admin_detail'),

    # Product URLs
    path('products/', get_products, name='get_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:pk>/', product_detail, name='product_detail'),

    # ProductDetail URLs
    path('product-details/', get_product_details, name='get_product_details'),
    path('product-details/create/', create_product_detail, name='create_product_detail'),
    path('product-details/<int:pk>/', product_detail_detail, name='product_detail_detail'),

    # Cart URLs
    path('carts/', get_carts, name='get_carts'),
    path('carts/create/', create_cart, name='create_cart'),
    path('carts/<int:pk>/', cart_detail, name='cart_detail'),

    # Order URLs
    path('orders/', get_orders, name='get_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<int:pk>/', order_detail, name='order_detail'),

    # OrderItem URLs
    path('order-items/', get_order_items, name='get_order_items'),
    path('order-items/create/', create_order_item, name='create_order_item'),
    path('order-items/<int:pk>/', order_item_detail, name='order_item_detail'),
]