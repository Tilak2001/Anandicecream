from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""
    
    list_display = [
        'order_id', 'full_name', 'email', 'phone',
        'total_amount', 'payment_status', 'status', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'full_name', 'email', 'phone']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'order_date', 'status', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone', 'alternate_phone', 'delivery_address', 'pincode')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_screenshot')
        }),
        ('Order Items', {
            'fields': ('items',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
