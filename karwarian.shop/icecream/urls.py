from django.urls import path
from . import views

app_name = 'icecream'

urlpatterns = [
    # Frontend pages (clean URLs)
    path('', views.icecream_home, name='home'),
    path('products/', views.icecream_products, name='products'),
    path('cup/', views.icecream_cup, name='cup'),
    path('cone/', views.icecream_cone, name='cone'),
    path('chocobar/', views.icecream_chocobar, name='chocobar'),
    path('kulfi/', views.icecream_kulfi, name='kulfi'),
    path('gadbad/', views.icecream_gadbad, name='gadbad'),
    path('cart/', views.icecream_cart, name='cart'),
    path('payment/', views.icecream_payment, name='payment'),
    
    # Legacy and relative HTML URL patterns to resolve 404s from hardcoded links
    path('index.html', views.icecream_home, name='home_html'),
    path('products.html', views.icecream_products, name='products_html'),
    path('cup.html', views.icecream_cup, name='cup_html'),
    path('cone.html', views.icecream_cone, name='cone_html'),
    path('chocobar.html', views.icecream_chocobar, name='chocobar_html'),
    path('kulfi.html', views.icecream_kulfi, name='kulfi_html'),
    path('gadbad.html', views.icecream_gadbad, name='gadbad_html'),
    path('cart.html', views.icecream_cart, name='cart_html'),
    path('payment.html', views.icecream_payment, name='payment_html'),
    
    # Relative subdirectory patterns for redirection from /ice-cream/products/
    path('products/index.html', views.icecream_home),
    path('products/products.html', views.icecream_products),
    path('products/cup.html', views.icecream_cup),
    path('products/cone.html', views.icecream_cone),
    path('products/chocobar.html', views.icecream_chocobar),
    path('products/kulfi.html', views.icecream_kulfi),
    path('products/gadbad.html', views.icecream_gadbad),
    path('products/cart.html', views.icecream_cart),
    path('products/payment.html', views.icecream_payment),
    
    # API endpoints
    path('api/health/', views.health_check, name='api_health'),
    path('api/orders/', views.create_order, name='api_create_order'),
    path('api/orders/list/', views.list_orders, name='api_list_orders'),
    path('api/orders/<str:order_id>/', views.get_order, name='api_get_order'),
    path('api/admin/login/', views.admin_login_api, name='api_admin_login'),
    path('api/orders/<str:order_id>/update-status/', views.update_order_status, name='api_update_status'),
    
    # Admin pages
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    path('pending-orders/', views.pending_orders_view, name='pending_orders'),
    path('confirmed-orders/', views.confirmed_orders_view, name='confirmed_orders'),
    path('out-for-delivery/', views.out_for_delivery_view, name='out_for_delivery'),
    path('delivered-orders/', views.delivered_orders_view, name='delivered_orders'),
]
