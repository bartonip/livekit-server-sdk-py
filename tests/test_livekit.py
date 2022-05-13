import pytest

import jwt
import json

from datetime import timedelta

from livekit.tokens import AccessToken, TokenVerifier
from livekit.grants import VideoGrant, ClaimGrants

def test_livekit_generate_access_token(client):
    result = client.generate_access_token(
        name="John",
        identity="big-johnny-and-the-watermelons"
    )

    assert isinstance(result, AccessToken)
    assert result.name == "John"
    assert result.identity == "big-johnny-and-the-watermelons"
    assert result.ttl == timedelta(hours=1)
    assert result.metadata is None


    result.add_grant(VideoGrant(room="myroom"))
    assert result.grants.video.room == "myroom"

    token = result.to_jwt()
    assert isinstance(token, str)

    decoded = jwt.decode(token, client.api_secret)
    assert decoded["name"] == "John"

    assert decoded["video"]
    assert decoded["video"]["room"] == "myroom"


def test_access_token_identity_required_for_only_join_grants(client):
    result = client.generate_access_token(
        name="John",
        identity="big-johnny-and-the-watermelons"
    )

    result.add_grant(VideoGrant(room_create=True))

    assert result.to_jwt()

    result = client.generate_access_token(
        name="John",
        identity="big-johnny-and-the-watermelons"
    )

    result.add_grant(VideoGrant(room_join=True))
    
    with pytest.raises(Exception) as e:
        result.to_jwt()
        assert str(e) == "Identity is required for join but not set"

    
def test_access_token_valid(client):
    result = client.generate_access_token(
        name="John",
        identity="big-johnny-and-the-watermelons"
    )

    result.sha256 = "abcdefg"
    result.add_grant(VideoGrant(room_create=True))

    v = TokenVerifier(api_key="abcd", api_secret="efgh")
    decoded = v.verify(result.to_jwt())

    assert decoded is not None
    assert decoded.sha256 == "abcdefg"
    assert decoded.video.room_create