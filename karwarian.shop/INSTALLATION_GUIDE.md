## Installation Guide

Complete installation instructions for different platforms.

---

## 🪟 Windows Installation

### Prerequisites
- Python 3.8 or higher ([Download](https://www.python.org/downloads/))
- Git (optional)

### Steps

1. **Extract or Clone Project**
   ```cmd
   cd C:\path\to\karwarian.shop
   ```

2. **Run Setup Script**
   ```cmd
   setup.bat
   ```
   
   The script will:
   - Create virtual environment
   - Install dependencies
   - Setup database
   - Prompt you to create admin user
   - Collect static files
   - Start the server

3. **Access Website**
   - Website: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

### Manual Installation (Windows)

If the script doesn't work:

```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver
```

### Starting Server Later

Double-click `START_SERVER.bat` or run:
```cmd
venv\Scripts\activate
python manage.py runserver
```

---

## 🐧 Ubuntu/Linux Installation

### Prerequisites
- Ubuntu 20.04 or later
- Python 3.8+ (usually pre-installed)

### Quick Setup

```bash
# Navigate to project directory
cd /path/to/karwarian_shop

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Manual Installation (Linux)

```bash
# Install Python and pip (if needed)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file
nano .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Starting Server Later

```bash
cd /path/to/karwarian_shop
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

## 🍎 macOS Installation

### Prerequisites
- Python 3.8+ ([Download](https://www.python.org/downloads/mac-osx/))
- Xcode Command Line Tools

### Steps

```bash
# Install Xcode Command Line Tools (if needed)
xcode-select --install

# Navigate to project
cd /path/to/karwarian_shop

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver
```

---

## 🚀 Production Deployment (Ubuntu Server)

See `DEPLOYMENT.md` for complete production setup with:
- Gunicorn
- Nginx
- SSL/HTTPS
- Systemd service
- Firewall configuration

Quick production setup:

```bash
# Upload files to server
scp -r karwarian_shop user@server:/var/www/

# SSH into server
ssh user@server

# Navigate to project
cd /var/www/karwarian_shop

# Run setup
chmod +x setup.sh
./setup.sh

# Follow DEPLOYMENT.md for Nginx and Gunicorn setup
```

---

## 📝 Post-Installation Steps

### 1. Access Admin Panel

Visit `http://your-server:8000/admin` and login with the superuser credentials you created.

### 2. Add Initial Data

#### Site Statistics
1. Go to **Core > Site Statistics**
2. Click **Add Site Statistics**
3. Set values:
   - Beaches count: 12
   - Matrimony profiles: 500
   - Events per year: 50
   - Local vendors: 200

#### Place Categories
1. Go to **Places > Place Categories**
2. Add categories:
   - Name: Beaches, Slug: beaches, Icon: 🏖️
   - Name: Forts, Slug: forts, Icon: 🏰
   - Name: Islands, Slug: islands, Icon: 🏝️
   - Name: Temples, Slug: temples, Icon: 🛕

#### Add Places
1. Go to **Places > Places**
2. Click **Add Place**
3. Fill in details and upload images

#### News Categories
1. Go to **News > News Categories**
2. Add categories like: Local News, Events, Announcements

#### Job Categories
1. Go to **Jobs > Job Categories**
2. Add categories like: IT, Healthcare, Education, Hospitality

#### Service Categories
1. Go to **Services > Service Categories**
2. Add categories like: Catering, Photography, Decorations, Rentals

### 3. Customize

- Edit `static/css/style.css` for custom styling
- Replace placeholder images in `static/images/`
- Update contact information in templates
- Modify colors and branding as needed

---

## 🔧 Troubleshooting

### Port Already in Use

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Error

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Then install requirements
pip install -r requirements.txt
```

### Database Errors

```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Permission Denied (Linux)

```bash
sudo chown -R $USER:$USER /path/to/karwarian_shop
chmod +x setup.sh
```

---

## 📚 Additional Resources

- **Quick Start**: See `QUICKSTART.md`
- **Production Deployment**: See `DEPLOYMENT.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`
- **Django Documentation**: https://docs.djangoproject.com/

---

## 🆘 Getting Help

If you encounter issues:

1. Check error messages carefully
2. Ensure virtual environment is activated
3. Verify Python version: `python --version` (should be 3.8+)
4. Check if all dependencies are installed: `pip list`
5. Review Django logs for detailed errors

---

## ✅ Verification

After installation, verify everything works:

1. ✓ Home page loads at http://localhost:8000
2. ✓ Admin panel accessible at http://localhost:8000/admin
3. ✓ Can login with superuser credentials
4. ✓ Can add content through admin panel
5. ✓ All navigation links work
6. ✓ Static files (CSS, images) load correctly

---

**Congratulations! Your Karwarian.shop website is ready! 🎉**
