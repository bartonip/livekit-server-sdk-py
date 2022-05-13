import requests

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

        url = f"{self.parent.host}/{self.parent.package}.{service}/{method}"

        return requests.post(
            url,
            data=data,
            headers=headers,
        )
