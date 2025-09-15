import os
import firebase_admin
from firebase_admin import credentials
import logging
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

def initialize_firebase():
    try:
        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not key_path:
            raise ValueError("Firebase credentials path not found in environment variables.")

        cred = credentials.Certificate(key_path)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            logging.info("Firebase successfully initialized.")
        else:
            logging.info("Firebase is already initialized.")
    
    except Exception as e:
        logging.error(f"Error initializing Firebase: {e}")
        raise
