from typing import Optional

class VideoGrant:
    def __init__(
        self,
        room_create: Optional[bool] = None,
        room_join: Optional[bool] = None,
        room_list: Optional[bool] = None,
        room_record: Optional[bool] = None,
        room_admin: Optional[bool] = None,
        room: Optional[str] = None,
        can_publish: Optional[bool] = None,
        can_subscribe: Optional[bool] = None,
        can_publish_data: Optional[bool] = None,
        hidden: Optional[bool] = None,
        recorder: Optional[bool] = None,
    ):

        self.room_create = room_create
        self.room_join = room_join
        self.room_list = room_list
        self.room_record = room_record
        self.room_admin = room_admin
        self.room = room
        self.can_publish = can_publish
        self.can_subscribe = can_subscribe
        self.can_publish_data = can_publish_data
        self.hidden = hidden
        self.recorder = recorder

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return cls()

        return cls(
            room_create=data.get("roomCreate"),
            room_join=data.get("roomJoin"),
            room_list=data.get("roomList"),
            room_record=data.get("roomRecord"),
            room_admin=data.get("roomAdmin"),
            room=data.get("room"),
            can_publish=data.get("canPublish"),
            can_subscribe=data.get("canSubscribe"),
            can_publish_data=data.get("canPublishData"),
            hidden=data.get("hidden"),
            recorder=data.get("recorder"),
        )

    def to_dict(self):
        return {
            "roomCreate": self.room_create,
            "roomJoin": self.room_join,
            "roomList": self.room_list,
            "roomRecord": self.room_record,
            "roomAdmin": self.room_admin,
            "room": self.room,
            "canPublish": self.can_publish,
            "canSubscribe": self.can_subscribe,
            "canPublishData": self.can_publish_data,
            "hidden": self.hidden,
            "recorder": self.recorder,
        }



class ClaimGrants:
    def __init__(
        self,
        name: Optional[str] = None,
        video: Optional[VideoGrant] = None,
        metadata: Optional[str] = None,
        sha256: Optional[str] = None,
    ):

        self.name = name
        self.video = video
        self.metadata = metadata
        self.sha256 = sha256

    @classmethod
    def from_jwt(cls, jwt):
        return cls(
            name=jwt.get("name"),
            video=VideoGrant.from_dict(jwt.get("video")) if "video" in jwt else None,
            metadata=jwt.get("metadata"),
            sha256=jwt.get("sha256"),
        )

    def to_dict(self):
        return {
            "name": self.name,
            "video": self.video.to_dict() if self.video else None,
            "metadata": self.metadata,
            "sha256": self.sha256
        }