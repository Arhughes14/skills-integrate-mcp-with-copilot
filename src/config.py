"""
Configuration management for the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "mergington_high_school")

# Server Configuration
DEBUG = os.getenv("DEBUG", "False") == "True"

# Collection Names
ACTIVITIES_COLLECTION = "activities"
PARTICIPANTS_COLLECTION = "participants"
