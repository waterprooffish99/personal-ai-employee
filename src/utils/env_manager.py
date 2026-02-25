import os
from dotenv import load_dotenv
from pathlib import Path


class EnvManager:
    """Environment variable manager for the AI Employee system."""

    def __init__(self, env_file_path: str = ".env"):
        """
        Initialize the environment manager.

        Args:
            env_file_path: Path to the .env file
        """
        self.env_file_path = Path(env_file_path)
        self._load_environment()

    def _load_environment(self):
        """Load environment variables from .env file."""
        if self.env_file_path.exists():
            load_dotenv(self.env_file_path, override=True)
        else:
            # Create a default .env file if it doesn't exist
            self._create_default_env_file()
            load_dotenv(self.env_file_path, override=True)

    def _create_default_env_file(self):
        """Create a default .env file with required variables."""
        default_env_content = """# AI Employee System Configuration

# Claude API Configuration
CLAUDE_API_KEY=

# Gmail Configuration
GMAIL_API_KEY=
GMAIL_USER_EMAIL=

# WhatsApp Configuration
WHATSAPP_SESSION_FILE=

# Odoo Configuration
ODOO_URL=
ODOO_DB=
ODOO_USERNAME=
ODOO_PASSWORD=

# System Configuration
DRY_RUN=true
VAULT_PATH=AI_Employee_Vault
LOG_LEVEL=INFO

# Other Configuration
MAX_RETRIES=3
BACKOFF_FACTOR=1.0
"""
        with open(self.env_file_path, 'w') as f:
            f.write(default_env_content)

    def get(self, key: str, default=None):
        """
        Get an environment variable.

        Args:
            key: Environment variable key
            default: Default value if key doesn't exist

        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get an environment variable as a boolean.

        Args:
            key: Environment variable key
            default: Default value if key doesn't exist

        Returns:
            Boolean value of environment variable
        """
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get an environment variable as an integer.

        Args:
            key: Environment variable key
            default: Default value if key doesn't exist

        Returns:
            Integer value of environment variable
        """
        try:
            return int(self.get(key, default))
        except ValueError:
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        Get an environment variable as a float.

        Args:
            key: Environment variable key
            default: Default value if key doesn't exist

        Returns:
            Float value of environment variable
        """
        try:
            return float(self.get(key, default))
        except ValueError:
            return default


# Global environment manager instance
env_manager = EnvManager()


def get_env(key: str, default=None):
    """Get an environment variable using the global manager."""
    return env_manager.get(key, default)


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get an environment variable as a boolean using the global manager."""
    return env_manager.get_bool(key, default)


def get_env_int(key: str, default: int = 0) -> int:
    """Get an environment variable as an integer using the global manager."""
    return env_manager.get_int(key, default)


def get_env_float(key: str, default: float = 0.0) -> float:
    """Get an environment variable as a float using the global manager."""
    return env_manager.get_float(key, default)