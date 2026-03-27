from django.http import HttpResponse
from rest_framework.request import Request

from sentry.auth.view import AuthView

from .client import HanzoClient


class FetchUser(AuthView):
    def dispatch(self, request: Request, helper) -> HttpResponse:
        access_token = helper.fetch_state("data")["access_token"]
        with HanzoClient(access_token) as client:
            user = client.get_user()

        helper.bind_state("user", user)
        return helper.next_step()
