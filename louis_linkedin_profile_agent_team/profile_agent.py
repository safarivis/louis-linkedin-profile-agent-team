"""
LinkedIn Profile Agent - Unified interface for LinkedIn profile operations
"""
from typing import Dict, Union, Optional
from pathlib import Path
import os
from dotenv import load_dotenv
from .auth import LinkedInAuthAgent
from .posting import LinkedInPostingAgent

class LinkedInProfileAgent:
    """Unified agent for managing a LinkedIn profile"""
    
    def __init__(self, auto_load_env: bool = True):
        """
        Initialize the LinkedIn Profile Agent
        
        Args:
            auto_load_env (bool): If True, automatically load environment variables from .env
        """
        if auto_load_env:
            load_dotenv()
            
        # Get credentials from environment
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError(
                "Missing LinkedIn credentials. Please set LINKEDIN_CLIENT_ID, "
                "LINKEDIN_CLIENT_SECRET, and LINKEDIN_REDIRECT_URI in your .env file"
            )
        
        # Initialize sub-agents
        self.auth_agent = LinkedInAuthAgent(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri
        )
        self.posting_agent = LinkedInPostingAgent()
    
    def authenticate(self) -> Dict[str, Union[bool, str]]:
        """
        Authenticate with LinkedIn and get an access token
        
        Returns:
            dict: Response containing success status and message
        """
        try:
            # Generate authorization URL
            auth_url = self.auth_agent.get_authorization_url()
            
            print("\nPlease visit this URL to authorize the application:")
            print(auth_url)
            print("\nAfter authorization, you will be redirected to your redirect URI.")
            
            # Start local server to receive the auth code
            self.auth_agent.start_auth_server()
            
            return {
                "success": True,
                "message": "Authentication successful. Token saved to token.json"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Authentication failed: {str(e)}"
            }
    
    def post_content(self, text: str) -> Dict[str, Union[bool, str]]:
        """
        Post content to LinkedIn
        
        Args:
            text (str): The text content to post
            
        Returns:
            dict: Response containing success status and message
        """
        return self.posting_agent.post_content(text)
    
    def is_authenticated(self) -> bool:
        """
        Check if we have a valid token
        
        Returns:
            bool: True if we have a valid token, False otherwise
        """
        token_file = Path("token.json")
        return token_file.exists()
    
    def ensure_authenticated(self) -> Dict[str, Union[bool, str]]:
        """
        Ensure we have a valid token, authenticate if needed
        
        Returns:
            dict: Response containing success status and message
        """
        if not self.is_authenticated():
            return self.authenticate()
        return {"success": True, "message": "Already authenticated"}
