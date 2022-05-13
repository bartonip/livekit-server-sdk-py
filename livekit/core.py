import jwt

from .tokens import AccessToken
from .room_service import RoomServiceClient
from .grants import ClaimGrants
from .twirp_rpc import TwirpRpcClient

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

        self.room_service = RoomServiceClient(self)
        self._twirp_client = TwirpRpcClient(self)

    def generate_access_token(self, name: str = None, identity: str = None):
        return AccessToken(parent=self, name=name, identity=identity)

    def verify(self, token: str):
        decoded = jwt.decode(token, self.api_secret)

        return ClaimGrants.from_jwt(decoded)