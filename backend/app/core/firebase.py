import os
from firebase_admin import credentials, initialize_app, auth
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
project_id = os.getenv('FIREBASE_PROJECT_ID')
private_key = os.getenv('FIREBASE_PRIVATE_KEY')
client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
client_x509_cert_url = os.getenv('FIREBASE_CLIENT_X509_CERT_URL')

# Check required environment variables
if not all([project_id, private_key, client_email]):
    logger.error("Missing required Firebase environment variables")
    logger.error(f"PROJECT_ID: {'Set' if project_id else 'Missing'}")
    logger.error(f"PRIVATE_KEY: {'Set' if private_key else 'Missing'}")
    logger.error(f"CLIENT_EMAIL: {'Set' if client_email else 'Missing'}")
    app = None
else:
    try:
        # Replace literal \n with actual newlines in private key
        private_key = private_key.replace('\\n', '\n')
        
        logger.info(f"Initializing Firebase with project ID: {project_id}")
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
            logger.error(f"Private key starts with: {private_key[:50]}...")
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