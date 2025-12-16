"""
Configuration settings for the application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_PATH = os.getenv("DB_PATH", "ecommerce.db")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

# System prompt for the agent
SYSTEM_PROMPT = """You are an e-commerce data analyst assistant. 

When querying the transactions table:
- Filter out non-product entries like adjustments, bad debt, postage, fees, etc.
- Exclude rows where UnitPrice is negative or zero for product queries
- Focus on actual customer purchases
- Be aware that Description may contain adjustment entries - filter these appropriately

When asked about products, ensure you're excluding administrative and accounting entries."""


def validate_config():
    """Validate required configuration settings."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
        raise ValueError("Please set your OPENAI_API_KEY in the .env file")
    
    if not Path(DB_PATH).exists():
        raise FileNotFoundError(
            f"Database '{DB_PATH}' not found. "
            "Please run the notebook first to create the database."
        )
