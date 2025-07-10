"""
anniversary.py: Anniversary event logic for Rotary Club Anniversary Management System
"""
import datetime
from supabase_db import HybridDatabaseManager
from models import Member

class AnniversaryManager:
    def __init__(self):
        self.db = HybridDatabaseManager()

    def get_month_events(self) -> dict:
        today = datetime.date.today()
        month = today.strftime("%m")
        all_members = self.db.get_all_members()
        birthdays = []
        anniversaries = []
        for member in all_members:
            if member.birthday:
                parts = member.birthday.split('-')
                if len(parts) == 2 and parts[1] == month:
                    day = int(parts[0])
                    event_date = datetime.date(today.year, int(month), day)
                    birthdays.append({'member': member, 'date': event_date})
                elif len(parts) == 3 and parts[1] == month:
                    day = int(parts[2])
                    event_date = datetime.date(today.year, int(month), day)
                    birthdays.append({'member': member, 'date': event_date})
            if member.wedding_anniversary:
                parts = member.wedding_anniversary.split('-')
                if len(parts) == 2 and parts[1] == month:
                    day = int(parts[0])
                    event_date = datetime.date(today.year, int(month), day)
                    anniversaries.append({'member': member, 'date': event_date})
                elif len(parts) == 3 and parts[1] == month:
                    day = int(parts[2])
                    event_date = datetime.date(today.year, int(month), day)
                    anniversaries.append({'member': member, 'date': event_date})
        birthdays.sort(key=lambda x: x['date'])
        anniversaries.sort(key=lambda x: x['date'])
        return {
            'birthdays': birthdays,
            'anniversaries': anniversaries,
            'month': today.strftime('%B')
        }

    def get_today_events(self) -> dict:
        today = datetime.date.today()
        date_str = today.strftime("%d-%m")
        birthdays = self.db.get_members_by_date(date_str, 'birthday')
        anniversaries = self.db.get_members_by_date(date_str, 'anniversary')
        return {
            'birthdays': birthdays,
            'anniversaries': anniversaries,
            'date': today
        }

    def get_upcoming_events(self, days: int = 7) -> dict:
        events = {'birthdays': [], 'anniversaries': []}
        for i in range(1, days + 1):
            future_date = datetime.date.today() + datetime.timedelta(days=i)
            date_str = future_date.strftime("%d-%m")
            birthdays = self.db.get_members_by_date(date_str, 'birthday')
            anniversaries = self.db.get_members_by_date(date_str, 'anniversary')
            for birthday in birthdays:
                events['birthdays'].append({
                    'member': birthday,
                    'date': future_date
                })
            for anniversary in anniversaries:
                events['anniversaries'].append({
                    'member': anniversary,
                    'date': future_date
                })
        events['birthdays'].sort(key=lambda x: x['date'])
        events['anniversaries'].sort(key=lambda x: x['date'])
        return events
