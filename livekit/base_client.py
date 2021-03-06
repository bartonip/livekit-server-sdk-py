from datetime import timedelta

from livekit.grants import VideoGrant


class BaseClient:
    service = None
    def __init__(self, parent):
        self.parent = parent

    def auth_header(self, grant: VideoGrant):
        token = self.parent.generate_access_token(ttl=timedelta(minutes=2))
        token.add_grant(grant)
        return {
            "Authorization": f"Bearer {token.to_jwt()}"
        }
