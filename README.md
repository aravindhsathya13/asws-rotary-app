# 🌟 Rotary Club Anniversary Management System

A comprehensive web application for managing club member anniversaries with mobile-first design and cloud database support.

## ✨ Features

### 📊 Core Features

- **Member Database**: Store member information with birthdays and wedding anniversaries
- **Web Dashboard**: Beautiful responsive interface for all devices
- **Event Management**: Track upcoming birthdays and anniversaries
- **Current Month Events**: View all events for the current month
- **Member Management**: Add, edit, and view club members
- **Statistics Dashboard**: Quick overview of member data

### 📱 Mobile & PWA Features

- **Mobile-First Design**: Optimized for smartphones and tablets
- **Progressive Web App**: Installable on device home screen
- **Touch-Friendly**: 44px minimum touch targets
- **Responsive Navigation**: Collapsible menu for mobile
- **Floating Action Buttons**: Quick access on mobile
- **Offline Support**: Basic functionality without internet

### ☁️ Cloud Database Support

- **Supabase Integration**: Free PostgreSQL cloud database
- **SQLite Fallback**: Local database for development
- **Hybrid Mode**: Automatic fallback between cloud and local
- **Real-time Sync**: Changes reflect immediately
- **Manual Management**: Manage data via Supabase dashboard

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

#### Option A: Use Local SQLite (Default)

```bash
# In .env file
USE_SUPABASE=false
```

#### Option B: Use Supabase Cloud Database

```bash
# In .env file
USE_SUPABASE=true
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

### 3. Run Locally

```bash
python main.py
```

Visit `http://localhost:5003` to access the dashboard.

## 🗂️ Project Structure

```
app/
├── main.py                 # Flask app entry point and routes
├── models.py              # Data models (Member class)
├── db.py                  # SQLite database management
├── supabase_db.py         # Supabase cloud database management
├── anniversary.py         # Anniversary event logic
├── ssl_config.py          # SSL configuration for cloud DB
├── templates/             # HTML templates
│   ├── base.html          # Base template with PWA features
│   ├── dashboard.html     # Main dashboard
│   ├── add_member.html    # Add member form
│   └── members.html       # Member list view
├── static/                # Static assets
│   ├── mobile.css         # Mobile-first CSS
│   ├── manifest.json      # PWA manifest
│   ├── sw.js             # Service worker
│   └── icons/            # PWA icons
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
└── README.md             # This file
```

## ☁️ Supabase Setup Guide

### Step 1: Create Supabase Account & Project

1. **Go to**: https://supabase.com
2. **Sign up** with GitHub/Google (completely free!)
3. **Create new project**:
   - Project name: `rotary-club-anniversary`
   - Database password: Choose a strong password
   - Region: Choose closest to you
4. **Wait 2-3 minutes** for project creation

### Step 2: Get API Credentials

1. In Supabase dashboard → **Settings** → **API**
2. Copy these values:
   - **Project URL**: `https://your-project-id.supabase.co`
   - **Anon Public Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Step 3: Create Members Table

Go to **Table Editor** → **Create a new table** → Use this SQL:

```sql
CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    title VARCHAR(10) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    birthday VARCHAR(5) NOT NULL,
    wedding_anniversary VARCHAR(5),
    spouse_name VARCHAR(255),
    email VARCHAR(255),
    relationship_status VARCHAR(50) DEFAULT 'Single',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Step 4: Configure Environment

Update your `.env` file:

```env
USE_SUPABASE=true
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

## 🌐 Deployment Options

### Option 1: Heroku (Recommended)

1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Deploy:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-rotary-club-app
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set USE_SUPABASE=true
   heroku config:set SUPABASE_URL=your_supabase_url
   heroku config:set SUPABASE_ANON_KEY=your_supabase_key
   git push heroku main
   ```

### Option 2: Railway

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables in Railway dashboard
4. Deploy automatically

### Option 3: Render

1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Set environment variables
4. Deploy as web service

## 📊 Dashboard Features

### Today's Events

- Shows birthdays and anniversaries for today
- Member contact information
- Quick actions for sending wishes

### Current Month Events

- All events for current month
- Sorted by date for easy planning
- User-friendly date format

### Upcoming Events

- 7-day preview of upcoming events
- Planning and preparation assistance
- Color-coded event types

### Member Management

- Add new members with complete information
- Edit existing member details
- Responsive table/card views
- Search and filter capabilities

### Statistics

- Total member count
- Registered birthdays count
- Registered anniversaries count
- Email addresses count

## 📱 Mobile Features

### PWA Installation

1. Open the app in mobile browser
2. Look for "Add to Home Screen" prompt
3. Or use browser menu → "Install App"
4. App icon appears on home screen

### Touch-Optimized Interface

- Large, finger-friendly buttons
- Swipe-friendly card layouts
- Responsive navigation menu
- Quick floating action buttons

### Offline Support

- Service worker caches essential files
- Basic functionality works offline
- Automatic sync when connection returns

## 🔧 Configuration

### Environment Variables

```env
# Database Configuration
USE_SUPABASE=true/false
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Flask Configuration
SECRET_KEY=your-secret-key
DEBUG=True/False
PORT=5003
HOST=0.0.0.0

# SSL Configuration (for Supabase)
SUPABASE_SSL_CERT=prod-ca-2021.crt
```

### Date Format

- Use DD-MM format for dates (day-month)
- Example: 15-03 for March 15th
- Year is not needed (only day and month)

## 📋 Usage Instructions

### Adding Members

1. Go to "Add Member" page
2. Fill in required information:
   - Title (Mr./Mrs./Dr./etc.)
   - Name (required)
   - Phone number (required)
   - Birthday in DD-MM format (required)
   - Wedding anniversary in DD-MM format (optional)
   - Spouse name (optional)
   - Email (optional)
   - Relationship status

### Managing Members

- **View All**: Members page shows responsive table/cards
- **Edit**: Click edit button to modify member details
- **Statistics**: Quick stats on dashboard
- **Search**: Filter members by various criteria

### Mobile Usage

- **Installation**: Add app to home screen for native feel
- **Navigation**: Use hamburger menu on mobile
- **Quick Actions**: Use floating action buttons
- **Touch**: All elements optimized for finger interaction

## 🛠️ Troubleshooting

### SSL Certificate Issues (Supabase)

The app includes SSL workarounds for development:

- SSL verification disabled for Supabase connections
- Automatic fallback to HTTP requests
- Certificate bundle included for production

### App Not Starting

1. Check dependencies: `pip install -r requirements.txt`
2. Verify Python version compatibility
3. Check port 5003 availability
4. Review error messages

### Database Issues

- **SQLite**: Database creates automatically
- **Supabase**: Check credentials in .env file
- **Connection**: App falls back to SQLite if Supabase fails
- **Tables**: Use provided SQL to create Supabase tables

### Mobile Issues

- **PWA**: Clear browser cache and try again
- **Installation**: Use HTTPS for PWA features
- **Touch**: Ensure viewport meta tag is present
- **Performance**: Service worker caches resources

## 🔐 Security Notes

- Keep Supabase credentials secure
- Use strong secret keys in production
- Regularly backup member database
- Use HTTPS in production
- Row Level Security (RLS) available in Supabase

## � Advanced Features

### Cloud Database Benefits

- **Automatic Backups**: Supabase handles backups
- **Real-time**: Changes sync across devices
- **Scalable**: Handles growing membership
- **Admin Dashboard**: Manage data via Supabase UI

### PWA Benefits

- **Installation**: App-like experience
- **Performance**: Faster loading with caching
- **Engagement**: Home screen access
- **Offline**: Basic functionality without internet

### Mobile Optimization

- **Responsive**: Works on all screen sizes
- **Touch-Friendly**: Optimized for finger interaction
- **Fast**: Lightweight and efficient
- **Accessible**: Screen reader compatible

## 🤝 Contributing

Enhance the system by:

- Adding notification features
- Creating additional reports
- Improving mobile experience
- Adding data export/import
- Enhancing PWA features
- Adding more member fields

## 📞 Support

For issues:

1. Check troubleshooting section
2. Verify environment variables
3. Check application logs
4. Test with SQLite fallback

---

**Made with ❤️ for Rotary Club | Complete Anniversary Management System 🌟**
