# Author: Peng Fei
# Configuration settings for job requirement generator

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))

# Output format template
OUTPUT_TEMPLATE = {
    "session_id": "",
    "requirements": {
        "title": "",
        "description": "",
        "must_have": {
            "technical_skills": [],
            "domain_experience": [],
            "soft_skills": []
        },
        "nice_to_have": []
    }
} 