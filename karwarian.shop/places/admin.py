from django.contrib import admin
from .models import PlaceCategory, Place, PlaceImage


@admin.register(PlaceCategory)
class PlaceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'is_active', 'views_count', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlaceImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'short_description', 'description')
        }),
        ('Location', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('Visit Information', {
            'fields': ('best_time_to_visit', 'entry_fee', 'timings')
        }),
        ('Images', {
            'fields': ('main_image', 'image_url')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active', 'views_count')
        }),
    )
    readonly_fields = ['views_count']
