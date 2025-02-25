from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="louis_linkedin_profile_agent_team",
    version="0.1.0",
    author="Louis",
    author_email="your.email@example.com",
    description="A unified package for managing LinkedIn profile operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/louis_linkedin_profile_agent_team",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
)
