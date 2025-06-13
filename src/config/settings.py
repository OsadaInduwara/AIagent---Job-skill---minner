# config/settings.py - Simplified Configuration

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Simple configuration for JobSkills AI"""

    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # App Settings
    MAX_JOBS_PER_SEARCH = int(os.getenv("MAX_JOBS_PER_SEARCH", "10"))
    SCRAPING_DELAY = int(os.getenv("SCRAPING_DELAY", "2"))

    # Data Settings
    DATA_DIR = "data"

    @staticmethod
    def validate_config():
        """Validate configuration"""
        if not Config.OPENAI_API_KEY:
            return False, "OpenAI API key is required"

        return True, "Configuration is valid"