"""
Utility functions for orders app
"""
import base64
import io
import time
import random
import string
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_order_id():
    """Generate unique order ID"""
    timestamp = base36_encode(int(time.time() * 1000))
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"ORD-{timestamp}-{random_str}"


def base36_encode(number):
    """Convert number to base36 string"""
    if number == 0:
        return '0'
    
    base36 = []
    while number:
        number, i = divmod(number, 36)
        base36.append('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i])
    
    return ''.join(reversed(base36))


def convert_image_to_pdf(base64_image):
    """
    Convert base64 image to PDF buffer
    
    Args:
        base64_image: Base64 encoded image string
        
    Returns:
        BytesIO buffer containing PDF data
    """
    try:
        # Remove data URL prefix if present
        if ',' in base64_image:
            base64_data = base64_image.split(',')[1]
        else:
            base64_data = base64_image
        
        # Decode base64 to image
        image_data = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_data))
        
        # Get image dimensions
        img_width, img_height = image.size
        
        # Create PDF buffer
        pdf_buffer = io.BytesIO()
        
        # Create PDF with image dimensions
        c = canvas.Canvas(pdf_buffer, pagesize=(img_width, img_height))
        
        # Save image to temporary buffer
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Draw image on PDF
        c.drawImage(img_buffer, 0, 0, width=img_width, height=img_height)
        
        # Finalize PDF
        c.save()
        
        # Reset buffer position
        pdf_buffer.seek(0)
        
        return pdf_buffer
        
    except Exception as e:
        print(f"Error converting image to PDF: {e}")
        raise


def send_order_email(order_data, order_id):
    """
    Send order confirmation email to admin with PDF attachment
    
    Args:
        order_data: Dictionary containing order information
        order_id: Unique order ID
        
    Returns:
        Boolean indicating success
    """
    try:
        # Format items for email
        items_list = '\n'.join([
            f"- {item['product']} ({item['flavor']}) x{item.get('quantity', 1)} - ₹{item['price']}"
            for item in order_data['items']
        ])
        
        # Email subject
        subject = f"🍦 New Order Received - {order_id}"
        
        # Email body (HTML)
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #ff6b9d;">🍦 New Order Received!</h2>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #333;">Order Details</h3>
                <p><strong>Order ID:</strong> {order_id}</p>
                <p><strong>Order Date:</strong> {order_data.get('orderDate', 'N/A')}</p>
                <p><strong>Total Amount:</strong> ₹{order_data['totalAmount']}</p>
                <p><strong>Payment Status:</strong> {order_data.get('paymentStatus', 'Pending Verification')}</p>
            </div>

            <div style="background: #fff5f8; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #333;">Customer Information</h3>
                <p><strong>Name:</strong> {order_data['customerInfo']['fullName']}</p>
                <p><strong>Email:</strong> {order_data['customerInfo']['email']}</p>
                <p><strong>Phone:</strong> {order_data['customerInfo']['phone']}</p>
                {f"<p><strong>Alternate Phone:</strong> {order_data['customerInfo'].get('alternatePhone', 'N/A')}</p>" if order_data['customerInfo'].get('alternatePhone') else ''}
                <p><strong>Delivery Address:</strong> {order_data['customerInfo']['deliveryAddress']}</p>
                <p><strong>Pincode:</strong> {order_data['customerInfo']['pincode']}</p>
            </div>

            <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #333;">Order Items</h3>
                <pre style="font-family: monospace; white-space: pre-wrap;">{items_list}</pre>
            </div>

            {'''
            <div style="background: #fff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #4CAF50;">
                <h3 style="color: #333;">📎 Payment Screenshot</h3>
                <p style="color: #666; font-size: 14px;">Payment screenshot is attached as a PDF file. Please check the attachment to view the payment proof.</p>
            </div>
            ''' if order_data.get('paymentScreenshot') else '<p style="color: #999;">No payment screenshot provided</p>'}

            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; color: #666; font-size: 12px;">
                <p>This is an automated email from Anand Ice Cream ordering system.</p>
            </div>
        </div>
        """
        
        # Create email
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.content_subtype = 'html'
        
        # Attach PDF if payment screenshot exists
        if order_data.get('paymentScreenshot'):
            try:
                pdf_buffer = convert_image_to_pdf(order_data['paymentScreenshot'])
                email.attach(
                    f'payment-screenshot-{order_id}.pdf',
                    pdf_buffer.read(),
                    'application/pdf'
                )
                print(f"✅ Payment screenshot converted to PDF for order: {order_id}")
            except Exception as pdf_error:
                print(f"❌ Error converting screenshot to PDF: {pdf_error}")
                # Fallback: attach as image
                try:
                    base64_data = order_data['paymentScreenshot'].split(',')[1] if ',' in order_data['paymentScreenshot'] else order_data['paymentScreenshot']
                    image_data = base64.b64decode(base64_data)
                    email.attach(
                        f'payment-screenshot-{order_id}.png',
                        image_data,
                        'image/png'
                    )
                    print(f"⚠️ Fallback: Attached screenshot as image for order: {order_id}")
                except Exception as img_error:
                    print(f"❌ Error attaching image: {img_error}")
        
        # Send email
        email.send()
        print(f"📧 Order email sent to admin for order: {order_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
