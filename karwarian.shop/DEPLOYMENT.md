# Production Deployment Guide for Ubuntu Server

This guide will help you deploy Karwarian.shop on an Ubuntu server using Gunicorn and Nginx.

## Prerequisites

- Ubuntu 20.04 or later
- Root or sudo access
- Domain name (optional, but recommended)

## Step 1: Initial Server Setup

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv nginx git
```

## Step 2: Clone and Setup Project

```bash
# Navigate to your preferred directory
cd /var/www

# Clone or upload your project
# If using git:
# git clone your-repo-url karwarian_shop

# Or upload files via SCP/SFTP to /var/www/karwarian_shop

# Navigate to project directory
cd karwarian_shop

# Run setup script
chmod +x setup.sh
./setup.sh
```

## Step 3: Configure Environment

Edit the `.env` file:

```bash
nano .env
```

Update these settings for production:

```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
```

## Step 4: Install and Configure Gunicorn

```bash
# Activate virtual environment
source venv/bin/activate

# Install Gunicorn
pip install gunicorn

# Test Gunicorn
gunicorn karwarian_shop.wsgi:application --bind 0.0.0.0:8000
```

If it works, press Ctrl+C to stop it.

## Step 5: Create Gunicorn Systemd Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/karwarian.service
```

Add the following content:

```ini
[Unit]
Description=Karwarian.shop Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/karwarian_shop
Environment="PATH=/var/www/karwarian_shop/venv/bin"
ExecStart=/var/www/karwarian_shop/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/karwarian_shop/karwarian.sock \
          karwarian_shop.wsgi:application

[Install]
WantedBy=multi-user.target
```

Set proper permissions:

```bash
sudo chown -R www-data:www-data /var/www/karwarian_shop
```

Start and enable the service:

```bash
sudo systemctl start karwarian
sudo systemctl enable karwarian
sudo systemctl status karwarian
```

## Step 6: Configure Nginx

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/karwarian
```

Add the following content:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/karwarian_shop/staticfiles/;
    }

    location /media/ {
        alias /var/www/karwarian_shop/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/karwarian_shop/karwarian.sock;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/karwarian /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 7: Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Step 8: SSL Certificate (Optional but Recommended)

Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
```

Obtain SSL certificate:

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts. Certbot will automatically configure Nginx for HTTPS.

## Step 9: Create Initial Data

Access your admin panel at `https://your-domain.com/admin` and create:

1. Site Statistics (Core > Site Statistics)
2. Place Categories (Places > Place Categories)
3. News Categories (News > News Categories)
4. Job Categories (Jobs > Job Categories)
5. Service Categories (Services > Service Categories)

Then add content for each section.

## Maintenance Commands

### Restart Services

```bash
sudo systemctl restart karwarian
sudo systemctl restart nginx
```

### View Logs

```bash
# Gunicorn logs
sudo journalctl -u karwarian -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Update Application

```bash
cd /var/www/karwarian_shop
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart karwarian
```

### Backup Database

```bash
cd /var/www/karwarian_shop
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### Restore Database

```bash
python manage.py loaddata backup_20260528.json
```

## Troubleshooting

### 502 Bad Gateway

Check Gunicorn service:
```bash
sudo systemctl status karwarian
sudo journalctl -u karwarian -n 50
```

### Static Files Not Loading

```bash
cd /var/www/karwarian_shop
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Permission Issues

```bash
sudo chown -R www-data:www-data /var/www/karwarian_shop
sudo chmod -R 755 /var/www/karwarian_shop
```

## Security Recommendations

1. Keep DEBUG=False in production
2. Use strong SECRET_KEY
3. Regular backups of database and media files
4. Keep system and packages updated
5. Use SSL/HTTPS
6. Configure proper firewall rules
7. Regular security audits

## Performance Optimization

1. Enable Nginx caching
2. Use CDN for static files
3. Optimize database queries
4. Enable gzip compression
5. Use Redis for caching (optional)

For more help, visit the Django documentation: https://docs.djangoproject.com/
