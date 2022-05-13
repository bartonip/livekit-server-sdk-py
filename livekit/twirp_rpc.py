import requests
import json

from typing import Optional


class TwirpRpcClient:
    def __init__(self, parent):
        self.parent = parent

    def request(
        self,
        service: str,
        method: str,
        data: any,
        headers: Optional[any] = None,
    ):

        url = f"{self.parent.host}{self.parent.twirp_prefix}/{self.parent.package}.{service}/{method}"

        result = requests.post(
            url,
            data=json.dumps(data),
            headers={**headers, "Content-Type": "application/json"},
        )

        try:
            return result.json()
        except Exception:
            return result
