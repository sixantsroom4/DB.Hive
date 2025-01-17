import os
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, auth
import logging
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_private_key(key: str) -> str:
    """Format private key with proper line breaks and headers."""
    # Remove any existing formatting
    key = key.replace('\\n', '')
    key = key.replace('\n', '')
    key = key.strip()
    
    # Remove surrounding quotes if present
    if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    
    # Remove existing headers if present
    key = key.replace('-----BEGIN PRIVATE KEY-----', '')
    key = key.replace('-----END PRIVATE KEY-----', '')
    key = key.strip()
    
    # Insert a line break every 64 characters
    key_parts = [key[i:i+64] for i in range(0, len(key), 64)]
    formatted_key = '\n'.join(key_parts)
    
    # Add headers
    return f"-----BEGIN PRIVATE KEY-----\n{formatted_key}\n-----END PRIVATE KEY-----"

# Get environment variables
project_id = os.getenv('FIREBASE_PROJECT_ID')
private_key = os.getenv('FIREBASE_PRIVATE_KEY')
client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
client_x509_cert_url = os.getenv('FIREBASE_CLIENT_X509_CERT_URL')

# Log environment variable status
logger.info("Checking Firebase environment variables...")
logger.info(f"PROJECT_ID: {'Set' if project_id else 'Missing'}")
logger.info(f"PRIVATE_KEY: {'Set (length: ' + str(len(private_key)) + ')' if private_key else 'Missing'}")
logger.info(f"CLIENT_EMAIL: {'Set' if client_email else 'Missing'}")

# Check required environment variables
if not all([project_id, private_key, client_email]):
    logger.error("Missing required Firebase environment variables")
    app = None
else:
    try:
        # Format the private key
        private_key = format_private_key(private_key)
        logger.info("Private key formatted successfully")
        
        logger.info(f"Initializing Firebase with project ID: {project_id}")
        logger.info(f"Using client email: {client_email}")
        
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": project_id,
            "private_key": private_key,
            "client_email": client_email,
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": client_x509_cert_url
        })
        
        app = initialize_app(cred)
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Firebase: {str(e)}")
        # Log the first few characters of the private key for debugging
        if private_key:
            logger.error(f"Private key format check - Starts with: {private_key[:50]}")
            logger.error(f"Private key format check - Ends with: {private_key[-50:]}")
        app = None

async def verify_firebase_token(token: str):
    if app is None:
        logger.error("Firebase app not initialized")
        raise ValueError("Firebase authentication is not available")
        
    try:
        decoded_token = auth.verify_id_token(token)
        logger.info(f"Token verified successfully for user: {decoded_token.get('uid')}")
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}") 