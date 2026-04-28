import os
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from dotenv import load_dotenv

load_dotenv()

# Xero Scopes needed for this project
SCOPES = [
    "openid", "profile", "email", "accounting.transactions", 
    "accounting.settings", "offline_access", "payments"
]

def get_xero_config():
    return Configuration(
        oauth2_token=OAuth2Token(
            client_id=os.getenv("XERO_CLIENT_ID"),
            client_secret=os.getenv("XERO_CLIENT_SECRET"),
        ),
    )

def get_api_client():
    config = get_xero_config()
    return ApiClient(config)

def get_authorization_url():
    """
    Generates the Xero authorization URL for the user to login.
    """
    client = get_api_client()
    redirect_uri = os.getenv("XERO_REDIRECT_URI", "http://localhost:8080/callback")
    return client.get_authorization_url(redirect_uri, scope=" ".join(SCOPES))

def handle_callback(url_with_code: str):
    """
    Exchanges the authorization code from the callback URL for an access token.
    """
    client = get_api_client()
    redirect_uri = os.getenv("XERO_REDIRECT_URI", "http://localhost:8080/callback")
    token = client.get_token_by_auth_sucess_url(url_with_code, redirect_uri)
    
    # TODO: Store this token securely (e.g., in GCP Secret Manager or encrypted DB)
    return token

def get_token():
    """
    Placeholder for retrieving the stored token.
    """
    # In a real app, this would fetch from Secret Manager or a DB
    return None
