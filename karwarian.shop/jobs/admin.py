from django.contrib import admin
from .models import JobCategory, Job


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'job_type', 'location', 'is_featured', 'is_active', 'views_count', 'created_at']
    list_filter = ['job_type', 'is_featured', 'is_active', 'category', 'created_at']
    search_fields = ['title', 'company_name', 'location', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'applications_count', 'created_at', 'updated_at']
