"""
URL configuration for anand_ice_cream project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from orders import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/', include('orders.urls')),
    # Frontend pages - support both with and without .html
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index'),
    path('cart.html', TemplateView.as_view(template_name='cart.html'), name='cart'),
    path('payment.html', TemplateView.as_view(template_name='payment.html'), name='payment'),
    path('products.html', TemplateView.as_view(template_name='products.html'), name='products'),
    path('cone.html', TemplateView.as_view(template_name='cone.html'), name='cone'),
    path('cup.html', TemplateView.as_view(template_name='cup.html'), name='cup'),
    path('chocobar.html', TemplateView.as_view(template_name='chocobar.html'), name='chocobar'),
    path('kulfi.html', TemplateView.as_view(template_name='kulfi.html'), name='kulfi'),
    path('gadbad.html', TemplateView.as_view(template_name='gadbad.html'), name='gadbad'),
    # Admin pages
    path('admin-login.html', order_views.admin_login_view, name='admin_login'),
    path('admin-dashboard.html', order_views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-logout/', order_views.admin_logout_view, name='admin_logout'),
    path('pending-orders.html', order_views.pending_orders_view, name='pending_orders'),  # Pending orders management
    path('confirmed-orders.html', order_views.confirmed_orders_view, name='confirmed_orders'),  # Confirmed orders management
    path('out-for-delivery.html', order_views.out_for_delivery_view, name='out_for_delivery'),  # Out for delivery orders
    path('delivered-orders.html', order_views.delivered_orders_view, name='delivered_orders'),  # Delivered orders
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

