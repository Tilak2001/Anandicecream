from django.db import models
from django.utils import timezone


class Order(models.Model):
    """Order model matching the existing PostgreSQL schema"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('pending_verification', 'Pending Verification'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    pincode = models.CharField(max_length=10)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    items = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_screenshot = models.TextField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=50, 
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"{self.order_id} - {self.full_name}"
