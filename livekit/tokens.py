import jwt
from datetime import datetime, timedelta

from typing import Optional

from .grants import VideoGrant, ClaimGrants

class AccessToken:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        name: str,
        identity: Optional[str] = None,
        ttl: Optional[timedelta] = timedelta(hours=1),
        metadata: Optional[str] = None,
    ):

        self.name = name
        self.identity = identity
        self.ttl = ttl
        self.metadata = metadata
        self.grants = ClaimGrants(name=name)

        self.api_key = api_key
        self.api_secret = api_secret

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
            "exp": datetime.now() + self.ttl,
            "iss": self.api_key,
            "nbf": datetime.now(),
            **self.grants.to_dict()
        }
        
        if self.identity:
            token_data["sub"] = self.identity
            token_data["kid"] = self.identity

        return jwt.encode(token_data, self.api_secret).decode("utf-8")


class TokenVerifier:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def verify(self, token: str):
        decoded = jwt.decode(token, self.api_secret)

        return ClaimGrants.from_jwt(decoded)