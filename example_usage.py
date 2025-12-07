"""Example usage of the Grok Ad Generation Pipeline"""
import os
from dotenv import load_dotenv
from src.models import CampaignInput
from src.pipeline import AdPipeline

load_dotenv()


def main():
    """Example: Generate an ad for a target user"""
    
    # Check API key
    if not os.getenv("XAI_API_KEY"):
        print("Error: XAI_API_KEY environment variable is not set")
        print("Please set it in your .env file or environment")
        return
    
    # Create campaign input
    campaign_input = CampaignInput(
        base_ad_creative="Introducing our revolutionary new AI-powered product that will change how you work!",
        brand_persona_json={
            "tone": "innovative and friendly",
            "values": ["innovation", "user-centric", "transparency"],
            "target_audience": "tech-savvy professionals",
            "brand_voice": "confident but approachable"
        },
        policy_rules=[
            "No offensive or controversial content",
            "Respect user privacy",
            "Be authentic and transparent",
            "Avoid misleading claims"
        ]
    )
    
    # Initialize pipeline
    print("Initializing pipeline...")
    pipeline = AdPipeline()
    
    # Run pipeline for a target user
    username = "elonmusk"  # Example: target this user's interests
    print(f"\nRunning pipeline for @{username}...")
    print("=" * 60)
    
    try:
        result = pipeline.run(
            username=username,
            campaign_input=campaign_input,
            user_id=f"user_{username}",
            cohort_id="tech_enthusiasts"
        )
        
        print("\n" + "=" * 60)
        print("Pipeline completed successfully!")
        print("=" * 60)
        print(f"\nSelected Variant ID: {result.metrics.variant_id}")
        print(f"\nAd Copy:\n{result.variant.copy}")
        
        if result.variant.image_overlay_suggestions:
            print(f"\nImage Overlay Suggestions:")
            for suggestion in result.variant.image_overlay_suggestions:
                print(f"  - {suggestion}")
        
        print(f"\nMetrics:")
        print(f"  CTR Prediction: {result.metrics.ctr_prediction:.3f}")
        print(f"  Native Feel Score: {result.metrics.native_feel_score:.3f}")
        print(f"  Brand Safety: {'✓ Pass' if result.metrics.brand_safety_check else '✗ Fail'}")
        
        print(f"\nDelivery Metadata:")
        print(f"  Topics: {', '.join(result.delivery_metadata.get('context_topics', []))}")
        print(f"  Tone: {result.delivery_metadata.get('tone', 'N/A')}")
        
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

