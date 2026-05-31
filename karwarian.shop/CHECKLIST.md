# Karwarian.shop - Deployment Checklist

Use this checklist to ensure everything is set up correctly.

## ✅ Initial Setup

### Installation
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example`
- [ ] SECRET_KEY generated and set in `.env`
- [ ] Database migrations run (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Development server starts without errors

### Access Verification
- [ ] Home page loads at http://localhost:8000
- [ ] Admin panel accessible at http://localhost:8000/admin
- [ ] Can login with superuser credentials
- [ ] All navigation links work
- [ ] Static files (CSS, images) load correctly

## 📝 Content Setup

### Core Configuration
- [ ] Site Statistics added (Core > Site Statistics)
  - [ ] Beaches count set
  - [ ] Matrimony profiles count set
  - [ ] Events per year set
  - [ ] Local vendors count set

### Places to Visit
- [ ] Place Categories created
  - [ ] Beaches category
  - [ ] Forts category
  - [ ] Islands category
  - [ ] Temples category
  - [ ] Other categories as needed
- [ ] At least 3-5 places added with:
  - [ ] Name and description
  - [ ] Images uploaded
  - [ ] Location details
  - [ ] Timings and entry fees
  - [ ] Category assigned

### News Section
- [ ] News Categories created
  - [ ] Local News
  - [ ] Events
  - [ ] Announcements
  - [ ] Other categories
- [ ] At least 3-5 news articles added with:
  - [ ] Title and content
  - [ ] Images
  - [ ] Category assigned
  - [ ] Published date set

### Matrimony
- [ ] Sample profiles created (optional for testing)
- [ ] Verification system understood
- [ ] Privacy settings configured

### Jobs
- [ ] Job Categories created
  - [ ] IT/Software
  - [ ] Healthcare
  - [ ] Education
  - [ ] Hospitality
  - [ ] Other categories
- [ ] Sample job listings added with:
  - [ ] Job title and description
  - [ ] Company information
  - [ ] Location and salary
  - [ ] Contact details

### Services
- [ ] Service Categories created
  - [ ] Catering
  - [ ] Photography
  - [ ] Decorations
  - [ ] Rentals
  - [ ] Other categories
- [ ] Sample services added with:
  - [ ] Service name and description
  - [ ] Images
  - [ ] Pricing
  - [ ] Contact information

### Bus Timings
- [ ] Bus routes added with:
  - [ ] Route names
  - [ ] From/To locations
  - [ ] Departure/Arrival times
  - [ ] Bus types
  - [ ] Frequency

### Other Pages
- [ ] About page content reviewed
- [ ] Contact page tested
- [ ] Contact form submissions working

## 🎨 Customization

### Branding
- [ ] Logo added/replaced in templates
- [ ] Favicon added
- [ ] Color scheme customized in `static/css/style.css`
- [ ] Footer information updated
- [ ] Social media links updated

### Content
- [ ] All placeholder text replaced
- [ ] Contact information updated
- [ ] About page customized
- [ ] Images optimized for web

## 🔒 Security (Production)

### Environment
- [ ] DEBUG set to False in `.env`
- [ ] Strong SECRET_KEY generated
- [ ] ALLOWED_HOSTS configured with domain
- [ ] Database credentials secured

### Server
- [ ] Firewall configured (UFW)
- [ ] SSH key authentication enabled
- [ ] Root login disabled
- [ ] Regular backups scheduled

## 🚀 Production Deployment (Ubuntu)

### Server Setup
- [ ] Ubuntu server provisioned
- [ ] Domain name configured (optional)
- [ ] DNS records set up
- [ ] SSH access configured

### Application
- [ ] Files uploaded to `/var/www/karwarian_shop`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Static files collected
- [ ] Media directory permissions set

### Gunicorn
- [ ] Gunicorn installed
- [ ] Systemd service file created
- [ ] Service started and enabled
- [ ] Service running without errors

### Nginx
- [ ] Nginx installed
- [ ] Site configuration created
- [ ] Configuration tested (`nginx -t`)
- [ ] Nginx restarted
- [ ] Site accessible via domain/IP

### SSL/HTTPS
- [ ] Certbot installed
- [ ] SSL certificate obtained
- [ ] HTTPS working
- [ ] HTTP redirects to HTTPS
- [ ] Auto-renewal configured

## 🧪 Testing

### Functionality
- [ ] All pages load correctly
- [ ] Navigation works
- [ ] Search functionality works
- [ ] Filters work on listing pages
- [ ] Forms submit successfully
- [ ] Admin panel accessible
- [ ] Content can be added/edited/deleted

### Responsive Design
- [ ] Mobile view tested
- [ ] Tablet view tested
- [ ] Desktop view tested
- [ ] Images scale properly
- [ ] Navigation menu works on mobile

### Performance
- [ ] Page load times acceptable
- [ ] Images optimized
- [ ] Static files cached
- [ ] Database queries optimized

### Browser Compatibility
- [ ] Chrome/Edge tested
- [ ] Firefox tested
- [ ] Safari tested (if available)
- [ ] Mobile browsers tested

## 📊 Monitoring

### Logs
- [ ] Gunicorn logs accessible
- [ ] Nginx logs accessible
- [ ] Django logs configured
- [ ] Error monitoring set up

### Backups
- [ ] Database backup script created
- [ ] Media files backup configured
- [ ] Backup schedule set
- [ ] Backup restoration tested

## 📱 Optional Enhancements

### Features
- [ ] Email notifications configured
- [ ] Social media integration
- [ ] Analytics added (Google Analytics)
- [ ] SEO optimization
- [ ] Sitemap generated
- [ ] robots.txt configured

### Performance
- [ ] CDN configured for static files
- [ ] Database indexing optimized
- [ ] Caching implemented (Redis/Memcached)
- [ ] Image compression automated

## 🎉 Launch

### Pre-Launch
- [ ] All content reviewed
- [ ] All links tested
- [ ] Contact information verified
- [ ] Legal pages added (Privacy Policy, Terms)
- [ ] Final testing completed

### Launch Day
- [ ] DNS propagation verified
- [ ] SSL certificate active
- [ ] All services running
- [ ] Monitoring active
- [ ] Backup verified

### Post-Launch
- [ ] User feedback collected
- [ ] Issues tracked and resolved
- [ ] Content regularly updated
- [ ] Performance monitored
- [ ] Security updates applied

## 📞 Support Contacts

- **Technical Issues:** Check logs and documentation
- **Django Help:** https://docs.djangoproject.com/
- **Server Issues:** Check systemd and nginx logs
- **Emergency:** Have backup and rollback plan ready

---

## Quick Commands Reference

### Development
```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Production
```bash
# Restart services
sudo systemctl restart karwarian
sudo systemctl restart nginx

# View logs
sudo journalctl -u karwarian -f
sudo tail -f /var/log/nginx/error.log

# Backup database
python manage.py dumpdata > backup.json
```

---

**Use this checklist to ensure nothing is missed during setup and deployment!**
