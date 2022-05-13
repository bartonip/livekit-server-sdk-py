import jwt
from datetime import datetime, timedelta, timezone

from typing import Optional

from livekit.grants import VideoGrant, ClaimGrants
from livekit.utilities import clean_null_terms

class AccessToken:
    def __init__(
        self,
        parent,
        name: Optional[str] = None,
        identity: Optional[str] = None,
        ttl: Optional[timedelta] = timedelta(hours=1),
        metadata: Optional[str] = None,
    ):

        self.name = name
        self.identity = identity
        self.ttl = ttl
        self.metadata = metadata
        self.grants = ClaimGrants(name=name)

        self.parent = parent

    @property
    def sha256(self):
        return None

    @sha256.setter
    def sha256(self, value):
        self.grants.sha256 = value

    def add_grant(self, grant: VideoGrant):
        self.grants.video = grant

    def to_jwt(self) -> str:
        if (self.identity and self.grants.video and self.grants.video.room_join):
            raise Exception("Identity is required for join but not set")

        token_data = {
            "exp": datetime.utcnow() + self.ttl,
            "iss": self.parent.api_key,
            "nbf": datetime.utcnow() - timedelta(seconds=10),
            **self.grants.to_dict()
        }
        
        if self.identity:
            token_data["sub"] = self.identity
            token_data["kid"] = self.identity

        return jwt.encode(clean_null_terms(token_data), self.parent.api_secret).decode("utf-8")


class TokenVerifier:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def verify(self, token: str):
        decoded = jwt.decode(token, self.api_secret)

        return ClaimGrants.from_jwt(decoded)