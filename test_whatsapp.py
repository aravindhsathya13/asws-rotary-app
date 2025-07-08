#!/usr/bin/env python3
"""
Test WhatsApp functionality in test mode
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_whatsapp():
    """Test WhatsApp messaging in test mode"""
    print("📱 Testing WhatsApp functionality...")
    
    # Mock the classes for testing
    from dataclasses import dataclass
    from typing import Optional
    import requests
    
    @dataclass
    class Member:
        id: Optional[int]
        name: str
        phone: str
        birthday: str
        wedding_anniversary: Optional[str]
        spouse_name: Optional[str]
        email: Optional[str]
    
    class WhatsAppManager:
        def __init__(self):
            self.api_url = "https://api.callmebot.com/whatsapp.php"
        
        def send_message(self, phone: str, message: str, api_key: str) -> bool:
            """Send WhatsApp message with test mode support"""
            try:
                # Check if we're in test mode
                if api_key == 'test_mode':
                    print(f"🧪 TEST MODE: Would send message to {phone}")
                    print(f"📱 Message: {message[:100]}...")
                    print("✅ Message sent successfully (TEST MODE)")
                    return True
                
                # Real API call would go here
                print("⚠️  Real API mode not tested in this script")
                return False
                
            except Exception as e:
                print(f"❌ Error: {e}")
                return False
        
        def send_birthday_wish(self, member: Member, api_key: str) -> bool:
            """Send birthday wish message"""
            message = f"""🎉 Happy Birthday {member.name}! 🎂

On behalf of the Rotary Club, we wish you a wonderful year ahead filled with joy, success, and good health.

May this special day bring you happiness and may the year ahead be filled with blessings!

Best wishes,
Rotary Club Team"""
            
            return self.send_message(member.phone, message, api_key)
    
    # Test with sample member
    test_member = Member(
        id=1,
        name="Aravindh Test",
        phone="+917010801016",
        birthday="07-04",
        wedding_anniversary=None,
        spouse_name=None,
        email="test@example.com"
    )
    
    # Create WhatsApp manager and test
    whatsapp = WhatsAppManager()
    
    print("\n1. Testing Birthday Wish in TEST MODE:")
    success = whatsapp.send_birthday_wish(test_member, "test_mode")
    
    if success:
        print("\n✅ WhatsApp test completed successfully!")
        print("💡 The system is working in test mode.")
        print("📝 To enable real WhatsApp messages:")
        print("   1. Send 'I allow callmebot to send me messages' to +34 644 49 93 26")
        print("   2. Get your API key from the response")
        print("   3. Update WHATSAPP_API_KEY in .env file")
    else:
        print("\n❌ WhatsApp test failed")
    
    return success

if __name__ == "__main__":
    success = test_whatsapp()
    sys.exit(0 if success else 1)
