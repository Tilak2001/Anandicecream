# Anand Ice Cream - Django Application

A modern ice cream ordering system built with Django backend and vanilla JavaScript frontend, featuring admin order management, email notifications, and payment processing.

## Features

### Customer Features
- Browse ice cream products with flavors and pricing
- Add items to cart with quantity selection
- Checkout with customer information form
- Payment via QR code with screenshot upload
- Order confirmation and tracking

### Admin Features
- Secure admin login (username: `admin`, password: `admin`)
- Admin dashboard with order statistics
- View and manage pending orders
- Accept/Reject orders with automated email notifications
- Order status tracking (pending, confirmed, delivered, cancelled)

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Tilak2001/Anandicecream.git
cd Anandicecream
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

**Start PostgreSQL Service:**
```bash
# Windows - PostgreSQL runs as a service automatically

# Mac
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

**Create Database:**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE anand_ice_cream;

# Exit
\q
```

### 5. Configure Environment Variables

Update `.env` file with your credentials:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=anand_ice_cream
DB_USER=postgres
DB_PASSWORD=your_password

# Email Configuration (Gmail)
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=admin_email@gmail.com
```

**Note:** For Gmail, use an App Password (not your regular password):
1. Go to https://myaccount.google.com/apppasswords
2. Generate a new app password
3. Use that password in `EMAIL_PASSWORD`

### 6. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## Application Structure

```
anand_ice_cream/          # Django project settings
├── settings.py           # Configuration
├── urls.py              # Main URL routing
└── wsgi.py              # WSGI config

orders/                   # Main Django app
├── models.py            # Order model
├── views.py             # API and page views
├── urls.py              # API endpoints
├── utils.py             # Email utilities
└── serializers.py       # DRF serializers

templates/               # HTML templates
├── index.html          # Home page
├── cart.html           # Shopping cart
├── payment.html        # Payment page
├── admin_login.html    # Admin login
├── admin_dashboard.html # Admin dashboard
└── pending_orders.html  # Order management

static/                  # Static files
├── css/                # Stylesheets
├── js/                 # JavaScript
└── images/             # Product images

media/                   # User uploads
└── payment_screenshots/ # Payment proofs
```

## Database Schema

### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    delivery_address TEXT NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    alternate_phone VARCHAR(20),
    items JSONB NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_screenshot TEXT,
    payment_status VARCHAR(20) DEFAULT 'pending',
    status VARCHAR(20) DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Public Endpoints
- `GET /api/health/` - Health check
- `POST /api/orders/` - Create new order
- `GET /api/orders/` - List all orders
- `GET /api/orders/<order_id>/` - Get specific order

### Admin Endpoints
- `POST /api/admin/login/` - Admin authentication
- `POST /api/orders/<order_id>/update-status/` - Accept/reject orders

### Pages
- `/` - Home page
- `/cart.html` - Shopping cart
- `/payment.html` - Payment page
- `/admin-login.html` - Admin login
- `/admin-dashboard.html` - Admin dashboard
- `/pending-orders.html` - Order management

## Admin Access

**Login Credentials:**
- Username: `admin`
- Password: `admin`

**Admin Features:**
1. View order statistics (total, pending, confirmed, delivered)
2. Monitor total revenue
3. View recent orders
4. Manage pending orders
5. Accept orders (sends confirmation email)
6. Reject orders (sends cancellation email with refund info)

## Email Notifications

### Order Acceptance Email
- Subject: "Order Confirmed - Anand Ice Cream"
- Contains: Order details, items, delivery message
- Sent to: Customer email

### Order Rejection Email
- Subject: "Order Cancelled - Anand Ice Cream"
- Contains: Order details, refund information (3 working days)
- Contact: anandicecream@gmail.com, 1234567890
- Sent to: Customer email

### Admin Notification Email
- Subject: "New Order Received"
- Contains: Full order details, customer info, payment screenshot (PDF)
- Sent to: Admin email (configured in .env)

## Usage Guide

### For Customers

1. **Browse Products**
   - Visit http://localhost:8000
   - View ice cream products with flavors and prices

2. **Add to Cart**
   - Select product and flavor
   - Click "Add to Cart"
   - View cart icon for item count

3. **Checkout**
   - Go to cart page
   - Review items
   - Click "Proceed to Checkout"
   - Fill in delivery details

4. **Payment**
   - Scan QR code
   - Make payment
   - Upload payment screenshot
   - Submit order

### For Admins

1. **Login**
   - Go to http://localhost:8000/admin-login.html
   - Enter credentials (admin/admin)

2. **View Dashboard**
   - See order statistics
   - Monitor revenue
   - View recent orders

3. **Manage Orders**
   - Click "Pending Orders" card
   - View order details
   - Accept or reject orders
   - Customers receive email notifications

## Troubleshooting

### Server won't start
- Ensure PostgreSQL is running
- Check `.env` file credentials
- Verify virtual environment is activated

### Database connection error
- Verify PostgreSQL service is running
- Check database name and credentials
- Ensure database `anand_ice_cream` exists

### Email not sending
- Verify Gmail App Password is correct
- Check EMAIL_USER and EMAIL_PASSWORD in `.env`
- Ensure "Less secure app access" is enabled (if not using App Password)

### Admin page 404 error
- Restart Django server: `Ctrl+C` then `python manage.py runserver`
- Clear browser cache
- Check URL: http://localhost:8000/admin-login.html

### Orders not saving
- Check browser console for errors
- Verify server is running
- Check server logs for database errors

## PostgreSQL Commands

```bash
# Connect to database
psql -U postgres -d anand_ice_cream

# View all orders
SELECT * FROM orders ORDER BY created_at DESC;

# View pending orders
SELECT * FROM orders WHERE status = 'pending';

# View order statistics
SELECT status, COUNT(*) as count, SUM(total_amount) as total
FROM orders
GROUP BY status;

# Exit
\q
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Superuser (Django Admin)
```bash
python manage.py createsuperuser
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Technology Stack

- **Backend:** Django 5.0.1, Django REST Framework
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Email:** Django Email (SMTP)
- **PDF Generation:** ReportLab, Pillow

## Security Notes

- Change default admin credentials in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Set `DEBUG = False` in production
- Configure ALLOWED_HOSTS properly

## License

This project is for educational purposes.

## Contact

For support or queries:
- Email: anandicecream@gmail.com
- Phone: 1234567890

## Contributors
hi bsdman

- Tilak Pednekar