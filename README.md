# Rotary Club Anniversary Management System

## 🎯 Features

- **Member Database**: Store member information with birthdays and wedding anniversaries
- **Web Dashboard**: Beautiful web interface to manage members and view events
- **Event Management**: Track upcoming birthdays and anniversaries with DD-MM format
- **Current Month Events**: View all events for the current month, sorted by date
- **Member Management**: Add, edit, and view club members with complete information
- **Free Hosting**: Deploy to Heroku, Railway, or other free platforms

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python main.py
```

Visit `http://localhost:5000` to access the dashboard.

## � Project Structure

```
app/
├── main.py              # Flask app entry point and routes
├── models.py            # Data models (Member class)
├── db.py               # Database management
├── anniversary.py       # Anniversary event logic
├── config.py           # App configuration
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── add_member.html
│   └── members.html
├── utils/              # Utility modules
├── requirements.txt    # Python dependencies
├── rotary_club.db     # SQLite database (auto-created)
└── README.md          # This file
```

## 🌐 Free Hosting Options

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
- View member details and contact information

### Current Month Events

- Shows all birthdays and anniversaries for the current month
- Events are sorted by date (ascending)
- Displays dates in user-friendly format (e.g., "Jul 02")

### Upcoming Events

- 7-day preview of upcoming birthdays and anniversaries
- Helps with planning and preparation
- Sorted by event date for easy viewing

### Member Management

- Add new club members with complete information
- Edit existing member details
- View all members in organized table format
- Search and filter capabilities

## 🔧 Configuration

### Environment Variables

```bash
SECRET_KEY=your-secret-key
DEBUG=False
PORT=5000
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
   - Relationship status (Single/Married/etc.)

### Editing Members

1. Go to "Members" page
2. Click "Edit" button next to any member
3. Update information as needed
4. Save changes

### Viewing Events

- **Dashboard**: Shows today's events and upcoming week
- **Current Month**: View all events for the current month
- **Member List**: View all members with their information

## �️ Database Management

### SQLite Database

- Database file: `rotary_club.db` (auto-created)
- Tables: `members`, `message_logs`
- Automatic backups recommended for production

### Database Tools (Admin/Developer)

#### DB Browser for SQLite

1. Download from [sqlitebrowser.org](https://sqlitebrowser.org/)
2. Open `rotary_club.db` file
3. View/edit data directly
4. Export data as needed

#### DBeaver (Advanced)

1. Download from [dbeaver.io](https://dbeaver.io/)
2. Create new SQLite connection
3. Point to `rotary_club.db` file
4. Full database management capabilities

## 🛠️ Troubleshooting

### App Not Starting

1. Check all dependencies installed: `pip install -r requirements.txt`
2. Verify Python version compatibility
3. Check port 5000 is not already in use
4. Review error messages in terminal

### Database Issues

- SQLite database creates automatically
- Check file permissions in app directory
- Try deleting `rotary_club.db` to recreate fresh database
- Backup database before making changes

### Hosting Issues

- Check environment variables are set
- Verify all dependencies in requirements.txt
- Check application logs for error messages
- Ensure database file has proper permissions

## 🔐 Security Notes

- Never commit sensitive data to version control
- Use strong secret keys in production
- Regularly backup your member database
- Keep personal information secure
- Use HTTPS in production environments

## 📞 Support

For any issues or questions:

1. Check the troubleshooting section
2. Verify your environment variables
3. Check application logs
4. Contact your system administrator

## 🤝 Contributing

Feel free to enhance this system by:

- Adding notification features (email/SMS)
- Creating mobile app version
- Adding data export/import features
- Improving the dashboard UI
- Adding more member fields
- Creating reporting features
- Adding backup/restore functionality

## 🏗️ Architecture

The application follows a modular structure:

- **main.py**: Flask routes and app configuration
- **models.py**: Data classes and structures
- **db.py**: Database operations and management
- **anniversary.py**: Event logic and date handling
- **config.py**: Configuration management
- **templates/**: Frontend HTML templates

---

Made with ❤️ for Rotary Club | Member Anniversary Management System �
