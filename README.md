# Louis's LinkedIn Profile Agent Team

A unified Python package for managing LinkedIn profile operations, combining authentication and posting capabilities into a single, easy-to-use interface.

## Features

- 🔐 LinkedIn OAuth2 authentication
- 📝 Post content to your LinkedIn profile
- 🔄 Automatic token management
- 🛡️ Secure credential handling
- 🚀 Simple, unified interface

## Setup Guide

### 1. LinkedIn API Credentials

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Create a new app or use an existing one
3. Get your credentials:
   - Client ID
   - Client Secret
4. Set up OAuth 2.0 settings:
   - Add redirect URL: `http://localhost:8000`
   - Request the following OAuth 2.0 Scopes:
     - `r_liteprofile`
     - `w_member_social`

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/safarivis/louis-linkedin-profile-agent-team.git
cd louis-linkedin-profile-agent_team

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### 3. Configuration

Create a `.env` file in your project root:

```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000
```

## Quick Start

### 1. Basic Usage

```python
from louis_linkedin_profile_agent_team import LinkedInProfileAgent

# Initialize the agent
agent = LinkedInProfileAgent()

# First-time setup: This will open your browser for authentication
auth_result = agent.ensure_authenticated()
if not auth_result["success"]:
    print(f"Authentication failed: {auth_result['message']}")
    exit(1)

# Post content
post_result = agent.post_content(
    "🚀 Testing my LinkedIn automation!\n\n"
    "Successfully integrated with the LinkedIn API "
    "using my new Python package.\n\n"
    "#Python #Automation #LinkedIn"
)

if post_result["success"]:
    print("Posted successfully!")
    print(f"Post ID: {post_result.get('post_id')}")
else:
    print(f"Posting failed: {post_result['message']}")
```

### 2. Save this as a Script

Create a file named `test_post.py`:

```python
from louis_linkedin_profile_agent_team import LinkedInProfileAgent
from datetime import datetime

def main():
    # Initialize agent
    agent = LinkedInProfileAgent()
    
    # Ensure we're authenticated
    auth_result = agent.ensure_authenticated()
    if not auth_result["success"]:
        print(f"Authentication failed: {auth_result['message']}")
        return
    
    # Create post content
    post_content = (
        "🤖 Automated Post\n\n"
        "Testing my LinkedIn automation package.\n\n"
        f"Posted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "#LinkedInAutomation #Python"
    )
    
    # Post to LinkedIn
    result = agent.post_content(post_content)
    
    if result["success"]:
        print("✅ Posted successfully!")
        print(f"Post ID: {result.get('post_id')}")
    else:
        print(f"❌ Posting failed: {result['message']}")

if __name__ == "__main__":
    main()
```

### 3. Run the Script

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the test script
python test_post.py
```

## First-Time Authentication Flow

1. When you run the script for the first time, it will:
   - Open your default web browser
   - Redirect to LinkedIn login (if not already logged in)
   - Ask for permission to access your profile
   - Redirect back to localhost

2. After successful authentication:
   - The token will be saved to `token.json`
   - Future runs will use this token automatically
   - Tokens are refreshed automatically when expired

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your LinkedIn API credentials in `.env`
   - Ensure redirect URI matches exactly
   - Check if you have the required OAuth scopes

2. **Posting Failed**
   - Verify your token is valid
   - Ensure you have the `w_member_social` scope
   - Check if your post content follows LinkedIn guidelines

3. **Token Issues**
   - Delete `token.json` and re-authenticate if you encounter persistent token problems
   - Ensure your system time is correct
   - Check if your LinkedIn API app is still active

## Security Notes

- Never commit `.env` or `token.json` to version control
- Keep your LinkedIn API credentials secure
- Regularly rotate your API credentials
- Monitor your LinkedIn app's usage in the Developer Portal

Need help? Open an issue on GitHub!
