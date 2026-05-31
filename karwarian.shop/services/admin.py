from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'service_type', 'function_segment', 'function_subcategory',
        'provider_name', 'is_featured', 'is_verified', 'is_active', 'views_count', 'created_at',
    ]
    list_filter = [
        'service_type', 'function_segment', 'is_featured', 'is_verified',
        'is_active', 'category', 'created_at',
    ]
    search_fields = ['title', 'provider_name', 'location', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
