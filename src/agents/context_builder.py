import json
from src.config import Config

try:
    from xai_sdk import Client
    from xai_sdk.chat import user, system
except ImportError:
    print("Warning: xai_sdk not found. Using MockClient.")
    Client = None

class ContextBuilderAgent:
    def __init__(self):
        if Client:
            self.client = Client(api_key=Config.XAI_API_KEY)
        else:
            self.client = None
        
    def build_context_card(self, likes: list, reposts: list) -> dict:
        """
        Analyze user data to build a Context Card using Grok.
        """
        if not self.client:
            return {
                "topics": ["Mock Topic 1", "Mock Topic 2"],
                "tone": "Mock Tone",
                "risks": "None (Mock)"
            }

        prompt = f"""
        You are an expert marketing strategist. Analyze the following user interaction data from X (Twitter).
        
        USER LIKES:
        {json.dumps(likes, indent=2)}
        
        USER REPOSTS:
        {json.dumps(reposts, indent=2)}
        
        Based on this, extract the following in JSON format:
        1. "topics": List of top 3 interests/topics.
        2. "tone": The general tone of content they engage with (e.g., "Humorous", "Professional", "Sarcastic").
        3. "risks": Any potential brand safety risks or sensitive topics detected (or "None").
        
        Return ONLY the valid JSON object.
        """
        
        try:
            chat = self.client.chat.create(model="grok-4-1-fast")
            chat.append(system("You are a JSON-only output assistant."))
            chat.append(user(prompt))
            
            response = chat.sample()
            
            # Clean response to ensure just JSON
            content = response.content.strip()
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing Grok response: {e}")
            if 'response' in locals():
                print(f"Raw response: {response.content}")
            return {"error": "Failed to parse context"}

