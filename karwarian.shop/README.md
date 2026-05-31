# Karwarian.shop - Django Website

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A complete community portal for Karwar, Karnataka (ಕಾರವಾರ) - God's Own Coast. This Django-based website replicates and enhances karwarian.shop with features for tourism, news, matrimony, jobs, and local services.

## ✨ Features

### 🏠 Home Page
- Beautiful hero section with gradient background
- Live statistics (beaches, matrimony profiles, events, vendors)
- Feature cards for all sections
- Fully responsive design

### 🏖️ Places to Visit
- Browse beaches, forts, islands, and temples
- Category filtering and search
- Detailed pages with images, location, timings
- Google Maps integration
- View counter and featured places

### 📰 News Section
- Local news and updates
- Category filtering
- Featured/breaking news
- Related articles
- Admin content management

### 💑 Matrimony
- Profile listings with filters
- Detailed profiles (login required)
- Verification system
- Contact information
- Privacy-focused design

### 💼 Jobs
- Job listings with advanced filters
- Company information
- Salary ranges
- Application contact details
- Featured jobs

### 🛒 Goods & Services
- Function services, goods, second-hand items
- Category and type filtering
- Seller contact information
- WhatsApp integration
- Verified sellers

### 🚌 Bus Timings
- Route schedules
- Filter by locations
- Bus type information
- Easy-to-read timetable

### 📞 Additional Pages
- About Karwar
- Contact form
- Help and support

## 🚀 Quick Start

### Windows
```cmd
# Run setup script
setup.bat

# Or double-click START_SERVER.bat to start later
```

### Ubuntu/Linux
```bash
# Run setup script
chmod +x setup.sh
./setup.sh
```

### Manual Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

**Access:**
- Website: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Detailed installation for all platforms
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment with Nginx & Gunicorn
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview

## 🛠️ Technology Stack

- **Backend:** Django 4.2+
- **Frontend:** Bootstrap 5, Font Awesome 6
- **Database:** SQLite (dev), PostgreSQL/MySQL ready
- **Server:** Gunicorn + Nginx (production)
- **Python:** 3.8+

## 📁 Project Structure

```
karwarian_shop/
├── core/                    # Home, about, contact, bus timings
├── places/                  # Tourist attractions
├── news/                    # News articles
├── matrimony/               # Matrimony profiles
├── jobs/                    # Job listings
├── services/                # Goods and services
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # User uploads
└── karwarian_shop/          # Project settings
```

## 🎨 Screenshots

### Home Page
- Hero section with welcome message
- Statistics cards with hover effects
- Feature cards for all sections

### Places to Visit
- Grid layout with images
- Category filtering
- Detailed place pages with gallery

### Admin Panel
- Complete content management
- User-friendly interface
- Bulk operations support

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### Admin Panel
Access at `/admin` to manage:
- ✅ Site statistics
- ✅ Places and categories
- ✅ News articles
- ✅ Matrimony profiles
- ✅ Job listings
- ✅ Services and goods
- ✅ Bus timings
- ✅ Contact messages

## 🚀 Production Deployment

### Ubuntu Server with Nginx

```bash
# 1. Upload files to server
scp -r karwarian_shop user@server:/var/www/

# 2. Run setup
cd /var/www/karwarian_shop
./setup.sh

# 3. Install Gunicorn
pip install gunicorn

# 4. Configure Nginx (see DEPLOYMENT.md)

# 5. Setup SSL with Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete production setup guide.

## 📝 Adding Content

1. Login to admin panel: http://your-site.com/admin
2. Add **Site Statistics** (Core > Site Statistics)
3. Create **Categories** for places, news, jobs, services
4. Add **Content** for each section
5. Upload **Images** for places and services
6. Configure **Bus Timings**

## 🔒 Security Features

- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Secure password hashing
- ✅ Login required for sensitive data
- ✅ Environment-based configuration

## 📱 Responsive Design

- ✅ Mobile-first approach
- ✅ Bootstrap 5 grid system
- ✅ Touch-friendly interfaces
- ✅ Optimized for all screen sizes

## 🤝 Contributing

This is a custom project for Karwar community. For modifications:

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- Check **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** for setup issues
- Review **[DEPLOYMENT.md](DEPLOYMENT.md)** for production problems
- See **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** for project overview
- Visit [Django Documentation](https://docs.djangoproject.com/)

## 🎯 Roadmap

Current version includes all core features. Future enhancements could include:
- User registration system
- Email notifications
- Payment integration
- Mobile app API
- Multi-language support (Kannada/English)
- Advanced search
- Review and rating system

## 👥 Credits

- **Original Website:** karwarian.shop
- **Framework:** Django
- **UI Framework:** Bootstrap 5
- **Icons:** Font Awesome 6

## 📞 Contact

For questions or support regarding this project, please use the contact form on the website or reach out through the admin panel.

---

**Made with ❤️ for Karwar (ಕಾರವಾರ) - God's Own Coast**

🌊 Discover the pearl of coastal Karnataka — pristine beaches, vibrant community, and rich culture all in one place.
