import pytest

from livekit import LiveKit

@pytest.fixture
def client():
    return LiveKit(api_key="abcd", api_secret="efgh")