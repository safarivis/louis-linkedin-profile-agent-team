"""
Louis's LinkedIn Profile Agent Team
A unified package for managing LinkedIn profile operations
"""

from .profile_agent import LinkedInProfileAgent
from .auth import LinkedInAuthAgent
from .posting import LinkedInPostingAgent

__version__ = '0.1.0'
__all__ = ['LinkedInProfileAgent', 'LinkedInAuthAgent', 'LinkedInPostingAgent']
