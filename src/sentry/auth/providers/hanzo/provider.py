from collections.abc import Mapping
from typing import Any

from sentry.auth.exceptions import IdentityNotValid
from sentry.auth.providers.oauth2 import OAuth2Callback, OAuth2Login, OAuth2Provider

from .client import HanzoApiError, HanzoClient
from .constants import ACCESS_TOKEN_URL, AUTHORIZE_URL, CLIENT_ID, CLIENT_SECRET, SCOPE
from .views import FetchUser


class HanzoOAuth2Provider(OAuth2Provider):
    access_token_url = ACCESS_TOKEN_URL
    authorize_url = AUTHORIZE_URL
    name = "Hanzo"

    def get_client_id(self):
        return CLIENT_ID

    def get_client_secret(self):
        return CLIENT_SECRET

    def get_auth_pipeline(self):
        return [
            OAuth2Login(
                authorize_url=self.authorize_url,
                client_id=self.get_client_id(),
                scope=SCOPE,
            ),
            OAuth2Callback(
                access_token_url=self.access_token_url,
                client_id=self.get_client_id(),
                client_secret=self.get_client_secret(),
            ),
            FetchUser(),
        ]

    def get_setup_pipeline(self):
        return self.get_auth_pipeline()

    def get_refresh_token_url(self):
        return ACCESS_TOKEN_URL

    def build_config(self, state):
        return {}

    def build_identity(self, state: Mapping[str, Any]) -> Mapping[str, Any]:
        data = state["data"]
        user_data = state["user"]
        return {
            "id": user_data.get("sub") or user_data.get("id", ""),
            "email": user_data.get("email", ""),
            "name": user_data.get("name", user_data.get("displayName", "")),
            "data": self.get_oauth_data(data),
        }

    def refresh_identity(self, auth_identity):
        with HanzoClient(auth_identity.data["access_token"]) as client:
            try:
                client.get_user()
            except HanzoApiError as e:
                raise IdentityNotValid(e)
