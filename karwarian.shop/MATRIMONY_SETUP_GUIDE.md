# Matrimony Profile System - Setup Guide

## Overview
A complete matrimony profile management system has been implemented with:
- User-facing profile submission form
- Admin approval workflow
- Admin dashboard for profile management
- Profile listing with filtering by caste/community

## Changes Made

### 1. Database Model (`core/models.py`)
Added `MatrimonyProfile` model with fields:
- Basic info: full_name, father_name, age, gender, height, caste
- Education: qualification, occupation
- Contact: contact_phone, contact_email, address
- Admin: is_approved (default False), is_active, timestamps

### 2. Admin Interface (`core/admin.py`)
Registered `MatrimonyProfile` with:
- List display with approval status
- Inline editing for approval/active status
- Filtering by approval, gender, caste
- Organized fieldsets

### 3. Views (`core/views.py`)
Added views:
- `matrimony_list`: Public listing (only approved profiles)
- `matrimony_add`: User submission form (requires approval)

### 4. Dashboard Views (`core/dashboard_views.py`)
Added admin dashboard views:
- `matrimony_dashboard_list`: List all profiles with status filters
- `matrimony_dashboard_add`: Admin can manually add profiles (auto-approved)
- `matrimony_dashboard_update_status`: AJAX endpoint for approval/status changes
- `matrimony_dashboard_delete`: Delete profiles

### 5. URLs (`core/urls.py`)
Added routes:
- `/matrimony/` - Public profile listing
- `/matrimony/add/` - User submission
- `/dashboard/matrimony/` - Admin profile management
- `/dashboard/matrimony/add/` - Admin add profile
- `/dashboard/matrimony/<id>/update-status/` - AJAX status update
- `/dashboard/matrimony/<id>/delete/` - Delete profile

### 6. Templates Created

#### `templates/core/matrimony_list.html`
- Beautiful profile cards with gradient headers
- Filter by caste/community dropdown
- "Add Profile" button opens modal form
- User submissions require admin approval
- Contact information display

#### `templates/dashboard/matrimony_list.html`
- Admin dashboard for profile moderation
- Tabs: Pending Approval, Approved, Inactive, All
- Approve/Disapprove buttons
- Activate/Deactivate toggle
- Delete functionality
- Shows submission date and contact info

#### `templates/dashboard/matrimony_form.html`
- Admin form to manually add profiles
- Organized sections: Basic Info, Education, Contact
- Auto-approved when added by admin
- Responsive grid layout

### 7. Navigation Updates
- Updated `templates/core/home.html` - Fixed matrimony card link
- Updated `templates/dashboard/base.html` - Added matrimony section to sidebar

## Setup Instructions

### Step 1: Activate Virtual Environment
```bash
# Navigate to project directory
cd "c:\Users\Tilak\OneDrive\Documents\docker projects\karwarian.shop"

# Activate virtual environment (if you have one)
# Windows:
venv\Scripts\activate
# Or if using different name:
.venv\Scripts\activate
```

### Step 2: Create Database Migrations
```bash
python manage.py makemigrations
```

This will create a migration file for the new `MatrimonyProfile` model.

### Step 3: Apply Migrations
```bash
python manage.py migrate
```

This will create the matrimony_profile table in your database.

### Step 4: Test the System

#### Test User Submission:
1. Start the development server: `python manage.py runserver`
2. Visit: `http://localhost:8000/matrimony/`
3. Click "Add Profile" button
4. Fill out the form and submit
5. Profile will be in "Pending Approval" status

#### Test Admin Dashboard:
1. Login to admin dashboard: `http://localhost:8000/dashboard/login/`
   - Username: admin
   - Password: 631176
2. Navigate to "Matrimony" → "Profiles" in sidebar
3. You'll see pending profiles
4. Click "Approve" to make them visible on public page
5. Test "Add Profile" to manually add profiles (auto-approved)

## Features

### User Features:
✅ Browse approved matrimony profiles
✅ Filter by caste/community
✅ Submit new profile (requires approval)
✅ View contact information
✅ Responsive design with beautiful UI

### Admin Features:
✅ View all profiles (pending, approved, inactive)
✅ Approve/disapprove profiles
✅ Activate/deactivate profiles
✅ Manually add profiles (auto-approved)
✅ Delete profiles
✅ View submission dates and contact info
✅ Filter by status tabs

## Workflow

1. **User Submits Profile**
   - User visits `/matrimony/`
   - Clicks "Add Profile"
   - Fills form and submits
   - Profile saved with `is_approved=False`
   - Success message shown

2. **Admin Reviews**
   - Admin logs into dashboard
   - Goes to Matrimony → Profiles
   - Sees profile in "Pending Approval" tab
   - Reviews information
   - Clicks "Approve" button

3. **Profile Goes Live**
   - Profile now has `is_approved=True`
   - Appears on public `/matrimony/` page
   - Users can see and contact

4. **Admin Can Also**
   - Manually add profiles (auto-approved)
   - Deactivate profiles temporarily
   - Delete profiles permanently
   - Filter by status

## Database Schema

```sql
CREATE TABLE matrimony_profile (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(100),
    father_name VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),  -- 'male' or 'female'
    height VARCHAR(20),
    caste VARCHAR(50),
    qualification VARCHAR(200),
    occupation VARCHAR(200),
    contact_phone VARCHAR(15),
    contact_email VARCHAR(254),
    address TEXT,
    additional_info TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME,
    updated_at DATETIME
);
```

## Caste/Community Options
- Gowda
- Bhandari
- Gunagi
- Ambig
- Konkan Maratha
- Kombarpath
- Harikantra
- Sonar
- Brahman
- Dalvi
- Gabith
- Nadar
- Other

## Security Notes
- User submissions require admin approval
- Only approved + active profiles shown publicly
- Admin authentication required for dashboard
- CSRF protection on all forms
- Contact info only shown when user clicks "Contact Now"

## Troubleshooting

### Issue: Migrations not working
**Solution**: Make sure Django is installed and virtual environment is activated

### Issue: 404 on matrimony page
**Solution**: Check that URLs are properly configured in main `urls.py`

### Issue: Profiles not showing
**Solution**: Make sure profiles are both `is_approved=True` AND `is_active=True`

### Issue: Can't access dashboard
**Solution**: Login credentials are:
- Username: `admin`
- Password: `631176`

## Next Steps (Optional Enhancements)

1. **Add Photo Upload**
   - Add `profile_photo` ImageField to model
   - Update forms to handle file uploads
   - Display photos in cards

2. **Advanced Filtering**
   - Filter by age range
   - Filter by qualification
   - Filter by gender

3. **Email Notifications**
   - Email admin when new profile submitted
   - Email user when profile approved

4. **Profile Details Page**
   - Dedicated page for each profile
   - Show full information
   - Contact form

5. **Search Functionality**
   - Search by name
   - Search by occupation
   - Search by location

## Support
If you encounter any issues, check:
1. Virtual environment is activated
2. All migrations are applied
3. Database is accessible
4. Static files are collected (for production)

---
**Created**: 2025
**Version**: 1.0
**Status**: Ready for Testing
