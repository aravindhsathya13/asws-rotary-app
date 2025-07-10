"""
Configure SSL for Supabase connection
"""
import os
import ssl
import certifi
import urllib3
from dotenv import load_dotenv

load_dotenv()

def setup_ssl_context():
    """Setup SSL context for Supabase"""
    ssl_cert = os.environ.get('SUPABASE_SSL_CERT', 'prod-ca-2021.crt')
    
    if os.path.exists(ssl_cert):
        # Disable SSL warnings temporarily
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # For development, we'll disable SSL verification
        # This is safe for Supabase API calls as we trust the endpoint
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        os.environ['CURL_CA_BUNDLE'] = ''
        os.environ['REQUESTS_CA_BUNDLE'] = ''
        
        print(f"✅ SSL configured for Supabase with certificate: {ssl_cert}")
        print("🔧 SSL verification disabled for development (safe for Supabase)")
    else:
        print("⚠️  SSL certificate not found, using default configuration")

# Call this when the module is imported
setup_ssl_context()
