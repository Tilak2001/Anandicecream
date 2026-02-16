from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .utils import generate_order_id, send_order_email, send_order_acceptance_email, send_order_rejection_email
import json


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
        
        print(f"[SUCCESS] New order created: {order_id} (Payment: {order.payment_status})")
        
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
        print(f"[ERROR] Error creating order: {e}")
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


# Admin Authentication Views
def admin_login_view(request):
    """Admin login page"""
    if request.session.get('is_admin'):
        return redirect('admin_dashboard')
    
    return render(request, 'admin_login.html')


@csrf_exempt
def admin_login_api(request):
    """Admin login API endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '')
            password = data.get('password', '')
            
            # Hardcoded credentials
            if username == 'admin' and password == 'admin':
                # Set session
                request.session['is_admin'] = True
                request.session['admin_username'] = username
                
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid username or password'
                }, status=401)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    }, status=405)


def admin_logout_view(request):
    """Admin logout"""
    request.session.flush()
    return redirect('admin_login')


def admin_dashboard_view(request):
    """Admin dashboard - requires authentication"""
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    
    # Get all orders
    orders = Order.objects.all().order_by('-created_at')
    
    # Calculate statistics
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    confirmed_orders = orders.filter(status='confirmed').count()
    delivered_orders = orders.filter(status='delivered').count()
    
    # Calculate revenue
    total_revenue = sum(float(order.total_amount) for order in orders)
    
    context = {
        'admin_username': request.session.get('admin_username', 'Admin'),
        'orders': orders[:20],  # Show latest 20 orders
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'delivered_orders': delivered_orders,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'admin_dashboard.html', context)


def pending_orders_view(request):
    """Pending orders page - requires authentication"""
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    
    # Get all pending orders
    pending_orders = Order.objects.filter(status='pending').order_by('-created_at')
    
    context = {
        'admin_username': request.session.get('admin_username', 'Admin'),
        'pending_orders': pending_orders,
    }
    
    return render(request, 'pending_orders.html', context)


@csrf_exempt
def update_order_status(request, order_id):
    """API endpoint to accept or reject orders"""
    if request.method == 'POST':
        try:
            # Check if admin is logged in
            if not request.session.get('is_admin'):
                return JsonResponse({
                    'success': False,
                    'message': 'Unauthorized'
                }, status=401)
            
            # Get order
            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Order not found'
                }, status=404)
            
            # Parse request data
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'accept':
                # Update order status to confirmed
                order.status = 'confirmed'
                order.payment_status = 'verified'
                order.save()
                
                # Send acceptance email
                try:
                    send_order_acceptance_email(order)
                except Exception as email_error:
                    print(f"[ERROR] Failed to send acceptance email: {email_error}")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Order accepted successfully',
                    'order': {
                        'order_id': order.order_id,
                        'status': order.status,
                        'payment_status': order.payment_status
                    }
                })
                
            elif action == 'reject':
                # Update order status to cancelled
                order.status = 'cancelled'
                order.payment_status = 'failed'
                order.save()
                
                # Send rejection email with refund information
                try:
                    send_order_rejection_email(order)
                except Exception as email_error:
                    print(f"[ERROR] Failed to send rejection email: {email_error}")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Order rejected successfully',
                    'order': {
                        'order_id': order.order_id,
                        'status': order.status,
                        'payment_status': order.payment_status
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid action'
                }, status=400)
                
        except Exception as e:
            print(f"[ERROR] Error updating order status: {e}")
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    }, status=405)

