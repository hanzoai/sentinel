from sentry.http import safe_urlopen, safe_urlread
from sentry.utils import json

from .constants import USERINFO_URL


class HanzoApiError(Exception):
    def __init__(self, message="", status=0):
        self.status = status
        super().__init__(message)


class HanzoClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _request(self, url):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        req = safe_urlopen(url, headers=headers)
        body = safe_urlread(req)
        if req.status_code != 200:
            raise HanzoApiError(f"Request failed: {body}", status=req.status_code)
        return json.loads(body)

    def get_user(self):
        return self._request(USERINFO_URL)
