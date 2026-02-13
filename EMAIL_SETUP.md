# Email Setup Guide for Gmail

## Step 1: Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "How you sign in to Google", click on "2-Step Verification"
4. Follow the steps to enable 2-Step Verification (if not already enabled)

## Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. You may need to sign in again
3. Under "Select app", choose "Mail"
4. Under "Select device", choose "Other (Custom name)"
5. Enter a name like "Anand Ice Cream Server"
6. Click "Generate"
7. Google will display a 16-character password
8. **Copy this password** - you'll need it for the `.env` file

## Step 3: Update .env File

Open your `.env` file and update these lines:

```env
ADMIN_EMAIL=tyson741161@gmail.com
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

Replace:
- `your_gmail_address@gmail.com` with your Gmail address
- `xxxx xxxx xxxx xxxx` with the 16-character app password (you can include or remove spaces)

## Step 4: Test Email

After updating `.env`:
1. Restart the server: `Ctrl+C` then `npm start`
2. Place a test order
3. Check the admin email (tyson741161@gmail.com) for the order notification

## Troubleshooting

**"Invalid login"** error:
- Make sure 2-Step Verification is enabled
- Use App Password, not your regular Gmail password
- Check that EMAIL_USER and EMAIL_PASSWORD are correct in `.env`

**Email not received:**
- Check spam/junk folder
- Verify ADMIN_EMAIL is correct
- Check server logs for email errors

**"Less secure app access"** message:
- This is outdated - use App Passwords instead
- App Passwords work with 2-Step Verification

## Alternative: Use Different Email Service

If you don't want to use Gmail, you can use other services:

**SendGrid, Mailgun, etc.:**
Update the transporter configuration in `server.js`:

```javascript
const transporter = nodemailer.createTransport({
    host: 'smtp.sendgrid.net',
    port: 587,
    auth: {
        user: 'apikey',
        pass: 'your-api-key'
    }
});
```
