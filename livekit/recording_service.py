from livekit.grants import VideoGrant

from typing import Optional


class RecordingServiceClient:
    def __init__(self, parent):
        self.parent = parent
        self.service = "RecordingService"

    def auth_header(self, grant: VideoGrant):
        token = self.parent.generate_access_token()
        token.add_grant(grant)
        return {
            "Authorization": f"Bearer {token.to_jwt()}"
        }

    def start_recording(self, url: str, filepath: str, options: dict):
        return self.parent._twirp_client.request(
            self.service,
            "StartRecording",
            {
                "url": url,
                "filepath": filepath,
                "options": options,
            },
            self.authHeader(VideoGrant(room_record=True)),
        )
    
    def add_output(self, recording_id: str, rtmp_url: str):
        return self.parent._twirp_client.request(
            self.service,
            "AddOutput",
            {
                "recordingId": recording_id,
                "rtmpUrl": rtmp_url,
            },
            self.authHeader(VideoGrant(room_record=True)),
        )

    def remove_output(self, recording_id: str, rtmp_url: str):
        return self.parent._twirp_client.request(
            self.service,
            "RemoveOutput",
            {
                "recordingId": recording_id,
                "rtmpUrl": rtmp_url,
            },
            self.authHeader(VideoGrant(room_record=True)),
        )

    def end_recording(self, recording_id: str):
        return self.parent._twirp_client.request(
            self.service,
            "AddOutput",
            {
                "recordingId": recording_id,
            },
            self.authHeader(VideoGrant(room_record=True)),
        )