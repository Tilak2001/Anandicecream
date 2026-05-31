"""
URL configuration for karwarian_shop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('places/', include('places.urls')),
    path('news/', include('news.urls')),
    path('matrimony/', include('matrimony.urls')),
    path('jobs/', include('jobs.urls')),
    path('services/', include('services.urls')),
    path('ice-cream/', include('icecream.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "Karwarian.shop Admin"
admin.site.site_title = "Karwarian Admin Portal"
admin.site.index_title = "Welcome to Karwarian.shop Administration"
