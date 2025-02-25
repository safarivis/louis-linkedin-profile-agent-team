"""
LinkedIn Posting Agent - Core posting functionality
"""
import json
import time
from typing import Dict, Optional, Union
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LinkedInPostingAgent:
    """Agent for posting content to LinkedIn"""
    
    def __init__(self):
        """Initialize the LinkedIn Posting Agent"""
        self.base_url = "https://api.linkedin.com/v2"
        # Look for token.json in the parent directory
        self.token_file = Path(__file__).parent.parent.parent / "token.json"
        self._load_token()
    
    def _load_token(self):
        """Load the access token from file"""
        if not self.token_file.exists():
            raise FileNotFoundError(f"token.json not found at {self.token_file}. Please run the auth agent first.")
            
        with open(self.token_file) as f:
            self.token_data = json.load(f)
            
        # Check if token is expired
        created_at = self.token_data.get('created_at', 0)
        expires_in = self.token_data.get('expires_in', 0)
        if time.time() > created_at + expires_in:
            raise Exception("Access token has expired. Please refresh the token.")
            
        self.access_token = self.token_data['access_token']
    
    def _get_user_profile(self) -> Optional[str]:
        """Get the user's LinkedIn profile URN"""
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            response = requests.get(
                f"{self.base_url}/userinfo",  # Using OpenID Connect userinfo endpoint
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return f"urn:li:person:{data['sub']}"  # OpenID Connect provides 'sub' as the user ID
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response.status_code == 401:
                raise Exception("Access token has expired or is invalid")
            raise Exception(f"Failed to fetch user profile: {str(e)}")

    def post_content(self, text: str) -> Dict[str, Union[bool, str]]:
        """
        Post text content to LinkedIn
        
        Args:
            text (str): The text content to post
            
        Returns:
            dict: Response containing success status and message
            
        Raises:
            Exception: If posting fails
        """
        try:
            # Validate input
            if not text or not isinstance(text, str):
                raise ValueError("Text content must be a non-empty string")

            # Get user profile URN
            author = self._get_user_profile()
            
            # Prepare the post payload
            post_data = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Make the post request
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=headers,
                json=post_data  # Using json parameter for proper JSON encoding
            )
            
            response.raise_for_status()
            
            return {
                "success": True,
                "message": "Content posted successfully",
                "post_id": response.json().get("id", "")
            }
            
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response.status_code == 401:
                return {
                    "success": False,
                    "message": "Authentication failed. Token may have expired.",
                    "error": str(e)
                }
            return {
                "success": False,
                "message": f"HTTP error occurred: {str(e)}",
                "error": str(e)
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Network error occurred: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"An unexpected error occurred: {str(e)}",
                "error": str(e)
            }
