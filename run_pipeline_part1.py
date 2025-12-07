import os
from src.config import Config
from src.services.x_service import XDataService
from src.agents.context_builder import ContextBuilderAgent

def main():
    print("=== Grok Ad Pipeline: Part 1 (Data & Context) ===")
    
    # 1. Validate Config
    Config.validate()
    
    # 2. Initialize Services
    x_service = XDataService()
    agent = ContextBuilderAgent()
    
    # 3. Get User Data (Using a dummy handle for demo if no secrets)
    target_handle = "snareyansh" 
    print(f"\nFetching data for @{target_handle}...")
    
    try:
        user_id = x_service.get_user_id(target_handle)
        likes = x_service.get_user_likes(user_id, limit=5)
        reposts = x_service.get_user_reposts(user_id, limit=5)
        
        print(f"Found {len(likes)} likes and {len(reposts)} reposts.")
        print("Sample Like:", likes[0] if likes else "None")
        
        # 4. Grok Analysis
        print("\nSending data to Grok Agent 1 (Context Builder)...")
        context_card = agent.build_context_card(likes, reposts)
        
        # 5. Output
        print("\n=== Generated Context Card ===")
        import json
        print(json.dumps(context_card, indent=2))
        
    except Exception as e:
        print(f"Pipeline Error: {e}")

if __name__ == "__main__":
    main()



