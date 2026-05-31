# Quick Start Guide

Get Karwarian.shop running in 5 minutes!

## For Ubuntu Server

### 1. Upload Files

Upload all project files to your Ubuntu server (e.g., to `/var/www/karwarian_shop`)

### 2. Run Setup Script

```bash
cd /var/www/karwarian_shop
chmod +x setup.sh
./setup.sh
```

The script will:
- Install Python dependencies
- Create virtual environment
- Set up database
- Create admin user (you'll be prompted)
- Collect static files

### 3. Start Development Server

```bash
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### 4. Access Website

- Website: `http://your-server-ip:8000`
- Admin Panel: `http://your-server-ip:8000/admin`

### 5. Add Initial Content

Login to admin panel and add:

1. **Site Statistics** (Core > Site Statistics)
   - Set beach count, matrimony profiles, events, vendors

2. **Place Categories** (Places > Place Categories)
   - Add categories like: Beaches, Forts, Islands, Temples

3. **Places** (Places > Places)
   - Add tourist attractions with photos and details

4. **News Categories** (News > News Categories)
   - Add categories like: Local News, Events, Announcements

5. **News Articles** (News > News)
   - Add local news and updates

6. **Job Categories** (Jobs > Job Categories)
   - Add categories like: IT, Healthcare, Education, etc.

7. **Jobs** (Jobs > Jobs)
   - Add job listings

8. **Service Categories** (Services > Service Categories)
   - Add categories like: Catering, Photography, Rentals, etc.

9. **Services** (Services > Services)
   - Add goods and services listings

10. **Bus Timings** (Core > Bus Timings)
    - Add bus routes and schedules

## For Production Deployment

See `DEPLOYMENT.md` for complete production setup with Nginx and Gunicorn.

## Default Admin Credentials

You'll create these during setup. Keep them secure!

## Need Help?

- Check `README.md` for detailed documentation
- Check `DEPLOYMENT.md` for production setup
- Review Django documentation: https://docs.djangoproject.com/

## Common Issues

### Port 8000 already in use

```bash
# Find and kill the process
sudo lsof -t -i tcp:8000 | xargs kill -9
```

### Permission denied

```bash
sudo chown -R $USER:$USER /var/www/karwarian_shop
```

### Module not found

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. Add your content through admin panel
2. Customize colors/styles in `static/css/style.css`
3. Add your logo and images
4. Configure email settings for contact form
5. Set up production deployment with Nginx

Enjoy your new Karwar community website! 🌊
