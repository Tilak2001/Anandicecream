from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('orders/', views.create_order, name='create_order'),
    path('orders/list/', views.list_orders, name='list_orders'),
    path('orders/<str:order_id>/', views.get_order, name='get_order'),
]
