import base64
import hashlib
import json
import jwt


from typing import Optional

from livekit.tokens import AccessToken
from livekit.room_service import RoomServiceClient
from livekit.recording_service import RecordingServiceClient
from livekit.egress import EgressClient
from livekit.grants import ClaimGrants
from livekit.twirp_rpc import TwirpRpcClient

class LiveKit:
    def __init__(
        self, 
        api_key: str, 
        api_secret: str,
        host: str,
        package: str = "livekit",
        twirp_prefix: str = "/twirp"
    ):
        self.api_key = api_key
        self.api_secret = api_secret

        self.host = host
        self.package = package
        self.twirp_prefix = twirp_prefix

        self._twirp_client = TwirpRpcClient(self)
        self.room_service = RoomServiceClient(self)
        self.recording_service = RecordingServiceClient(self)
        self.egress_client = EgressClient(self)

    def generate_access_token(self, name: str = None, identity: str = None):
        return AccessToken(parent=self, name=name, identity=identity)

    def verify(self, token: str):
        decoded = jwt.decode(token, self.api_secret)

        return ClaimGrants.from_jwt(decoded)

    def receive(self, body: str, auth_header: Optional[str], skip_auth: bool = False):
        if skip_auth is False and not auth_header:
            raise Exception("Authorization header is empty")

        claims = self.verify(auth_header)
        checksum = hashlib.sha256(body.encode()).digest()

        assert claims.sha256 == base64.b64encode(checksum).decode("utf-8"), "sha256 checksum of body does not match"

        return json.loads(body)
