import pytest
from src.config import Config

def test_config_validation():
    # Should not raise error, but might print warning if vars missing
    Config.validate()

def test_xai_sdk_client_init():
    # If XAI_API_KEY is not set, this might fail or just initialize without auth check until call
    # We'll mock the env var for this test to ensure it passes basic init
    import os
    if not os.getenv("XAI_API_KEY"):
        os.environ["XAI_API_KEY"] = "dummy_key"
    
    try:
        from xai_sdk import Client
        client = Client()
        assert client is not None
    except ImportError:
        pytest.skip("xai_sdk not installed")
    except Exception as e:
        pytest.fail(f"Client initialization failed: {e}")

