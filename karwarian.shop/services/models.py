from django.db import models
from django.contrib.auth.models import User


class ServiceCategory(models.Model):
    """Service categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Services and goods listings"""
    SERVICE_TYPE_CHOICES = [
        ('function_service', 'Function Service'),
        ('goods', 'Goods'),
        ('second_hand', 'Second Hand Items'),
        ('rental', 'Rental'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='services')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)

    FUNCTION_SEGMENT_CHOICES = [
        ('decoration', 'Decoration'),
        ('catering', 'Catering'),
        ('photography', 'Photography'),
    ]
    function_segment = models.CharField(
        max_length=20, choices=FUNCTION_SEGMENT_CHOICES, blank=True,
        help_text='Function Services category (decoration, catering, photography)',
    )
    function_subcategory = models.CharField(
        max_length=50, blank=True,
        help_text='e.g. marriage, haldi, veg-thali, wedding',
    )
    
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_text = models.CharField(max_length=100, blank=True, help_text="e.g., 'Starting from ₹5000', 'Negotiable'")
    
    # Images
    main_image = models.ImageField(upload_to='services/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    
    # Contact
    provider_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True)
    location = models.CharField(max_length=200)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    
    # Meta
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.main_image:
            return self.main_image.url
        return self.image_url or '/static/images/service-placeholder.jpg'
