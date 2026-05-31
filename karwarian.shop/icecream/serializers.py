from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'full_name', 'email', 'phone',
            'delivery_address', 'pincode', 'alternate_phone',
            'items', 'total_amount', 'payment_screenshot',
            'payment_status', 'order_date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_id', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating orders from frontend data"""
    
    customerInfo = serializers.DictField()
    items = serializers.ListField()
    totalAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    orderDate = serializers.DateTimeField(required=False)
    paymentScreenshot = serializers.CharField(required=False, allow_blank=True)
    paymentStatus = serializers.CharField(required=False, default='pending')
    status = serializers.CharField(required=False, default='pending')
    
    def validate_customerInfo(self, value):
        """Validate customer info has required fields"""
        required_fields = ['fullName', 'email', 'phone', 'deliveryAddress', 'pincode']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"Missing required field: {field}")
        return value
    
    def validate_items(self, value):
        """Validate items list is not empty"""
        if not value or len(value) == 0:
            raise serializers.ValidationError("Cart must contain at least one item")
        return value
