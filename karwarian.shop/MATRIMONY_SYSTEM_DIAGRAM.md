# Matrimony System - Visual Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │   PUBLIC PAGE        │         │   ADMIN DASHBOARD    │    │
│  │  /matrimony/         │         │  /dashboard/         │    │
│  │                      │         │  matrimony/          │    │
│  │  • Browse Profiles   │         │                      │    │
│  │  • Filter by Caste   │         │  • Approve Profiles  │    │
│  │  • Submit Profile    │         │  • Add Profiles      │    │
│  │  • View Contact      │         │  • Manage Status     │    │
│  └──────────────────────┘         └──────────────────────┘    │
│           │                                  │                  │
└───────────┼──────────────────────────────────┼─────────────────┘
            │                                  │
            ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                            VIEWS LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │  core/views.py       │         │ core/dashboard_      │    │
│  │                      │         │ views.py             │    │
│  │  • matrimony_list    │         │                      │    │
│  │  • matrimony_add     │         │ • matrimony_         │    │
│  │                      │         │   dashboard_list     │    │
│  │                      │         │ • matrimony_         │    │
│  │                      │         │   dashboard_add      │    │
│  │                      │         │ • matrimony_         │    │
│  │                      │         │   dashboard_update   │    │
│  │                      │         │ • matrimony_         │    │
│  │                      │         │   dashboard_delete   │    │
│  └──────────────────────┘         └──────────────────────┘    │
│           │                                  │                  │
└───────────┼──────────────────────────────────┼─────────────────┘
            │                                  │
            └──────────────┬───────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         MODEL LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    core/models.py                               │
│                                                                 │
│              ┌─────────────────────────┐                        │
│              │   MatrimonyProfile      │                        │
│              ├─────────────────────────┤                        │
│              │ • full_name             │                        │
│              │ • father_name           │                        │
│              │ • age                   │                        │
│              │ • gender                │                        │
│              │ • height                │                        │
│              │ • caste                 │                        │
│              │ • qualification         │                        │
│              │ • occupation            │                        │
│              │ • contact_phone         │                        │
│              │ • contact_email         │                        │
│              │ • address               │                        │
│              │ • additional_info       │                        │
│              │ • is_approved ⚠️        │                        │
│              │ • is_active             │                        │
│              │ • created_at            │                        │
│              │ • updated_at            │                        │
│              └─────────────────────────┘                        │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│              matrimony_profile table                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagrams

### User Submission Flow

```
┌─────────────┐
│   User      │
│ Visits Page │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Clicks "Add Profile"│
│ Button              │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Modal Form Opens    │
│ Fills Information   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Submits Form        │
│ POST /matrimony/add/│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────┐
│ matrimony_add() view        │
│ Creates MatrimonyProfile    │
│ is_approved = False ⚠️      │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Saves to Database           │
│ Shows Success Message       │
│ "Pending Admin Approval"    │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Redirects to /matrimony/    │
│ Profile NOT visible yet     │
└─────────────────────────────┘
```

### Admin Approval Flow

```
┌─────────────┐
│   Admin     │
│ Logs In     │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│ Navigates to Dashboard   │
│ /dashboard/matrimony/    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Sees "Pending Approval"  │
│ Tab with Badge Count     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Reviews Profile Info     │
│ Clicks "Approve" Button  │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ AJAX POST to                     │
│ /dashboard/matrimony/            │
│ <id>/update-status/              │
│ action: "approve"                │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ matrimony_dashboard_update_      │
│ status() view                    │
│ Sets is_approved = True ✅       │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ Saves to Database                │
│ Returns JSON success             │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ Page Reloads                     │
│ Profile moves to "Approved" tab  │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ Profile NOW visible on           │
│ Public /matrimony/ page          │
└──────────────────────────────────┘
```

### Admin Manual Add Flow

```
┌─────────────┐
│   Admin     │
│ Logs In     │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│ Clicks "Add Profile"     │
│ in Sidebar               │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Opens Form Page          │
│ /dashboard/matrimony/add/│
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Fills Comprehensive Form │
│ All Sections             │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Submits Form             │
│ POST to same URL         │
└──────┬───────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ matrimony_dashboard_add() view  │
│ Creates MatrimonyProfile        │
│ is_approved = True ✅           │
│ (Auto-approved!)                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Saves to Database               │
│ Redirects to List Page          │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Profile IMMEDIATELY visible on  │
│ Public /matrimony/ page         │
└─────────────────────────────────┘
```

---

## 🗺️ URL Routing Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         URL PATTERNS                            │
└─────────────────────────────────────────────────────────────────┘

PUBLIC ROUTES:
├── /matrimony/
│   ├── GET  → matrimony_list()
│   │         Shows approved profiles
│   │         Filters by caste
│   │
│   └── /add/
│       └── POST → matrimony_add()
│                  Creates profile (unapproved)

ADMIN ROUTES:
└── /dashboard/
    └── matrimony/
        ├── GET  → matrimony_dashboard_list()
        │          Lists all profiles
        │          Filters by status
        │
        ├── /add/
        │   ├── GET  → matrimony_dashboard_add()
        │   │          Shows form
        │   └── POST → matrimony_dashboard_add()
        │              Creates profile (auto-approved)
        │
        ├── /<id>/update-status/
        │   └── POST → matrimony_dashboard_update_status()
        │              AJAX: approve/disapprove/toggle
        │
        └── /<id>/delete/
            └── GET  → matrimony_dashboard_delete()
                       Deletes profile
```

---

## 📊 State Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROFILE STATE MACHINE                        │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │  Profile Created │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌───────────────────┐     ┌──────────────────┐
    │ User Submission   │     │ Admin Creation   │
    │ is_approved=False │     │ is_approved=True │
    │ is_active=True    │     │ is_active=True   │
    └────────┬──────────┘     └────────┬─────────┘
             │                         │
             │ Admin                   │
             │ Approves                │
             ▼                         │
    ┌───────────────────┐             │
    │ APPROVED          │◄────────────┘
    │ is_approved=True  │
    │ is_active=True    │
    │ ✅ VISIBLE        │
    └────────┬──────────┘
             │
             │ Admin can:
             │
    ┌────────┼────────────────────┐
    │        │                    │
    ▼        ▼                    ▼
┌────────┐ ┌──────────┐    ┌──────────┐
│Deactivate│ │Disapprove│    │ Delete   │
│          │ │          │    │          │
│is_active │ │is_approved│   │ Removed  │
│= False   │ │= False   │    │ from DB  │
│          │ │          │    │          │
│❌ HIDDEN │ │❌ HIDDEN │    │❌ GONE   │
└────┬─────┘ └────┬─────┘    └──────────┘
     │            │
     │ Reactivate │ Re-approve
     │            │
     └────────────┴──────────────┐
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ APPROVED         │
                        │ is_approved=True │
                        │ is_active=True   │
                        │ ✅ VISIBLE       │
                        └──────────────────┘
```

---

## 🎨 Template Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEMPLATE STRUCTURE                         │
└─────────────────────────────────────────────────────────────────┘

PUBLIC TEMPLATES:
base.html
└── core/matrimony_list.html
    ├── Hero Section
    │   ├── Title & Icon
    │   ├── Subtitle
    │   └── "Add Profile" Button
    │
    ├── Stats Bar
    │   ├── Total Profiles
    │   ├── Communities
    │   └── Verification %
    │
    ├── Filter Section
    │   └── Caste Dropdown
    │
    ├── Profiles Grid
    │   └── Profile Cards (loop)
    │       ├── Card Header (gradient)
    │       │   ├── Avatar
    │       │   ├── Name
    │       │   └── Caste Badge
    │       ├── Card Body
    │       │   └── Info Rows
    │       └── Card Footer
    │           └── Contact Button
    │
    └── Modal Overlay
        └── Modal
            ├── Modal Header
            ├── Modal Body
            │   └── Submission Form
            │       ├── Basic Info
            │       ├── Education
            │       ├── Contact
            │       └── Submit Button
            └── Modal Close

ADMIN TEMPLATES:
dashboard/base.html
├── Sidebar
│   ├── Brand
│   ├── Navigation Sections
│   │   ├── Overview
│   │   ├── Cricket
│   │   ├── Ice Cream
│   │   ├── Content
│   │   ├── Marketplace
│   │   ├── Matrimony ⭐
│   │   │   ├── Profiles
│   │   │   └── Add Profile
│   │   └── System
│   └── Logout
│
└── Main Content Area
    │
    ├── dashboard/matrimony_list.html
    │   ├── Topbar
    │   │   ├── Title
    │   │   └── "Add Profile" Button
    │   │
    │   └── Panel
    │       ├── Panel Header
    │       │   └── Status Tabs
    │       │       ├── Pending (badge)
    │       │       ├── Approved (badge)
    │       │       ├── Inactive
    │       │       └── All (badge)
    │       │
    │       └── Table
    │           └── Profile Rows (loop)
    │               ├── Name & Father
    │               ├── Age, Gender, Caste
    │               ├── Education
    │               ├── Contact
    │               ├── Status Badges
    │               ├── Date
    │               └── Action Buttons
    │
    └── dashboard/matrimony_form.html
        ├── Topbar
        │   ├── Title
        │   └── "Back" Button
        │
        └── Panel (Form)
            ├── Basic Information
            │   ├── Name Fields
            │   ├── Age, Gender, Height
            │   └── Caste
            │
            ├── Education & Occupation
            │   ├── Qualification
            │   └── Occupation
            │
            ├── Contact Information
            │   ├── Phone, Email
            │   └── Address
            │
            ├── Additional Info
            │
            └── Action Buttons
                ├── Cancel
                └── Save
```

---

## 🔐 Permission Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                      ACCESS CONTROL                             │
└─────────────────────────────────────────────────────────────────┘

ACTION                          │ PUBLIC USER │ ADMIN
────────────────────────────────┼─────────────┼──────
View Approved Profiles          │     ✅      │  ✅
View Pending Profiles           │     ❌      │  ✅
View Inactive Profiles          │     ❌      │  ✅
Submit New Profile              │     ✅      │  ✅
Approve Profile                 │     ❌      │  ✅
Disapprove Profile              │     ❌      │  ✅
Activate/Deactivate Profile     │     ❌      │  ✅
Delete Profile                  │     ❌      │  ✅
Manually Add Profile            │     ❌      │  ✅
View Contact Information        │     ✅*     │  ✅
Filter by Caste                 │     ✅      │  ✅
Access Dashboard                │     ❌      │  ✅

* Only for approved profiles, via button click
```

---

## 📱 Responsive Breakpoints

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSIVE DESIGN                            │
└─────────────────────────────────────────────────────────────────┘

DESKTOP (> 768px):
├── Profiles Grid: 3-4 columns
├── Form: 2-3 column layout
├── Dashboard Sidebar: Visible (260px)
└── Tables: Full width with all columns

TABLET (481px - 768px):
├── Profiles Grid: 2 columns
├── Form: 2 column layout
├── Dashboard Sidebar: Hidden (hamburger)
└── Tables: Horizontal scroll

MOBILE (≤ 480px):
├── Profiles Grid: 1 column
├── Form: 1 column (stacked)
├── Dashboard Sidebar: Hidden
├── Tables: Horizontal scroll
└── Stats Bar: Stacked vertically
```

---

## 🎯 Key Features Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                      FEATURE MATRIX                             │
└─────────────────────────────────────────────────────────────────┘

PUBLIC FEATURES:
✅ Browse approved matrimony profiles
✅ Beautiful card-based layout
✅ Filter profiles by caste/community
✅ Submit new profile via modal form
✅ View contact information (on click)
✅ Responsive design (mobile-friendly)
✅ Smooth animations and transitions
✅ Form validation
✅ Success/error messages

ADMIN FEATURES:
✅ View all profiles (pending/approved/inactive)
✅ Status filter tabs with badge counts
✅ Approve/disapprove profiles (AJAX)
✅ Activate/deactivate profiles
✅ Delete profiles (with confirmation)
✅ Manually add profiles (auto-approved)
✅ Comprehensive form with all fields
✅ Real-time status updates
✅ Professional dashboard UI
✅ Sidebar navigation
✅ Search and filter capabilities

WORKFLOW FEATURES:
✅ User submission → Pending approval
✅ Admin review → Approve/reject
✅ Approved profiles → Public visibility
✅ Admin manual add → Instant approval
✅ Deactivate → Hide without deleting
✅ Delete → Permanent removal
```

---

This visual architecture shows the complete matrimony system from top to bottom! 🎉
