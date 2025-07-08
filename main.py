

# --- SSL Verification Workaround for Local Debug ---
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['PYTHONHTTPSVERIFY'] = '0'

"""
Rotary Club Anniversary Management System
=========================================
A Python application to manage member anniversaries and send email reminders.

Features:
- Member database management
- Email notification automation
- Dashboard for upcoming events
- Scheduled reminders (daily, weekly, monthly)
"""

import sqlite3
import datetime
import os
import json
import schedule
import time
from dataclasses import dataclass
from typing import List, Optional
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import threading
from models import Member
from db import DatabaseManager
from anniversary import AnniversaryManager

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, environment variables should be set by hosting platform
    pass


# Flask Web Application for Dashboard
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Global instance
anniversary_manager = None

def init_anniversary_manager():
    """Initialize the anniversary manager"""
    global anniversary_manager
    anniversary_manager = AnniversaryManager()

@app.route('/')
def dashboard():
    """Main dashboard"""
    if not anniversary_manager:
        init_anniversary_manager()
    today_events = anniversary_manager.get_today_events()
    month_events = anniversary_manager.get_month_events()
    upcoming_events = anniversary_manager.get_upcoming_events(7)
    return render_template('dashboard.html', 
                         today_events=today_events,
                         month_events=month_events,
                         upcoming_events=upcoming_events)

@app.route('/members')
def members_list():
    """List all members"""
    if not anniversary_manager:
        init_anniversary_manager()
    
    members = anniversary_manager.db.get_all_members()
    return render_template('members.html', members=members)

@app.route('/add_member', methods=['GET', 'POST'])
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    """Add new member"""
    if not anniversary_manager:
        init_anniversary_manager()

    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        phone = request.form['phone']
        birthday = request.form['birthday']
        wedding_anniversary = request.form.get('wedding_anniversary') or None
        spouse_name = request.form.get('spouse_name') or None
        email = request.form.get('email') or None
        relationship_status = request.form.get('relationship_status')

        # Auto-fill spouse name if Married and left blank
        if relationship_status == 'Married' and (not spouse_name or spouse_name.strip() == ''):
            if title == 'Mr.':
                spouse_name = f"Mrs. {name}"
            elif title == 'Mrs.':
                spouse_name = f"Mr. {name}"

        member = Member(
            id=None,
            name=name,
            phone=phone,
            birthday=birthday,
            wedding_anniversary=wedding_anniversary,
            spouse_name=spouse_name,
            email=email
        )
        # Attach extra fields for DB
        member.title = title
        member.relationship_status = relationship_status

        if anniversary_manager.db.add_member(member):
            flash('Member added successfully!', 'success')
            return redirect(url_for('members_list'))
        else:
            flash('Error adding member. Phone number might already exist.', 'error')

    return render_template('add_member.html')

@app.route('/send_wishes')
def send_wishes():
    """Manual trigger to send today's wishes"""
    if not anniversary_manager:
        init_anniversary_manager()
    
    anniversary_manager.send_daily_wishes()
    flash('Wishes sent for today\'s events!', 'success')
    return redirect(url_for('dashboard'))

# --- Edit Member Route ---
@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    """Edit an existing member's information."""
    if not anniversary_manager:
        init_anniversary_manager()
    # Fetch member from DB
    members = anniversary_manager.db.get_all_members()
    member = next((m for m in members if m.id == member_id), None)
    if not member:
        flash('Member not found.', 'error')
        return redirect(url_for('members_list'))
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        phone = request.form['phone']
        birthday = request.form['birthday']
        wedding_anniversary = request.form.get('wedding_anniversary') or None
        spouse_name = request.form.get('spouse_name') or None
        email = request.form.get('email') or None
        relationship_status = request.form.get('relationship_status')

        # Auto-fill spouse name if Married and left blank
        if relationship_status == 'Married' and (not spouse_name or spouse_name.strip() == ''):
            if title == 'Mr.':
                spouse_name = f"Mrs. {name}"
            elif title == 'Mrs.':
                spouse_name = f"Mr. {name}"

        # Update in DB
        try:
            with sqlite3.connect(anniversary_manager.db.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE members SET title=?, name=?, phone=?, birthday=?, wedding_anniversary=?, spouse_name=?, email=?, relationship_status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?
                ''', (title, name, phone, birthday, wedding_anniversary, spouse_name, email, relationship_status, member_id))
                conn.commit()
            flash('Member updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating member: {e}', 'error')
        return redirect(url_for('members_list'))
    # Render edit form (reuse add_member.html with member context)
    return render_template('add_member.html', member=member, edit_mode=True)

def setup_scheduler():
    """Setup the daily scheduler"""
    # Schedule daily wishes at 9 AM
    schedule.every().day.at("09:00").do(lambda: anniversary_manager.send_daily_wishes())
    
    # Schedule reminder notifications at 6 PM for next day
    schedule.every().day.at("18:00").do(lambda: anniversary_manager.send_reminder_notifications())
    
    # Run scheduler in background
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

if __name__ == '__main__':
    # Initialize the system
    init_anniversary_manager()
    
    # Setup the scheduler for automated messages
    setup_scheduler()
    
    # Run the web application
    print("🚀 Rotary Club Anniversary Management System Starting...")
    print("� Notifications are disabled.")
    
    # Get port from environment variable for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    if debug:
        print(f"🌐 Web dashboard available at http://localhost:{port}")
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        print(f"🌐 Web dashboard running on port {port}")
        app.run(debug=False, host='0.0.0.0', port=port)