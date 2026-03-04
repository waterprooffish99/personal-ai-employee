from setuptools import setup, find_packages

setup(
    name="personal-ai-employee",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "watchdog",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "ai-employee=src.orchestrator:main",
        ],
    },
)