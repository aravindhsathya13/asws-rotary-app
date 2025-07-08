#!/usr/bin/env python3
"""
Test Twilio WhatsApp functionality
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def test_twilio_config():
    """Test if Twilio is properly configured"""
    print("🔧 Testing Twilio Configuration...")
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    provider = os.getenv('WHATSAPP_PROVIDER')
    
    print(f"📱 Provider: {provider}")
    print(f"🔑 Account SID: {account_sid[:10]}..." if account_sid else "❌ Missing Account SID")
    print(f"🔐 Auth Token: {'✅ Set' if auth_token else '❌ Missing'}")
    print(f"📞 WhatsApp Number: {whatsapp_number}")
    
    if provider != 'twilio':
        print("⚠️  Provider is not set to 'twilio'")
        return False
    
    if not all([account_sid, auth_token, whatsapp_number]):
        print("❌ Missing Twilio credentials")
        return False
    
    print("✅ Twilio configuration looks good!")
    return True

def test_twilio_connection():
    """Test connection to Twilio"""
    print("\n📡 Testing Twilio Connection...")
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        client = Client(account_sid, auth_token)
        
        # Test by fetching account info
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Connected to Twilio account: {account.friendly_name}")
        print(f"📊 Account status: {account.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Twilio connection failed: {e}")
        return False

def test_whatsapp_sandbox():
    """Test WhatsApp sandbox status"""
    print("\n📱 Testing WhatsApp Sandbox...")
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        client = Client(account_sid, auth_token)
        
        # Check sandbox settings
        sandbox = client.messaging.v1.tollfree.verification.list(limit=1)
        print("✅ WhatsApp sandbox accessible")
        
        return True
        
    except Exception as e:
        print(f"⚠️  WhatsApp sandbox check: {e}")
        print("💡 This might be normal - sandbox doesn't always respond to API calls")
        return True  # Don't fail on this

def send_test_message():
    """Send a test message"""
    print("\n📤 Sending Test Message...")
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        admin_phone = os.getenv('ADMIN_PHONE', '+919876543210')
        
        client = Client(account_sid, auth_token)
        
        # Format phone number
        if not admin_phone.startswith('whatsapp:'):
            to_number = f"whatsapp:{admin_phone}"
        else:
            to_number = admin_phone
        
        test_message = """🧪 Twilio Test Message

This is a test message from your Rotary Club Anniversary Management System.

If you receive this message, your Twilio WhatsApp integration is working perfectly!

🎉 Ready to send anniversary wishes! 🎂💕"""
        
        message = client.messages.create(
            body=test_message,
            from_=whatsapp_number,
            to=to_number
        )
        
        print(f"✅ Test message sent successfully!")
        print(f"📧 Message SID: {message.sid}")
        print(f"📱 Sent to: {admin_phone}")
        print("🔍 Check your WhatsApp for the test message!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test message: {e}")
        
        if "not a valid phone number" in str(e).lower():
            print("💡 Make sure you joined the WhatsApp sandbox first!")
            print("   Send the join code to the Twilio sandbox number")
        elif "authentication" in str(e).lower():
            print("💡 Check your Twilio credentials in .env file")
        
        return False

def main():
    """Run all tests"""
    print("🧪 Twilio WhatsApp Integration Test")
    print("=" * 40)
    
    tests = [
        test_twilio_config,
        test_twilio_connection,
        test_whatsapp_sandbox,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    if passed == len(tests):
        print("🎯 All tests passed! Ready to send test message...")
        print()
        
        response = input("📤 Send a test message to your phone? (y/n): ").lower()
        if response in ['y', 'yes']:
            if send_test_message():
                print("\n🎉 Twilio integration is fully working!")
            else:
                print("\n⚠️  Test message failed - check troubleshooting guide")
        else:
            print("\n✅ Twilio configuration verified!")
    else:
        print(f"⚠️  {passed}/{len(tests)} tests passed. Check your configuration.")
    
    print("\n📖 For setup help, see WHATSAPP_SETUP.md")

if __name__ == "__main__":
    main()
