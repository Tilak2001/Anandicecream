from django.db import models


class PlaceCategory(models.Model):
    """Categories for places (Beach, Fort, Island, Temple, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Place Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Place(models.Model):
    """Places to visit in Karwar"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(PlaceCategory, on_delete=models.CASCADE, related_name='places')
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for cards")
    
    # Location details
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Additional info
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    entry_fee = models.CharField(max_length=100, blank=True, help_text="e.g., Free, ₹50, etc.")
    timings = models.CharField(max_length=200, blank=True, help_text="Opening hours")
    
    # Images
    main_image = models.ImageField(upload_to='places/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Alternative to uploading image")
    
    # Meta
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def get_image_url(self):
        """Return image URL, prioritizing uploaded image"""
        if self.main_image:
            return self.main_image.url
        return self.image_url or '/static/images/placeholder.jpg'


class PlaceImage(models.Model):
    """Additional images for places"""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='places/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.place.name} - Image"
