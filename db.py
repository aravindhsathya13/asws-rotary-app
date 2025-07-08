"""
db.py: Database management for Rotary Club Anniversary Management System
"""
import sqlite3
from typing import List
from models import Member

class DatabaseManager:
    """Handles all database operations"""
    def __init__(self, db_path: str = "rotary_club.db"):
        self.db_path = db_path
        self.setup_database_pragma()
        self.init_database()

    def setup_database_pragma(self):
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            conn.execute("PRAGMA temp_store=memory")
            conn.commit()

    def init_database(self):
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    birthday TEXT NOT NULL,
                    wedding_anniversary TEXT,
                    spouse_name TEXT,
                    email TEXT,
                    title TEXT,
                    relationship_status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_member(self, member: Member) -> bool:
        try:
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO members (title, name, phone, birthday, wedding_anniversary, spouse_name, email, relationship_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    member.title,
                    member.name,
                    member.phone,
                    member.birthday,
                    member.wedding_anniversary,
                    member.spouse_name,
                    member.email,
                    member.relationship_status
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def get_all_members(self) -> List[Member]:
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('PRAGMA table_info(members)')
            columns = [col[1] for col in cursor.fetchall()]
            cursor.execute('SELECT * FROM members ORDER BY name')
            rows = cursor.fetchall()
        members = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            member = Member(
                id=row_dict.get('id'),
                name=row_dict.get('name'),
                phone=row_dict.get('phone'),
                birthday=row_dict.get('birthday'),
                wedding_anniversary=row_dict.get('wedding_anniversary'),
                spouse_name=row_dict.get('spouse_name'),
                email=row_dict.get('email'),
                title=row_dict.get('title'),
                relationship_status=row_dict.get('relationship_status')
            )
            members.append(member)
        return members

    def get_members_by_date(self, date_str: str, event_type: str) -> List[Member]:
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            if event_type == 'birthday':
                cursor.execute('SELECT * FROM members WHERE birthday = ?', (date_str,))
            elif event_type == 'anniversary':
                cursor.execute('SELECT * FROM members WHERE wedding_anniversary = ?', (date_str,))
            rows = cursor.fetchall()
        members = []
        for row in rows:
            member = Member(
                id=row[0], name=row[1], phone=row[2], birthday=row[3],
                wedding_anniversary=row[4], spouse_name=row[5], email=row[6],
                title=row[7] if len(row) > 7 else None,
                relationship_status=row[8] if len(row) > 8 else None
            )
            members.append(member)
        return members

    def update_member(self, member_id: int, member: Member) -> bool:
        try:
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE members SET title=?, name=?, phone=?, birthday=?, wedding_anniversary=?, spouse_name=?, email=?, relationship_status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?
                ''', (member.title, member.name, member.phone, member.birthday, member.wedding_anniversary, member.spouse_name, member.email, member.relationship_status, member_id))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error updating member: {e}")
            return False
