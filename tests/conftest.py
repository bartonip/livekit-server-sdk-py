import pytest

from livekit import LiveKit

@pytest.fixture
def client():
    return LiveKit(
        host="wss://test.gg",
        api_key="abcd", 
        api_secret="efgh"
    )