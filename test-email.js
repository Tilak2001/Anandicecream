// Test email configuration
const nodemailer = require('nodemailer');
require('dotenv').config();

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD
    }
});

async function testEmail() {
    try {
        console.log('Testing email configuration...');
        console.log('EMAIL_USER:', process.env.EMAIL_USER);
        console.log('ADMIN_EMAIL:', process.env.ADMIN_EMAIL);
        console.log('EMAIL_PASSWORD:', process.env.EMAIL_PASSWORD ? '***configured***' : 'NOT SET');

        const info = await transporter.sendMail({
            from: process.env.EMAIL_USER,
            to: process.env.ADMIN_EMAIL,
            subject: '🧪 Test Email - Anand Ice Cream',
            html: '<h1>Test Email</h1><p>If you receive this, email is working correctly!</p>'
        });

        console.log('✅ Email sent successfully!');
        console.log('Message ID:', info.messageId);
        console.log('Check inbox:', process.env.ADMIN_EMAIL);
    } catch (error) {
        console.error('❌ Email failed:', error.message);
        console.error('Full error:', error);
    }
}

testEmail();
