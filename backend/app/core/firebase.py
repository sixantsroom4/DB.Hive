import os
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, auth
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # Clean and format private key
        private_key = private_key.strip()
        if private_key.startswith('"') and private_key.endswith('"'):
            private_key = private_key[1:-1]
        if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
            private_key = '-----BEGIN PRIVATE KEY-----\n' + private_key
        if not private_key.endswith('-----END PRIVATE KEY-----'):
            private_key = private_key + '\n-----END PRIVATE KEY-----'
        
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