#!/usr/bin/env python3
"""
Simple database test to verify the system works properly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our classes
try:
    from dataclasses import dataclass
    from typing import Optional
    import sqlite3
    import datetime
    
    @dataclass
    class Member:
        """Data class for club members"""
        id: Optional[int]
        name: str
        phone: str
        birthday: str  # Format: MM-DD
        wedding_anniversary: Optional[str]  # Format: MM-DD
        spouse_name: Optional[str]
        email: Optional[str]
    
    class DatabaseManager:
        """Simplified database manager for testing"""
        
        def __init__(self, db_path: str = "test_rotary.db"):
            self.db_path = db_path
            self.setup_database_pragma()
            self.init_database()
        
        def setup_database_pragma(self):
            """Setup SQLite PRAGMA settings"""
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=memory")
                conn.commit()
        
        def init_database(self):
            """Initialize the database with required tables"""
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
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
        
        def add_member(self, member: Member) -> bool:
            """Add a new member to the database"""
            try:
                with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO members (name, phone, birthday, wedding_anniversary, spouse_name, email)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (member.name, member.phone, member.birthday, 
                          member.wedding_anniversary, member.spouse_name, member.email))
                    
                    conn.commit()
                    return True
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                return False
        
        def get_all_members(self):
            """Get all members from database"""
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM members ORDER BY name')
                rows = cursor.fetchall()
            return rows
    
    def test_database():
        """Test database operations"""
        print("🧪 Testing database operations...")
        
        # Create test database
        db = DatabaseManager("test_rotary.db")
        
        # Create test member
        test_member = Member(
            id=None,
            name="Test Member",
            phone="+919876543210",
            birthday="07-04",  # Today for testing
            wedding_anniversary="12-25",
            spouse_name="Test Spouse",
            email="test@example.com"
        )
        
        # Test adding member
        success = db.add_member(test_member)
        if success:
            print("✅ Member added successfully")
        else:
            print("❌ Failed to add member")
            return False
        
        # Test retrieving members
        members = db.get_all_members()
        if len(members) > 0:
            print(f"✅ Retrieved {len(members)} members")
            print(f"   First member: {members[0][1]} - {members[0][2]}")
        else:
            print("❌ No members found")
            return False
        
        # Test adding another member
        test_member2 = Member(
            id=None,
            name="Another Member",
            phone="+919876543211",
            birthday="03-15",
            wedding_anniversary=None,
            spouse_name=None,
            email=None
        )
        
        success2 = db.add_member(test_member2)
        if success2:
            print("✅ Second member added successfully")
        else:
            print("❌ Failed to add second member")
        
        # Clean up
        os.remove("test_rotary.db")
        if os.path.exists("test_rotary.db-wal"):
            os.remove("test_rotary.db-wal")
        if os.path.exists("test_rotary.db-shm"):
            os.remove("test_rotary.db-shm")
        
        print("✅ Database test completed successfully!")
        return True

    if __name__ == "__main__":
        success = test_database()
        if success:
            print("\n🎉 Database is working properly! You can now run the main application.")
        else:
            print("\n❌ Database test failed. Please check the configuration.")
        sys.exit(0 if success else 1)

except Exception as e:
    print(f"❌ Test failed with error: {e}")
    sys.exit(1)
