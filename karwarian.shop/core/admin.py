from django.contrib import admin
from .models import SiteStatistics, BusTiming, ContactMessage, MatrimonyProfile


@admin.register(SiteStatistics)
class SiteStatisticsAdmin(admin.ModelAdmin):
    list_display = ['beaches_count', 'matrimony_profiles', 'events_per_year', 'local_vendors', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one statistics record
        return not SiteStatistics.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(BusTiming)
class BusTimingAdmin(admin.ModelAdmin):
    list_display = ['route_name', 'from_location', 'to_location', 'departure_time', 'arrival_time', 'bus_type', 'is_active']
    list_filter = ['bus_type', 'is_active', 'from_location', 'to_location']
    search_fields = ['route_name', 'from_location', 'to_location']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(MatrimonyProfile)
class MatrimonyProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'age', 'gender', 'caste', 'qualification', 'has_photo', 'is_approved', 'is_active', 'created_at']
    list_filter = ['is_approved', 'is_active', 'gender', 'caste', 'created_at']
    search_fields = ['full_name', 'father_name', 'qualification', 'occupation']
    list_editable = ['is_approved', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'photo_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'father_name', 'age', 'gender', 'height', 'caste', 'photo', 'photo_preview')
        }),
        ('Education & Occupation', {
            'fields': ('qualification', 'occupation')
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'address')
        }),
        ('Additional Details', {
            'fields': ('additional_info',)
        }),
        ('Admin Controls', {
            'fields': ('is_approved', 'is_active', 'created_at', 'updated_at')
        }),
    )

    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Photo'

    def photo_preview(self, obj):
        if obj.photo:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height:120px;border-radius:8px;">', obj.photo.url)
        return '—'
    photo_preview.short_description = 'Preview'
