from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .utils import generate_order_id, send_order_email


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return Response({
            'status': 'OK',
            'message': 'Server is running',
            'database': 'Connected'
        })
    except Exception as e:
        return Response({
            'status': 'ERROR',
            'message': 'Database connection failed',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_order(request):
    """Create a new order"""
    try:
        # Validate input data
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid data',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        customer_info = data['customerInfo']
        
        # Generate unique order ID
        order_id = generate_order_id()
        
        # Create order
        order = Order.objects.create(
            order_id=order_id,
            full_name=customer_info['fullName'],
            email=customer_info['email'],
            phone=customer_info['phone'],
            delivery_address=customer_info['deliveryAddress'],
            pincode=customer_info['pincode'],
            alternate_phone=customer_info.get('alternatePhone', ''),
            items=data['items'],
            total_amount=data['totalAmount'],
            payment_screenshot=data.get('paymentScreenshot', ''),
            payment_status=data.get('paymentStatus', 'pending'),
            status=data.get('status', 'pending'),
            order_date=data.get('orderDate')
        )
        
        print(f"✅ New order created: {order_id} (Payment: {order.payment_status})")
        
        # Send email to admin (async in background)
        try:
            send_order_email({
                'customerInfo': customer_info,
                'items': data['items'],
                'totalAmount': str(data['totalAmount']),
                'orderDate': str(order.order_date),
                'paymentStatus': order.payment_status,
                'paymentScreenshot': data.get('paymentScreenshot', '')
            }, order_id)
        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
        
        # Return response
        return Response({
            'success': True,
            'message': 'Order placed successfully',
            'orderId': order_id,
            'order': {
                'orderId': order.order_id,
                'customerInfo': {
                    'fullName': order.full_name,
                    'email': order.email,
                    'phone': order.phone,
                    'deliveryAddress': order.delivery_address,
                    'pincode': order.pincode,
                    'alternatePhone': order.alternate_phone
                },
                'items': order.items,
                'totalAmount': float(order.total_amount),
                'paymentStatus': order.payment_status,
                'orderDate': order.order_date,
                'status': order.status
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        return Response({
            'error': 'Failed to create order',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_orders(request):
    """List all orders (for admin)"""
    try:
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        
        return Response({
            'success': True,
            'count': orders.count(),
            'orders': serializer.data
        })
    except Exception as e:
        print(f"❌ Error fetching orders: {e}")
        return Response({
            'error': 'Failed to fetch orders',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_order(request, order_id):
    """Get specific order by order_id"""
    try:
        order = Order.objects.get(order_id=order_id)
        serializer = OrderSerializer(order)
        
        return Response({
            'success': True,
            'order': serializer.data
        })
    except Order.DoesNotExist:
        return Response({
            'error': 'Order not found',
            'message': f'No order found with ID: {order_id}'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Error fetching order: {e}")
        return Response({
            'error': 'Failed to fetch order',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
