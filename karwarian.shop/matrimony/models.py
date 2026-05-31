from django.db import models
from django.contrib.auth.models import User


class MatrimonyProfile(models.Model):
    """Matrimony profiles"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    MARITAL_STATUS = [
        ('never_married', 'Never Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='matrimony_profile')
    
    # Basic Info
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    height = models.CharField(max_length=20, help_text="e.g., 5'8\"")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS)
    
    # Contact
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    
    # Professional
    education = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    annual_income = models.CharField(max_length=100, blank=True)
    
    # Family
    father_name = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    siblings = models.CharField(max_length=200, blank=True)
    
    # Additional
    religion = models.CharField(max_length=100)
    caste = models.CharField(max_length=100, blank=True)
    about = models.TextField(help_text="About yourself")
    partner_expectations = models.TextField(blank=True)
    
    # Photo
    photo = models.ImageField(upload_to='matrimony/', blank=True, null=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.gender}"
