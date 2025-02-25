# Louis's LinkedIn Profile Agent Team

A unified Python package for managing LinkedIn profile operations, combining authentication and posting capabilities into a single, easy-to-use interface.

## Features

- 🔐 LinkedIn OAuth2 authentication
- 📝 Post content to your LinkedIn profile
- 🔄 Automatic token management
- 🛡️ Secure credential handling
- 🚀 Simple, unified interface

## Installation

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/louis_linkedin_profile_agent_team.git
   cd louis_linkedin_profile_agent_team
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## Configuration

1. Create a `.env` file in your project root with your LinkedIn API credentials:
   ```env
   LINKEDIN_CLIENT_ID=your_client_id_here
   LINKEDIN_CLIENT_SECRET=your_client_secret_here
   LINKEDIN_REDIRECT_URI=http://localhost:8000
   ```

## Usage

### Basic Usage

```python
from louis_linkedin_profile_agent_team import LinkedInProfileAgent

# Initialize the agent
agent = LinkedInProfileAgent()

# Ensure authentication (this will prompt for auth if needed)
auth_result = agent.ensure_authenticated()
if auth_result["success"]:
    # Post content to LinkedIn
    post_result = agent.post_content(
        "🚀 Excited to share my latest project!\n\n"
        "I've been working on AI-driven automation tools "
        "that make social media management a breeze.\n\n"
        "#Innovation #AI #LinkedIn #Automation"
    )
    
    if post_result["success"]:
        print("Posted successfully!")
        print(f"Post ID: {post_result.get('post_id')}")
    else:
        print(f"Posting failed: {post_result['message']}")
else:
    print(f"Authentication failed: {auth_result['message']}")
```

### Advanced Usage

You can also access the individual agents directly:

```python
from louis_linkedin_profile_agent_team import LinkedInProfileAgent

agent = LinkedInProfileAgent()

# Access auth agent
auth_url = agent.auth_agent.get_authorization_url()

# Access posting agent
post_result = agent.posting_agent.post_content("Hello LinkedIn!")
```

## Security Notes

- Never commit your `.env` file or `token.json` to version control
- Keep your LinkedIn API credentials secure
- The `.gitignore` file is configured to exclude sensitive files

## File Structure

```
louis_linkedin_profile_agent_team/
├── louis_linkedin_profile_agent_team/
│   ├── __init__.py              # Expose main agent class
│   ├── auth.py                  # Authentication logic
│   ├── posting.py               # Posting logic
│   └── profile_agent.py         # Unified interface
├── .gitignore                   # Ignore sensitive files
├── README.md                    # This file
├── requirements.txt             # Dependencies
└── setup.py                     # For pip installation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This package builds upon the LinkedIn API and combines authentication and posting capabilities into a unified interface.
