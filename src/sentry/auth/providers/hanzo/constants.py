import os

# IAM OIDC endpoints (hanzo.id)
AUTHORIZE_URL = os.environ.get("SENTRY_OIDC_AUTHORIZE_URL", "https://hanzo.id/oauth/authorize")
ACCESS_TOKEN_URL = os.environ.get("SENTRY_OIDC_TOKEN_URL", "https://hanzo.id/oauth/token")
USERINFO_URL = os.environ.get("SENTRY_OIDC_USERINFO_URL", "https://hanzo.id/oauth/userinfo")

CLIENT_ID = os.environ.get("SENTRY_OIDC_CLIENT_ID", "app-sentry")
CLIENT_SECRET = os.environ.get("SENTRY_OIDC_CLIENT_SECRET", "")

SCOPE = "openid profile email"
