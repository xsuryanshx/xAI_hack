import requests
from src.config import Config

class XDataService:
    def __init__(self):
        self.base_url = "https://api.x.com/2"
        self.headers = {
            "Authorization": f"Bearer {Config.X_BEARER_TOKEN}",
            "Content-Type": "application/json"
        }

    def get_user_id(self, username: str) -> str:
        """Resolve username to user ID."""
        if not Config.X_BEARER_TOKEN:
             # Fallback for demo/testing without real token
            print(f"Mocking User ID resolution for {username}")
            return "123456789"
            
        url = f"{self.base_url}/users/by/username/{username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"X API Error: {response.text}")
        return response.json()["data"]["id"]

    def get_user_likes(self, user_id: str, limit: int = 5) -> list:
        """Fetch recent likes for a user."""
        if not Config.X_BEARER_TOKEN:
            return ["Mock liked tweet 1: I love AI technology!", "Mock liked tweet 2: Python is great for backend."]

        url = f"{self.base_url}/users/{user_id}/liked_tweets"
        params = {"max_results": limit, "tweet.fields": "created_at,text"}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching likes: {response.text}")
            return []
            
        data = response.json().get("data", [])
        return [tweet["text"] for tweet in data]

    def get_user_reposts(self, user_id: str, limit: int = 5) -> list:
        """Fetch recent reposts (Retweets) from user timeline."""
        if not Config.X_BEARER_TOKEN:
            return ["Mock repost 1: Breaking news in Tech.", "Mock repost 2: Meme about coding."]

        url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            "max_results": limit * 2, # Fetch more to filter
            "exclude": "replies"
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching tweets: {response.text}")
            return []
            
        data = response.json().get("data", [])
        # Filter for RTs (starts with RT @) - simple heuristic or use referenced_tweets field if expanded
        reposts = [t["text"] for t in data if t["text"].startswith("RT @")]
        return reposts[:limit]



