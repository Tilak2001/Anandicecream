from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('orders/', views.create_order, name='create_order'),
    path('orders/list/', views.list_orders, name='list_orders'),
    path('orders/<str:order_id>/', views.get_order, name='get_order'),
    # Admin authentication
    path('admin/login/', views.admin_login_api, name='admin_login_api'),
    # Order management
    path('orders/<str:order_id>/update-status/', views.update_order_status, name='update_order_status'),
]
