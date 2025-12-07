import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # X Data API
    X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
    
    # Grok API
    XAI_API_KEY = os.getenv("XAI_API_KEY")
    
    # X Ads API (Boilerplate credentials)
    X_ADS_API_KEY = os.getenv("X_ADS_API_KEY")
    X_ADS_API_SECRET = os.getenv("X_ADS_API_SECRET")
    X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
    X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.XAI_API_KEY:
            missing.append("XAI_API_KEY")
        # For part 1 demo, we might only need XAI_API_KEY if we mock X data
        # But ideally we check all relevant ones
        if missing:
            print(f"Warning: Missing environment variables: {', '.join(missing)}")



