import os
import firebase_admin
from firebase_admin import credentials
import logging
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  # Load variables from .env file

def initialize_firebase():
    if not firebase_admin._apps:  # avoid reinitialization
        firebase_config = st.secrets["firebase"]

        cred = credentials.Certificate({
            "type": firebase_config["type"],
            "project_id": firebase_config["project_id"],
            "private_key_id": firebase_config["private_key_id"],
            "private_key": firebase_config["private_key"].replace("\\n", "\n"),
            "client_email": firebase_config["client_email"],
            "client_id": firebase_config["client_id"],
            "auth_uri": firebase_config["auth_uri"],
            "token_uri": firebase_config["token_uri"],
            "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
            "client_x509_cert_url": firebase_config["client_x509_cert_url"],
        })

        firebase_admin.initialize_app(cred)
