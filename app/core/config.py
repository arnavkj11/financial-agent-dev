import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Financial Advisor Agent"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # We will add OpenAI and Database config here later
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-this-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
