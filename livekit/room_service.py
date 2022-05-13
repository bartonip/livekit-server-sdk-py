import json
from datetime import timedelta
from typing import Optional, List

from livekit.grants import VideoGrant

class RoomServiceClient:
    def __init__(self, parent):
        self.parent = parent
        self.service = "RoomService"

    def auth_header(self, grant: VideoGrant):
        token = self.parent.generate_access_token()
        token.add_grant(grant)
        return {
            "Authorization": f"Bearer {token.to_jwt()}"
        }

    def create_room(self, name: str, empty_timeout: timedelta = timedelta(minutes=30), max_participants: int = 20, node_id: Optional[str] = None, metadata: Optional[str] = None):
        return self.parent._twirp_client.request(
            self.service,
            "CreateRoom",
            {
                "name": name,
                "emptyTimeout": empty_timeout.total_seconds(),
                "maxParticipants": max_participants,
                "nodeId": node_id,
                "metadata": metadata, 
            },
            self.auth_header(VideoGrant(room_create=True)),
        )


    def list_rooms(self, names=[]):
        return self.parent._twirp_client.request(
            self.service,
            "ListRooms",
            {"names": names},
            self.auth_header(VideoGrant(room_list=True)),
        )

    def delete_room(self, room: str):
        return self.parent._twirp_client.request(
            self.service,
            "DeleteRoom",
            {"room": room},
            self.auth_header(VideoGrant(room_create=True)),

        )

    def update_room_metadata(self, room: str, metadata: str):
        return self.parent._twirp_client.request(
            self.service,
            "UpdateRoomMetadata",
            {"room": room, "metadata": metadata},
            self.auth_header(VideoGrant(room_admin=True, room=room)),

        )

    def list_participants(self, room: str):
        return self.parent._twirp_client.request(
            self.service,
            "ListParticipants",
            {"room": room},
            self.auth_header(VideoGrant(room_admin=True, room=room)),

        )

    def get_participant(self, room: str, identity: str):
        return self.parent._twirp_client.request(
            self.service,
            "GetParticipant",
            {"room": room, "identity": identity},
            self.auth_header(VideoGrant(room_admin=True, room=room)),

        )

    def remove_participant(self, room: str, identity: str):
        return self.parent._twirp_client.request(
            self.service,
            "RemoveParticipant",
            {"room": room, "identity": identity},
            self.auth_header(VideoGrant(room_admin=True, room=room)),

        )

    def mute_published_track(self, room: str, identity: str, track_sid: str, muted: bool):
        return self.parent._twirp_client.request(
            self.service,
            "MutePublishedTrack",
            {"room": room, "identity": identity, "trackSid": track_sid, "muted": muted},
            self.auth_header(VideoGrant(room_admin=True, room=room)),
        )

    def update_participant(
        self, 
        room: str, 
        identity: str, 
        metadata: Optional[str] = None, 
        can_subscribe: bool = False, 
        can_publish: bool = False,
        can_publish_data: bool = False,
        hidden: bool = False,
        recorder: bool = False ):
        return self.parent._twirp_client.request(
            self.service,
            "UpdateParticipant",
            {
                "room": room, 
                "identity": identity, 
                "metadata": metadata, 
                "permission": {
                    "canSubscribe": can_subscribe,
                    "canPublish": can_publish,
                    "canPublishData": can_publish_data,
                    "hidden": hidden,
                    "recorder": recorder
                }
            },
            self.auth_header(VideoGrant(room_admin=True, room=room)),

        )

    def update_subscriptions(self, room: str, identity: str, track_sids: List[str], subscribe: bool):
        return self.parent._twirp_client.request(
            self.service,
            "UpdateSubscriptions",
            {"room": room, "identity": identity, "trackSids": track_sids, "subscribe": subscribe},
            self.auth_header(VideoGrant(room_admin=True, room=room)),

        )

    def send_data(self, room: str, data: bytes, kind: str, destinationSids: List[str]):
        return self.parent._twirp_client.request(
            self.service,
            "SendData",
            {"room": room, "data": base64.b64encode(bytes).decode("utf-8"), "kind": kind, "destinationSids": destinationSids},
            self.auth_header(VideoGrant(room_admin=True, room=room)),
        )