from django.db import models
from django.contrib.auth.models import User


class JobCategory(models.Model):
    """Job categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Job(models.Model):
    """Job listings"""
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='jobs')
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='jobs/companies/', blank=True, null=True)
    
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., ₹20,000 - ₹30,000")
    
    description = models.TextField()
    requirements = models.TextField(help_text="Job requirements and qualifications")
    responsibilities = models.TextField(blank=True)
    
    # Contact
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True)
    application_url = models.URLField(blank=True, help_text="External application link")
    
    # Meta
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    expires_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} at {self.company_name}"
