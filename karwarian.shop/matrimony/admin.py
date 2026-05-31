from django.contrib import admin
from .models import MatrimonyProfile


@admin.register(MatrimonyProfile)
class MatrimonyProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'age_display', 'city', 'occupation', 'is_verified', 'is_active', 'created_at']
    list_filter = ['gender', 'marital_status', 'is_verified', 'is_active', 'city']
    search_fields = ['full_name', 'email', 'phone', 'city', 'occupation']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    def age_display(self, obj):
        from datetime import date
        today = date.today()
        age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
        return f"{age} years"
    age_display.short_description = 'Age'
