const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const nodemailer = require('nodemailer');
const PDFDocument = require('pdfkit');
const { createCanvas, loadImage } = require('canvas');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' })); // Increased limit for base64 images
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// PostgreSQL Connection Pool
const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'anand_ice_cream',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD
});

// Test database connection
pool.connect((err, client, release) => {
    if (err) {
        console.error('❌ Error connecting to PostgreSQL:', err.stack);
    } else {
        console.log('✅ Connected to PostgreSQL');
        release();
    }
});

// Initialize database tables
async function initializeDatabase() {
    const createTableQuery = `
        CREATE TABLE IF NOT EXISTS orders (
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
            payment_status VARCHAR(50) DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_order_id ON orders(order_id);
        CREATE INDEX IF NOT EXISTS idx_email ON orders(email);
        CREATE INDEX IF NOT EXISTS idx_status ON orders(status);
        CREATE INDEX IF NOT EXISTS idx_payment_status ON orders(payment_status);
    `;

    try {
        await pool.query(createTableQuery);
        console.log('✅ Database tables initialized');
    } catch (error) {
        console.error('❌ Error initializing database:', error);
    }
}

// Initialize database on startup
initializeDatabase();

// Generate unique order ID
function generateOrderId() {
    const timestamp = Date.now().toString(36);
    const randomStr = Math.random().toString(36).substring(2, 7);
    return `ORD-${timestamp}-${randomStr}`.toUpperCase();
}

// Convert base64 image to PDF buffer
async function convertImageToPDF(base64Image) {
    try {
        // Remove data URL prefix if present
        const base64Data = base64Image.replace(/^data:image\/\w+;base64,/, '');
        const imageBuffer = Buffer.from(base64Data, 'base64');

        // Load the image to get dimensions
        const image = await loadImage(imageBuffer);

        // Create PDF document
        const doc = new PDFDocument({
            size: [image.width, image.height],
            margins: { top: 0, bottom: 0, left: 0, right: 0 }
        });

        // Collect PDF data in chunks
        const chunks = [];
        doc.on('data', chunk => chunks.push(chunk));

        // Add image to PDF
        doc.image(imageBuffer, 0, 0, {
            width: image.width,
            height: image.height
        });

        // Finalize PDF
        doc.end();

        // Return promise that resolves with PDF buffer
        return new Promise((resolve, reject) => {
            doc.on('end', () => resolve(Buffer.concat(chunks)));
            doc.on('error', reject);
        });
    } catch (error) {
        console.error('❌ Error converting image to PDF:', error);
        throw error;
    }
}

// Email Configuration
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD
    }
});

// Function to send order email to admin
async function sendOrderEmail(orderData, orderId) {
    try {
        // Format items for email
        const itemsList = orderData.items.map(item =>
            `- ${item.product} (${item.flavor}) x${item.quantity || 1} - ₹${item.price}`
        ).join('\n');

        // Prepare email options
        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: process.env.ADMIN_EMAIL,
            subject: `🍦 New Order Received - ${orderId}`,
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #ff6b9d;">🍦 New Order Received!</h2>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #333;">Order Details</h3>
                        <p><strong>Order ID:</strong> ${orderId}</p>
                        <p><strong>Order Date:</strong> ${new Date(orderData.orderDate).toLocaleString()}</p>
                        <p><strong>Total Amount:</strong> ₹${orderData.totalAmount}</p>
                        <p><strong>Payment Status:</strong> ${orderData.paymentStatus || 'Pending Verification'}</p>
                    </div>

                    <div style="background: #fff5f8; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #333;">Customer Information</h3>
                        <p><strong>Name:</strong> ${orderData.customerInfo.fullName}</p>
                        <p><strong>Email:</strong> ${orderData.customerInfo.email}</p>
                        <p><strong>Phone:</strong> ${orderData.customerInfo.phone}</p>
                        ${orderData.customerInfo.alternatePhone ? `<p><strong>Alternate Phone:</strong> ${orderData.customerInfo.alternatePhone}</p>` : ''}
                        <p><strong>Delivery Address:</strong> ${orderData.customerInfo.deliveryAddress}</p>
                        <p><strong>Pincode:</strong> ${orderData.customerInfo.pincode}</p>
                    </div>

                    <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #333;">Order Items</h3>
                        <pre style="font-family: monospace; white-space: pre-wrap;">${itemsList}</pre>
                    </div>

                    ${orderData.paymentScreenshot ? `
                    <div style="background: #fff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #4CAF50;">
                        <h3 style="color: #333;">📎 Payment Screenshot</h3>
                        <p style="color: #666; font-size: 14px;">Payment screenshot is attached as a PDF file. Please check the attachment to view the payment proof.</p>
                    </div>
                    ` : '<p style="color: #999;">No payment screenshot provided</p>'}

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; color: #666; font-size: 12px;">
                        <p>This is an automated email from Anand Ice Cream ordering system.</p>
                    </div>
                </div>
            `,
            attachments: []
        };

        // Convert payment screenshot to PDF and attach if available
        if (orderData.paymentScreenshot) {
            try {
                const pdfBuffer = await convertImageToPDF(orderData.paymentScreenshot);
                mailOptions.attachments.push({
                    filename: `payment-screenshot-${orderId}.pdf`,
                    content: pdfBuffer,
                    contentType: 'application/pdf'
                });
                console.log(`✅ Payment screenshot converted to PDF for order: ${orderId}`);
            } catch (pdfError) {
                console.error('❌ Error converting screenshot to PDF:', pdfError);
                // Fallback: attach as image if PDF conversion fails
                const base64Data = orderData.paymentScreenshot.replace(/^data:image\/\w+;base64,/, '');
                const imageBuffer = Buffer.from(base64Data, 'base64');
                mailOptions.attachments.push({
                    filename: `payment-screenshot-${orderId}.png`,
                    content: imageBuffer,
                    contentType: 'image/png'
                });
                console.log(`⚠️ Fallback: Attached screenshot as image for order: ${orderId}`);
            }
        }

        await transporter.sendMail(mailOptions);
        console.log(`📧 Order email sent to admin for order: ${orderId}`);
        return true;
    } catch (error) {
        console.error('❌ Error sending email:', error);
        return false;
    }
}

// API Routes

// Health check
app.get('/api/health', async (req, res) => {
    try {
        await pool.query('SELECT NOW()');
        res.json({
            status: 'OK',
            message: 'Server is running',
            database: 'Connected'
        });
    } catch (error) {
        res.status(500).json({
            status: 'ERROR',
            message: 'Database connection failed',
            error: error.message
        });
    }
});

// Create new order
app.post('/api/orders', async (req, res) => {
    try {
        const { customerInfo, items, totalAmount, orderDate, status, paymentScreenshot, paymentStatus } = req.body;

        // Validation
        if (!customerInfo || !items || !totalAmount) {
            return res.status(400).json({
                error: 'Missing required fields',
                message: 'Please provide customerInfo, items, and totalAmount'
            });
        }

        if (!customerInfo.fullName || !customerInfo.email || !customerInfo.phone ||
            !customerInfo.deliveryAddress || !customerInfo.pincode) {
            return res.status(400).json({
                error: 'Incomplete customer information',
                message: 'Please provide all required customer details'
            });
        }

        if (!Array.isArray(items) || items.length === 0) {
            return res.status(400).json({
                error: 'Invalid items',
                message: 'Cart must contain at least one item'
            });
        }

        // Generate order ID
        const orderId = generateOrderId();

        // Insert order into database
        const insertQuery = `
            INSERT INTO orders (
                order_id, full_name, email, phone, delivery_address, 
                pincode, alternate_phone, items, total_amount, payment_screenshot, 
                payment_status, order_date, status
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            RETURNING *
        `;

        const values = [
            orderId,
            customerInfo.fullName,
            customerInfo.email,
            customerInfo.phone,
            customerInfo.deliveryAddress,
            customerInfo.pincode,
            customerInfo.alternatePhone || null,
            JSON.stringify(items),
            totalAmount,
            paymentScreenshot || null,
            paymentStatus || 'pending',
            orderDate || new Date(),
            status || 'pending'
        ];

        const result = await pool.query(insertQuery, values);
        const newOrder = result.rows[0];

        console.log(`✅ New order created: ${orderId} (Payment: ${paymentStatus || 'pending'})`);

        // Send email to admin
        sendOrderEmail({
            customerInfo,
            items,
            totalAmount,
            orderDate: orderDate || new Date(),
            paymentStatus: paymentStatus || 'pending',
            paymentScreenshot
        }, orderId).catch(err => console.error('Email sending failed:', err));

        res.status(201).json({
            success: true,
            message: 'Order placed successfully',
            orderId: orderId,
            order: {
                orderId: newOrder.order_id,
                customerInfo: {
                    fullName: newOrder.full_name,
                    email: newOrder.email,
                    phone: newOrder.phone,
                    deliveryAddress: newOrder.delivery_address,
                    pincode: newOrder.pincode,
                    alternatePhone: newOrder.alternate_phone
                },
                items: newOrder.items,
                totalAmount: parseFloat(newOrder.total_amount),
                paymentStatus: newOrder.payment_status,
                orderDate: newOrder.order_date,
                status: newOrder.status
            }
        });

    } catch (error) {
        console.error('❌ Error creating order:', error);
        res.status(500).json({
            error: 'Failed to create order',
            message: error.message
        });
    }
});

// Get all orders (for admin)
app.get('/api/orders', async (req, res) => {
    try {
        const query = 'SELECT * FROM orders ORDER BY created_at DESC';
        const result = await pool.query(query);

        const orders = result.rows.map(row => ({
            orderId: row.order_id,
            customerInfo: {
                fullName: row.full_name,
                email: row.email,
                phone: row.phone,
                deliveryAddress: row.delivery_address,
                pincode: row.pincode,
                alternatePhone: row.alternate_phone
            },
            items: row.items,
            totalAmount: parseFloat(row.total_amount),
            orderDate: row.order_date,
            status: row.status,
            createdAt: row.created_at
        }));

        res.json({
            success: true,
            count: orders.length,
            orders
        });
    } catch (error) {
        console.error('❌ Error fetching orders:', error);
        res.status(500).json({
            error: 'Failed to fetch orders',
            message: error.message
        });
    }
});

// Get order by ID
app.get('/api/orders/:orderId', async (req, res) => {
    try {
        const query = 'SELECT * FROM orders WHERE order_id = $1';
        const result = await pool.query(query, [req.params.orderId]);

        if (result.rows.length === 0) {
            return res.status(404).json({
                error: 'Order not found',
                message: `No order found with ID: ${req.params.orderId}`
            });
        }

        const row = result.rows[0];
        const order = {
            orderId: row.order_id,
            customerInfo: {
                fullName: row.full_name,
                email: row.email,
                phone: row.phone,
                deliveryAddress: row.delivery_address,
                pincode: row.pincode,
                alternatePhone: row.alternate_phone
            },
            items: row.items,
            totalAmount: parseFloat(row.total_amount),
            orderDate: row.order_date,
            status: row.status,
            createdAt: row.created_at
        };

        res.json({
            success: true,
            order
        });
    } catch (error) {
        console.error('❌ Error fetching order:', error);
        res.status(500).json({
            error: 'Failed to fetch order',
            message: error.message
        });
    }
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM signal received: closing HTTP server');
    pool.end(() => {
        console.log('PostgreSQL pool closed');
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log(`📊 Database: PostgreSQL at ${process.env.DB_HOST || 'localhost'}:${process.env.DB_PORT || 5432}`);
});
