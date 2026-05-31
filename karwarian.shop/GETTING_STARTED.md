# 🚀 Getting Started with Karwarian.shop

Welcome! This guide will help you get your Karwar community website up and running quickly.

## 📋 What You Have

A complete Django website with:
- ✅ Home page with statistics
- ✅ Places to visit section
- ✅ News section
- ✅ Matrimony profiles
- ✅ Job listings
- ✅ Goods & services marketplace
- ✅ Bus timings
- ✅ Admin panel for content management
- ✅ Responsive design (mobile, tablet, desktop)

## 🎯 Choose Your Path

### Path 1: Quick Test (5 minutes)
**Goal:** See the website running locally

**Windows:**
```cmd
1. Double-click setup.bat
2. Follow prompts to create admin user
3. Website opens automatically
```

**Ubuntu/Linux:**
```bash
1. chmod +x setup.sh
2. ./setup.sh
3. Follow prompts
4. Visit http://localhost:8000
```

### Path 2: Production Deployment (30 minutes)
**Goal:** Deploy to Ubuntu server with domain

1. Read **DEPLOYMENT.md**
2. Upload files to server
3. Run setup.sh
4. Configure Nginx
5. Setup SSL certificate
6. Add content via admin panel

### Path 3: Development Setup (15 minutes)
**Goal:** Set up for customization and development

1. Read **INSTALLATION_GUIDE.md**
2. Create virtual environment
3. Install dependencies
4. Run migrations
5. Start development server
6. Begin customizing

## 📚 Documentation Guide

**Start Here:**
- `README.md` - Overview and features
- `QUICKSTART.md` - 5-minute setup

**Installation:**
- `INSTALLATION_GUIDE.md` - Detailed setup for all platforms
- `setup.sh` / `setup.bat` - Automated setup scripts

**Deployment:**
- `DEPLOYMENT.md` - Production deployment guide
- `CHECKLIST.md` - Deployment checklist

**Reference:**
- `PROJECT_SUMMARY.md` - Complete project overview
- `PROJECT_STRUCTURE.txt` - File structure

## 🎬 Quick Start Steps

### Step 1: Install (Choose One)

**Option A - Automated (Recommended):**
```bash
# Ubuntu/Linux
./setup.sh

# Windows
setup.bat
```

**Option B - Manual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Step 2: Access

- **Website:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin

### Step 3: Add Content

Login to admin panel and add:

1. **Site Statistics** (Core > Site Statistics)
   - Beaches: 12
   - Matrimony Profiles: 500
   - Events/Year: 50
   - Local Vendors: 200

2. **Place Categories** (Places > Place Categories)
   - Beaches 🏖️
   - Forts 🏰
   - Islands 🏝️
   - Temples 🛕

3. **Places** (Places > Places)
   - Add 3-5 tourist attractions
   - Upload images
   - Add location details

4. **News Categories** (News > News Categories)
   - Local News
   - Events
   - Announcements

5. **News Articles** (News > News)
   - Add 3-5 news articles
   - Upload images
   - Set published date

6. **Job Categories** (Jobs > Job Categories)
   - IT/Software
   - Healthcare
   - Education
   - Hospitality

7. **Service Categories** (Services > Service Categories)
   - Catering
   - Photography
   - Decorations
   - Rentals

8. **Bus Timings** (Core > Bus Timings)
   - Add bus routes
   - Set schedules

### Step 4: Customize

1. **Logo & Branding:**
   - Replace logo in `templates/base.html`
   - Update colors in `static/css/style.css`

2. **Contact Information:**
   - Update footer in `templates/base.html`
   - Update contact page

3. **About Page:**
   - Edit `templates/core/about.html`

## 🔧 Common Tasks

### Start Server
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Start server
python manage.py runserver
```

### Create Admin User
```bash
python manage.py createsuperuser
```

### Add New Content
1. Go to http://localhost:8000/admin
2. Login with admin credentials
3. Click on the section you want to add content to
4. Click "Add" button
5. Fill in the form
6. Click "Save"

### Update Existing Content
1. Go to admin panel
2. Click on the section
3. Click on the item to edit
4. Make changes
5. Click "Save"

### Upload Images
1. In admin panel, go to the item
2. Click "Choose File" for image field
3. Select image from your computer
4. Click "Save"

## 🎨 Customization Tips

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;  /* Change this */
    --secondary-color: #764ba2; /* And this */
}
```

### Add Your Logo
Replace the icon in `templates/base.html`:
```html
<a class="navbar-brand" href="{% url 'home' %}">
    <img src="{% static 'images/logo.png' %}" alt="Logo">
    Karwarian.shop
</a>
```

### Update Footer
Edit `templates/base.html` footer section

### Modify Home Page
Edit `templates/core/home.html`

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
source venv/bin/activate  # Activate venv first
pip install -r requirements.txt
```

### Database Errors
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## 📞 Need Help?

1. **Check Documentation:**
   - README.md
   - INSTALLATION_GUIDE.md
   - DEPLOYMENT.md

2. **Check Logs:**
   - Terminal output
   - Browser console (F12)

3. **Common Issues:**
   - Virtual environment not activated
   - Wrong Python version
   - Missing dependencies
   - Port already in use

## 🎯 Next Steps

### For Testing:
1. ✅ Run setup script
2. ✅ Access website
3. ✅ Login to admin
4. ✅ Add sample content
5. ✅ Test all features

### For Production:
1. ✅ Complete local setup
2. ✅ Add all content
3. ✅ Test thoroughly
4. ✅ Read DEPLOYMENT.md
5. ✅ Deploy to server
6. ✅ Configure domain
7. ✅ Setup SSL
8. ✅ Go live!

### For Development:
1. ✅ Complete local setup
2. ✅ Study project structure
3. ✅ Customize templates
4. ✅ Modify styles
5. ✅ Add new features
6. ✅ Test changes
7. ✅ Deploy updates

## 🎉 You're Ready!

Your Karwarian.shop website is ready to use. Choose your path above and get started!

**Quick Links:**
- 📖 [README.md](README.md) - Full documentation
- ⚡ [QUICKSTART.md](QUICKSTART.md) - 5-minute guide
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- ✅ [CHECKLIST.md](CHECKLIST.md) - Deployment checklist

---

**Made with ❤️ for Karwar (ಕಾರವಾರ)**

🌊 Welcome to God's Own Coast!
