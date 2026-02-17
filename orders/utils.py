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
        print(f"[ERROR] Error sending email: {e}")
        return False


def send_order_acceptance_email(order):
    """
    Send order acceptance email to customer
    
    Args:
        order: Order model instance
        
    Returns:
        Boolean indicating success
    """
    try:
        # Format items for email
        items_list = '\n'.join([
            f"- {item['product']} ({item['flavor']}) x{item.get('quantity', 1)} - ₹{item['price']}"
            for item in order.items
        ])
        
        # Email subject
        subject = f"Order Confirmed - Anand Ice Cream (Order #{order.order_id})"
        
        # Email body (HTML)
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🎉 Order Confirmed!</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <p style="font-size: 16px; color: #333;">Dear {order.full_name},</p>
                
                <p style="font-size: 16px; color: #333; line-height: 1.6;">
                    Great news! Your order has been <strong style="color: #00b894;">successfully confirmed</strong>.
                </p>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #00b894;">
                    <h3 style="color: #333; margin-top: 0;">Order Details</h3>
                    <p><strong>Order ID:</strong> {order.order_id}</p>
                    <p><strong>Total Amount:</strong> ₹{order.total_amount}</p>
                    <p><strong>Order Date:</strong> {order.order_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">Order Items</h3>
                    <pre style="font-family: monospace; white-space: pre-wrap; color: #666;">{items_list}</pre>
                </div>
                
                <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;">
                    <p style="font-size: 18px; color: #00b894; margin: 0;">
                        🍦 Your delicious ice cream will be delivered soon!
                    </p>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 30px;">
                    Thank you for choosing Anand Ice Cream!
                </p>
                
                <p style="font-size: 14px; color: #666;">
                    Best regards,<br>
                    <strong>Anand Ice Cream Team</strong>
                </p>
            </div>
            
            <div style="margin-top: 20px; padding: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>This is an automated email from Anand Ice Cream ordering system.</p>
            </div>
        </div>
        """
        
        # Create email
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.content_subtype = 'html'
        
        # Send email
        email.send()
        print(f"[SUCCESS] Order acceptance email sent to {order.email} for order: {order.order_id}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error sending acceptance email: {e}")
        return False


def send_order_rejection_email(order):
    """
    Send order rejection email to customer with refund information
    
    Args:
        order: Order model instance
        
    Returns:
        Boolean indicating success
    """
    try:
        # Email subject
        subject = f"Order Cancelled - Anand Ice Cream (Order #{order.order_id})"
        
        # Email body (HTML)
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #ff6b9d 0%, #e84393 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">Order Cancelled</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <p style="font-size: 16px; color: #333;">Dear {order.full_name},</p>
                
                <p style="font-size: 16px; color: #333; line-height: 1.6;">
                    We regret to inform you that your order has been <strong style="color: #e84393;">cancelled</strong>.
                </p>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #e84393;">
                    <h3 style="color: #333; margin-top: 0;">Order Details</h3>
                    <p><strong>Order ID:</strong> {order.order_id}</p>
                    <p><strong>Total Amount:</strong> ₹{order.total_amount}</p>
                    <p><strong>Order Date:</strong> {order.order_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h3 style="color: #856404; margin-top: 0;">💰 Refund Information</h3>
                    <p style="color: #856404; font-size: 15px; line-height: 1.6;">
                        Your amount of <strong>₹{order.total_amount}</strong> will be refunded within <strong>3 working days</strong>.
                    </p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #667eea;">
                    <h3 style="color: #333; margin-top: 0;">📞 Need Help?</h3>
                    <p style="color: #666; margin: 10px 0;">For more details, please contact us:</p>
                    <p style="margin: 5px 0;"><strong>Email:</strong> <a href="mailto:anandicecream@gmail.com" style="color: #667eea; text-decoration: none;">anandicecream@gmail.com</a></p>
                    <p style="margin: 5px 0;"><strong>Phone:</strong> <a href="tel:1234567890" style="color: #667eea; text-decoration: none;">1234567890</a></p>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 30px;">
                    We apologize for any inconvenience caused.
                </p>
                
                <p style="font-size: 14px; color: #666;">
                    Best regards,<br>
                    <strong>Anand Ice Cream Team</strong>
                </p>
            </div>
            
            <div style="margin-top: 20px; padding: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>This is an automated email from Anand Ice Cream ordering system.</p>
            </div>
        </div>
        """
        
        # Create email
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.content_subtype = 'html'
        
        # Send email
        email.send()
        print(f"[SUCCESS] Order rejection email sent to {order.email} for order: {order.order_id}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error sending rejection email: {e}")
        return False


def send_delivery_confirmation_email(order):
    """Send delivery confirmation email to customer with invoice attachment"""
    try:
        # Generate invoice PDF
        invoice_path = generate_invoice_pdf(order)
        
        subject = f'Order Delivered - Anand Ice Cream (Order #{order.order_id})'
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #00b894 0%, #00cec9 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .order-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .detail-label {{ font-weight: bold; color: #666; }}
                .detail-value {{ color: #333; }}
                .items-list {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .item {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
                .success-icon {{ font-size: 48px; margin-bottom: 20px; }}
                .invoice-notice {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2196f3; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="success-icon">✅</div>
                    <h1>Order Delivered Successfully!</h1>
                    <p>Your delicious ice cream has been delivered</p>
                </div>
                
                <div class="content">
                    <p>Dear {order.full_name},</p>
                    
                    <p>Great news! Your order has been successfully delivered to your address.</p>
                    
                    <div class="invoice-notice">
                        <h3>📄 Invoice Attached</h3>
                        <p>Please find your invoice attached to this email for your records.</p>
                    </div>
                    
                    <div class="order-details">
                        <h3>Order Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Order ID:</span>
                            <span class="detail-value">{order.order_id}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Total Amount:</span>
                            <span class="detail-value">₹{order.total_amount}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Delivery Date:</span>
                            <span class="detail-value">{order.updated_at.strftime('%B %d, %Y at %I:%M %p')}</span>
                        </div>
                    </div>
                    
                    <div class="items-list">
                        <h3>Order Items</h3>
        """
        
        # Add items to email
        for item in order.items:
            html_message += f"""
                        <div class="item">
                            <strong>{item.get('name', 'N/A')}</strong> - {item.get('flavor', 'N/A')}<br>
                            Quantity: {item.get('quantity', 0)} × ₹{item.get('price', 0)} = ₹{item.get('quantity', 0) * item.get('price', 0)}
                        </div>
            """
        
        html_message += f"""
                    </div>
                    
                    <p>We hope you enjoy your delicious ice cream!</p>
                    
                    <p>Thank you for choosing Anand Ice Cream. We look forward to serving you again!</p>
                    
                    <div class="footer">
                        <p><strong>Anand Ice Cream</strong></p>
                        <p>Email: anandicecream@gmail.com | Phone: 1234567890</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create email
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.content_subtype = 'html'
        
        # Attach invoice PDF if generated successfully
        if invoice_path:
            email.attach_file(invoice_path)
            print(f"[SUCCESS] Invoice attached to email: {invoice_path}")
        
        # Send email
        email.send()
        print(f"[SUCCESS] Delivery confirmation email sent to {order.email} for order: {order.order_id}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error sending delivery confirmation email: {e}")
        return False


def send_cancellation_email(order):
    """Send cancellation email for confirmed orders"""
    try:
        subject = f'Order Cancelled - Anand Ice Cream (Order #{order.order_id})'
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ff6b9d 0%, #e84393 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .order-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .detail-label {{ font-weight: bold; color: #666; }}
                .detail-value {{ color: #333; }}
                .refund-info {{ background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107; }}
                .contact-info {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2196f3; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Order Cancelled</h1>
                    <p>We're sorry to inform you about the cancellation</p>
                </div>
                
                <div class="content">
                    <p>Dear {order.full_name},</p>
                    
                    <p>We regret to inform you that your order has been cancelled.</p>
                    
                    <div class="order-details">
                        <h3>Order Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Order ID:</span>
                            <span class="detail-value">{order.order_id}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Order Amount:</span>
                            <span class="detail-value">₹{order.total_amount}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Order Date:</span>
                            <span class="detail-value">{order.order_date.strftime('%B %d, %Y')}</span>
                        </div>
                    </div>
                    
                    <div class="refund-info">
                        <h3>💰 Refund Information</h3>
                        <p><strong>Refund Amount:</strong> ₹{order.total_amount}</p>
                        <p><strong>Processing Time:</strong> 3 working days</p>
                        <p>The refund will be processed to your original payment method within 3 working days.</p>
                    </div>
                    
                    <div class="contact-info">
                        <h3>📞 Need Help?</h3>
                        <p>If you have any questions or concerns, please feel free to contact us:</p>
                        <p><strong>Email:</strong> anandicecream@gmail.com</p>
                        <p><strong>Phone:</strong> 1234567890</p>
                    </div>
                    
                    <p>We apologize for any inconvenience caused. We hope to serve you better in the future.</p>
                    
                    <div class="footer">
                        <p><strong>Anand Ice Cream</strong></p>
                        <p>Thank you for your understanding</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create and send email
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.content_subtype = 'html'
        
        # Send email
        email.send()
        print(f"[SUCCESS] Cancellation email sent to {order.email} for order: {order.order_id}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error sending cancellation email: {e}")
        return False


def generate_invoice_pdf(order):
    """Generate professional PDF invoice for delivered order"""
    import os
    from datetime import datetime
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    
    try:
        # Create invoices directory if it doesn't exist
        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        os.makedirs(invoice_dir, exist_ok=True)
        
        # Generate invoice filename
        invoice_filename = f"INV-{order.order_id}.pdf"
        invoice_path = os.path.join(invoice_dir, invoice_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(invoice_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
        )
        
        # Company Header
        company_name = Paragraph("🍦 ANAND ICE CREAM", title_style)
        elements.append(company_name)
        
        company_info = Paragraph(
            "Email: anandicecream@gmail.com | Phone: 1234567890",
            ParagraphStyle('CompanyInfo', parent=normal_style, alignment=TA_CENTER)
        )
        elements.append(company_info)
        elements.append(Spacer(1, 20))
        
        # Invoice Title
        invoice_title = Paragraph("INVOICE", ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#00b894'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        elements.append(invoice_title)
        elements.append(Spacer(1, 20))
        
        # Invoice Details
        invoice_data = [
            ['Invoice Number:', f"INV-{order.order_id}"],
            ['Invoice Date:', datetime.now().strftime('%B %d, %Y')],
            ['Delivery Date:', order.updated_at.strftime('%B %d, %Y')],
        ]
        
        invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
        invoice_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333333')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#666666')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(invoice_table)
        elements.append(Spacer(1, 20))
        
        # Bill To Section
        bill_to_heading = Paragraph("BILL TO:", heading_style)
        elements.append(bill_to_heading)
        
        customer_info = f"""
        <b>{order.full_name}</b><br/>
        Email: {order.email}<br/>
        Phone: {order.phone}<br/>
        Address: {order.delivery_address}<br/>
        Pincode: {order.pincode}
        """
        customer_para = Paragraph(customer_info, normal_style)
        elements.append(customer_para)
        elements.append(Spacer(1, 20))
        
        # Items Table
        items_heading = Paragraph("ORDER ITEMS:", heading_style)
        elements.append(items_heading)
        elements.append(Spacer(1, 10))
        
        # Table header
        items_data = [['Product', 'Flavor', 'Quantity', 'Price', 'Amount']]
        
        # Add items
        for item in order.items:
            product_name = item.get('product', 'N/A')
            flavor = item.get('flavor', 'N/A')
            quantity = item.get('quantity', 1)
            price = float(item.get('price', 0))
            amount = quantity * price
            
            items_data.append([
                product_name,
                flavor,
                str(quantity),
                f"₹{price:.2f}",
                f"₹{amount:.2f}"
            ])
        
        # Add total row
        items_data.append(['', '', '', 'TOTAL:', f"₹{float(order.total_amount):.2f}"])
        
        # Create table
        items_table = Table(items_data, colWidths=[2*inch, 1.5*inch, 0.8*inch, 0.8*inch, 1*inch])
        items_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0, 1), (-1, -2), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
            
            # Total row
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#00b894')),
            ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#00b894')),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 30))
        
        # Payment Status
        payment_info = Paragraph(
            f"<b>Payment Status:</b> {order.get_payment_status_display()}",
            normal_style
        )
        elements.append(payment_info)
        elements.append(Spacer(1, 40))
        
        # Thank you message
        thank_you = Paragraph(
            "Thank you for your business!",
            ParagraphStyle('ThankYou', parent=heading_style, alignment=TA_CENTER, textColor=colors.HexColor('#00b894'))
        )
        elements.append(thank_you)
        elements.append(Spacer(1, 20))
        
        # Digital Signature
        signature_text = Paragraph(
            "___________________________<br/><b>Authorized Signature</b><br/>Anand Ice Cream",
            ParagraphStyle('Signature', parent=normal_style, alignment=TA_RIGHT, fontSize=9)
        )
        elements.append(signature_text)
        
        # Build PDF
        doc.build(elements)
        
        print(f"[SUCCESS] Invoice generated: {invoice_path}")
        return invoice_path
        
    except Exception as e:
        print(f"[ERROR] Error generating invoice: {e}")
        return None
