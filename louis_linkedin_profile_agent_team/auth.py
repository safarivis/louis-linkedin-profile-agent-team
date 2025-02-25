import requests
from urllib.parse import urlencode, parse_qs, urlparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
from typing import Optional
from dotenv import load_dotenv
import os
import sys
import time
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

class LinkedInAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_code: Optional[str] = None
        
        # LinkedIn OpenID Connect endpoints
        self.AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
        self.TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
        self.USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
        
        # Define the scope of permissions you need
        self.SCOPE = ["openid", "profile", "email", "w_member_social"]  # OpenID Connect scopes

    def get_authorization_url(self) -> str:
        """Generate the authorization URL for LinkedIn OAuth."""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.SCOPE),
            "state": "random_state_string"  # In production, use a secure random string
        }
        auth_url = f"{self.AUTH_URL}?{urlencode(params)}"
        print(f"Generated authorization URL: {auth_url}")
        return auth_url

    def exchange_code_for_token(self, authorization_code: str) -> dict:
        """Exchange the authorization code for an access token."""
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        
        print(f"Exchanging code for token with data: {data}")
        response = requests.post(self.TOKEN_URL, data=data)
        if response.status_code != 200:
            print(f"Error response from LinkedIn: {response.text}")
            raise Exception(f"Failed to get access token: {response.text}")
        
        token_info = response.json()
        
        # Get user info using the access token
        headers = {
            "Authorization": f"Bearer {token_info['access_token']}"
        }
        userinfo_response = requests.get(self.USERINFO_URL, headers=headers)
        user_info = {}
        if userinfo_response.status_code == 200:
            user_info = userinfo_response.json()
            print("\nUser Info:", json.dumps(user_info, indent=2))

        # Save token and user info to file
        token_data = {
            "access_token": token_info["access_token"],
            "expires_in": token_info["expires_in"],
            "token_type": token_info.get("token_type", "Bearer"),
            "scope": token_info.get("scope", " ".join(self.SCOPE)),
            "user_info": user_info,
            "created_at": int(time.time())
        }
        
        with open("token.json", "w") as f:
            json.dump(token_data, f, indent=4)
            print("\nToken information saved to token.json")
        
        return token_info

class AuthCodeHandler(BaseHTTPRequestHandler):
    auth_code = None
    
    def do_GET(self):
        """Handle the OAuth callback."""
        print(f"Received callback with path: {self.path}")
        query_components = parse_qs(urlparse(self.path).query)
        print(f"Query components: {query_components}")
        
        if 'error' in query_components:
            error = query_components['error'][0]
            error_description = query_components.get('error_description', ['No description'])[0]
            print(f"Error in OAuth callback: {error} - {error_description}")
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"Authorization failed: {error_description}".encode())
            return
        
        if 'code' in query_components:
            AuthCodeHandler.auth_code = query_components['code'][0]
            print(f"Received authorization code: {AuthCodeHandler.auth_code}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
        else:
            print("No authorization code found in callback")
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization failed! No code received.")
    
    def log_message(self, format, *args):
        """Override to print server logs to stdout"""
        print(f"Server log: {format%args}")

def main():
    # Load credentials from environment variables
    CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8001')
    
    print(f"Using redirect URI: {REDIRECT_URI}")
    
    if not all([CLIENT_ID, CLIENT_SECRET]):
        print("Error: Please set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in your .env file")
        return
    
    # Initialize LinkedIn OAuth handler
    linkedin_auth = LinkedInAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    
    # Get the authorization URL
    auth_url = linkedin_auth.get_authorization_url()
    
    # Start local server to handle the OAuth callback
    server = HTTPServer(('localhost', 8001), AuthCodeHandler)
    
    print("Opening browser for LinkedIn authorization...")
    print(f"Please authorize the application at: {auth_url}")
    webbrowser.open(auth_url)
    
    print("Waiting for authorization code...")
    server.handle_request()
    
    if AuthCodeHandler.auth_code:
        try:
            # Exchange the authorization code for an access token
            token_info = linkedin_auth.exchange_code_for_token(AuthCodeHandler.auth_code)
            print("\nAccess Token obtained successfully!")
            print(f"Access Token: {token_info['access_token']}")
            print(f"Expires in: {token_info['expires_in']} seconds")
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
    else:
        print("Failed to get authorization code")

if __name__ == "__main__":
    main()
