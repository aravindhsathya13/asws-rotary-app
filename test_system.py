#!/usr/bin/env python3
"""
Test Script for Rotary Club Anniversary Management System
This script tests basic functionality before deployment
"""

import os
import sys
import sqlite3
from datetime import datetime, date

def test_database():
    """Test database operations"""
    print("🗄️  Testing database operations...")
    
    try:
        # Test database creation
        from Untitled1 import DatabaseManager
        db = DatabaseManager("test_rotary.db")
        
        # Test adding a member
        from Untitled1 import Member
        test_member = Member(
            id=None,
            name="Test Member",
            phone="+1234567890",
            birthday="03-15",
            wedding_anniversary="06-20",
            spouse_name="Test Spouse",
            email="test@example.com"
        )
        
        success = db.add_member(test_member)
        if success:
            print("✅ Database operations working")
        else:
            print("❌ Database operations failed")
            return False
            
        # Test retrieving members
        members = db.get_all_members()
        if len(members) > 0:
            print(f"✅ Retrieved {len(members)} members")
        else:
            print("❌ Failed to retrieve members")
            return False
            
        # Cleanup test database
        os.remove("test_rotary.db")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_whatsapp_config():
    """Test WhatsApp configuration"""
    print("📱 Testing WhatsApp configuration...")
    
    api_key = os.environ.get('WHATSAPP_API_KEY')
    admin_phone = os.environ.get('ADMIN_PHONE')
    
    if api_key and api_key != 'your_callmebot_api_key_here':
        print("✅ WhatsApp API key configured")
    else:
        print("⚠️  WhatsApp API key not configured (add to .env file)")
        
    if admin_phone and admin_phone.startswith('+'):
        print("✅ Admin phone number configured")
    else:
        print("⚠️  Admin phone number not configured (add to .env file)")
        
    return True

def test_flask_imports():
    """Test Flask and web components"""
    print("🌐 Testing Flask imports...")
    
    try:
        from flask import Flask
        from Untitled1 import app
        print("✅ Flask imports working")
        return True
    except Exception as e:
        print(f"❌ Flask imports failed: {e}")
        return False

def test_scheduling():
    """Test scheduling functionality"""
    print("⏰ Testing scheduling functionality...")
    
    try:
        import schedule
        print("✅ Scheduling module working")
        return True
    except Exception as e:
        print(f"❌ Scheduling test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🎯 Rotary Club Anniversary System - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_flask_imports,
        test_database,
        test_whatsapp_config,
        test_scheduling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
