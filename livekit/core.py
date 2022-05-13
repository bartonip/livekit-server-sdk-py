from .tokens import AccessToken

class LiveKit:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def generate_access_token(self, name, identity):
        return AccessToken(api_key=self.api_key, api_secret=self.api_secret, name=name, identity=identity)
