from livekit.grants import VideoGrant

from typing import Optional


class EgressClient:
    def __init__(self, parent):
         self.parent = parent
