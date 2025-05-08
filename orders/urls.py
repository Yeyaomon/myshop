from django.urls import path
from . import views

# orders/urls.py

urlpatterns = [
    # Cart & checkout
    path('cart/add/<int:product_id>/', views.add_to_cart,    name='add_to_cart'),
    path('detail/<int:order_id>/',    views.order_detail,    name='order_detail'),
    path('cart/',                     views.view_cart,       name='view_cart'),
    path('checkout/',                 views.checkout,        name='checkout'),
    path('cart/remove/',              views.remove_from_cart,name='remove_from_cart'),

    # Immediate buy
    path('buy/<int:product_id>/',     views.buy_product,     name='buy_product'),

    # Order history
    path('orders/',                   views.order_list,      name='order_list'),

    # Admin dashboard
    path('admin/dashboard/',          views.admin_dashboard, name='admin_dashboard'),
]
