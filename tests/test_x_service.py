import pytest
from unittest.mock import patch, MagicMock
from src.services.x_service import XDataService
from src.config import Config

@pytest.fixture
def x_service():
    return XDataService()

def test_get_user_id_mock(x_service):
    # Mocking Config to ensure no real API call is attempted if we don't want it, 
    # but the service checks Config.X_BEARER_TOKEN. 
    # If token is missing, it returns a mock ID.
    with patch.object(Config, 'X_BEARER_TOKEN', None):
        user_id = x_service.get_user_id("testuser")
        assert user_id == "123456789"

def test_get_user_likes_mock(x_service):
    with patch.object(Config, 'X_BEARER_TOKEN', None):
        likes = x_service.get_user_likes("123", limit=2)
        assert len(likes) == 2
        assert "Mock liked tweet" in likes[0]

@patch('requests.get')
def test_get_user_likes_api(mock_get, x_service):
    # Simulate API call with token
    with patch.object(Config, 'X_BEARER_TOKEN', "fake_token"):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "1", "text": "Tweet 1"},
                {"id": "2", "text": "Tweet 2"}
            ]
        }
        mock_get.return_value = mock_response

        likes = x_service.get_user_likes("123", limit=2)
        assert len(likes) == 2
        assert likes[0] == "Tweet 1"
        mock_get.assert_called_once()



