"""
Supabase Database Manager for Rotary Club Anniversary System
"""
import os
import ssl
import requests
import urllib3
from typing import List, Optional
from supabase import create_client, Client
from models import Member
from dotenv import load_dotenv

# Global SSL bypass for development
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Load environment and SSL configuration
load_dotenv()
try:
    import ssl_config  # This will setup SSL certificates
except ImportError:
    pass

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Additional global SSL bypass
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''

class SupabaseManager:
    """Handles all Supabase database operations with SSL workaround"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.url = None
        self.key = None
        self.headers = None
        self.base_url = None
        self.is_available = False
        self.init_supabase()
    
    def init_supabase(self):
        """Initialize Supabase connection with HTTP fallback"""
        try:
            self.url = os.environ.get('SUPABASE_URL')
            self.key = os.environ.get('SUPABASE_ANON_KEY')
            
            if not self.url or not self.key:
                print("❌ Supabase credentials not found in environment")
                print("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
                return
            
            # Setup HTTP client headers for direct API calls
            self.headers = {
                'apikey': self.key,
                'Authorization': f'Bearer {self.key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
            }
            self.base_url = f"{self.url}/rest/v1"
            
            # Try to initialize the official Supabase client
            try:
                self.supabase = create_client(self.url, self.key)
                print("✅ Supabase client initialized")
            except Exception as e:
                print(f"⚠️  Supabase client initialization failed: {e}")
            
            # Test connection using HTTP
            if self._test_http_connection():
                print("✅ Supabase HTTP connection successful!")
                self.is_available = True
            else:
                print("❌ Supabase HTTP connection failed")
                self.is_available = False
                
        except Exception as e:
            print(f"❌ Supabase initialization failed: {e}")
            self.is_available = False
    
    def _test_http_connection(self):
        """Test HTTP connection to Supabase"""
        try:
            response = requests.get(
                f"{self.base_url}/members?limit=1",
                headers=self.headers,
                verify=False,  # Disable SSL verification
                timeout=10
            )
            return response.status_code in [200, 404]  # 404 is OK if table doesn't exist
        except Exception:
            return False
    
    def _create_members_table(self):
        """Create the members table if it doesn't exist"""
        print("📝 Creating members table in Supabase...")
        print("Go to your Supabase dashboard → SQL Editor and run:")
        print("""
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

-- Insert sample data
INSERT INTO members (title, name, phone, birthday, wedding_anniversary, spouse_name, email, relationship_status) VALUES
('Mr.', 'John Doe', '+91 9876543210', '15-03', '20-05', 'Mrs. Jane Doe', 'john@example.com', 'Married'),
('Mrs.', 'Jane Doe', '+91 9876543211', '22-07', '20-05', 'Mr. John Doe', 'jane@example.com', 'Married'),
('Mr.', 'Bob Smith', '+91 9876543212', '10-12', NULL, NULL, 'bob@example.com', 'Single');
        """)
        print("🌐 Dashboard: https://supabase.com/dashboard/project/ffhywbefisdeutaqlnwj/sql")
    
    def get_all_members(self) -> List[Member]:
        """Get all members from Supabase using HTTP"""
        if not self.base_url:
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/members",
                headers=self.headers,
                verify=False,  # Disable SSL verification
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                members = []
                
                for item in data:
                    member = Member(
                        id=item.get('id'),
                        title=item.get('title', 'Mr.'),
                        name=item.get('name', ''),
                        phone=item.get('phone', ''),
                        birthday=item.get('birthday', ''),
                        wedding_anniversary=item.get('wedding_anniversary'),
                        spouse_name=item.get('spouse_name'),
                        email=item.get('email'),
                        relationship_status=item.get('relationship_status', 'Single')
                    )
                    members.append(member)
                
                return members
            elif response.status_code == 404:
                print("📝 Members table doesn't exist yet. Create it in Supabase dashboard.")
                return []
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
                return []
                
        except Exception as e:
            print(f"Error getting members: {e}")
            return []
    
    def add_member(self, member: Member) -> bool:
        """Add a new member to Supabase using HTTP"""
        if not self.base_url:
            return False
        
        try:
            data = {
                'title': member.title,
                'name': member.name,
                'phone': member.phone,
                'birthday': member.birthday,
                'wedding_anniversary': member.wedding_anniversary,
                'spouse_name': member.spouse_name,
                'email': member.email,
                'relationship_status': member.relationship_status
            }
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            response = requests.post(
                f"{self.base_url}/members",
                headers=self.headers,
                json=data,
                verify=False,  # Disable SSL verification
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Added member: {member.name}")
                return True
            else:
                print(f"❌ Failed to add member: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error adding member: {e}")
            return False
    
    def update_member(self, member: Member) -> bool:
        """Update an existing member in Supabase using HTTP"""
        if not self.base_url:
            return False
        
        try:
            data = {
                'title': member.title,
                'name': member.name,
                'phone': member.phone,
                'birthday': member.birthday,
                'wedding_anniversary': member.wedding_anniversary,
                'spouse_name': member.spouse_name,
                'email': member.email,
                'relationship_status': member.relationship_status
            }
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            response = requests.patch(
                f"{self.base_url}/members?id=eq.{member.id}",
                headers=self.headers,
                json=data,
                verify=False,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"✅ Updated member: {member.name}")
                return True
            else:
                print(f"❌ Failed to update member: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error updating member: {e}")
            return False
    
    def delete_member(self, member_id: str) -> bool:
        """Delete a member from Supabase using HTTP"""
        if not self.base_url:
            return False
        
        try:
            response = requests.delete(
                f"{self.base_url}/members?id=eq.{member_id}",
                headers=self.headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"✅ Deleted member ID: {member_id}")
                return True
            else:
                print(f"❌ Failed to delete member: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error deleting member: {e}")
            return False
    
    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        """Get a member by ID using HTTP"""
        if not self.base_url:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/members?id=eq.{member_id}",
                headers=self.headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    item = data[0]
                    member = Member(
                        id=item.get('id'),
                        title=item.get('title', 'Mr.'),
                        name=item.get('name', ''),
                        phone=item.get('phone', ''),
                        birthday=item.get('birthday', ''),
                        wedding_anniversary=item.get('wedding_anniversary'),
                        spouse_name=item.get('spouse_name'),
                        email=item.get('email'),
                        relationship_status=item.get('relationship_status', 'Single')
                    )
                    return member
            
            return None
            
        except Exception as e:
            print(f"Error getting member by ID: {e}")
            return None
    
    def get_members_by_date(self, date_str: str, event_type: str) -> List[Member]:
        """Get members by birthday or anniversary date using HTTP"""
        if not self.base_url:
            return []
        
        try:
            field_name = 'birthday' if event_type == 'birthday' else 'wedding_anniversary'
            
            response = requests.get(
                f"{self.base_url}/members?{field_name}=eq.{date_str}",
                headers=self.headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                members = []
                
                for item in data:
                    member = Member(
                        id=item.get('id'),
                        title=item.get('title', 'Mr.'),
                        name=item.get('name', ''),
                        phone=item.get('phone', ''),
                        birthday=item.get('birthday', ''),
                        wedding_anniversary=item.get('wedding_anniversary'),
                        spouse_name=item.get('spouse_name'),
                        email=item.get('email'),
                        relationship_status=item.get('relationship_status', 'Single')
                    )
                    members.append(member)
                
                return members
            else:
                return []
                
        except Exception:
            return []


# Hybrid Database Manager (SQLite + Supabase)
class HybridDatabaseManager:
    """Database manager that can use SQLite locally or Supabase as cloud database"""
    
    def __init__(self):
        use_supabase = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
        
        if use_supabase:
            self.supabase_db = SupabaseManager()
            self.use_supabase = self.supabase_db.is_available
            if self.use_supabase:
                print("🌐 Using Supabase as cloud database")
            else:
                print("📱 Supabase failed, falling back to SQLite")
                from db import DatabaseManager
                self.sqlite_db = DatabaseManager()
                self.use_supabase = False
        else:
            from db import DatabaseManager
            self.sqlite_db = DatabaseManager()
            self.use_supabase = False
            print("💾 Using SQLite local database")
    
    def get_all_members(self) -> List[Member]:
        if self.use_supabase:
            return self.supabase_db.get_all_members()
        else:
            return self.sqlite_db.get_all_members()
    
    def add_member(self, member: Member) -> bool:
        if self.use_supabase:
            return self.supabase_db.add_member(member)
        else:
            return self.sqlite_db.add_member(member)
    
    def update_member(self, member: Member) -> bool:
        if self.use_supabase:
            return self.supabase_db.update_member(member)
        else:
            return self.sqlite_db.update_member(member)
    
    def delete_member(self, member_id: str) -> bool:
        if self.use_supabase:
            return self.supabase_db.delete_member(member_id)
        else:
            return self.sqlite_db.delete_member(member_id)
    
    def get_members_by_date(self, date_str: str, event_type: str) -> List[Member]:
        if self.use_supabase:
            return self.supabase_db.get_members_by_date(date_str, event_type)
        else:
            return self.sqlite_db.get_members_by_date(date_str, event_type)
    
    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        if self.use_supabase:
            return self.supabase_db.get_member_by_id(member_id)
        else:
            return self.sqlite_db.get_member_by_id(member_id)
