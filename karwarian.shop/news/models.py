from django.db import models
from django.contrib.auth.models import User


class NewsCategory(models.Model):
    """News categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    """News articles"""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='news')
    content = models.TextField()
    excerpt = models.CharField(max_length=300, help_text="Brief summary")
    
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=200, blank=True, help_text="News source if external")
    
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/news-placeholder.jpg'
