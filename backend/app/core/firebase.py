import os
from firebase_admin import credentials, initialize_app
import logging

# Get environment variables
private_key = os.getenv('FIREBASE_PRIVATE_KEY')
if private_key:
    # Replace literal \n with actual newlines
    private_key = private_key.replace('\\n', '\n')

try:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key": private_key,
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
    })
    
    app = initialize_app(cred)
    logging.info("Firebase initialized successfully")
except Exception as e:
    logging.error(f"Error initializing Firebase: {str(e)}")
    # Don't raise the exception, just log it
    app = None

async def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}") 