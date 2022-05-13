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
            room_create=data.get("room_create"),
            room_join=data.get("room_join"),
            room_list=data.get("room_list"),
            room_record=data.get("room_record"),
            room_admin=data.get("room_admin"),
            room=data.get("room"),
            can_publish=data.get("can_publish"),
            can_subscribe=data.get("can_subscribe"),
            can_publish_data=data.get("can_publish_data"),
            hidden=data.get("hidden"),
            recorder=data.get("recorder"),
        )

    def to_dict(self):
        return {
            "room_create": self.room_create,
            "room_join": self.room_join,
            "room_list": self.room_list,
            "room_record": self.room_record,
            "room_admin": self.room_admin,
            "room": self.room,
            "can_publish": self.can_publish,
            "can_subscribe": self.can_subscribe,
            "can_publish_data": self.can_publish_data,
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