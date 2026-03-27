from django.apps import AppConfig


class Config(AppConfig):
    name = "sentry.auth.providers.hanzo"

    def ready(self):
        from sentry.auth import register

        from .provider import HanzoOAuth2Provider

        register("hanzo", HanzoOAuth2Provider)
