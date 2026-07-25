import os

# IAM OIDC endpoints (hanzo.id). Canonical HIP-0111 paths — what hanzo.id's
# /.well-known/openid-configuration advertises. The bare /oauth/* forms were
# served only by the hanzo.id-worker shim; IAM itself 401s them.
AUTHORIZE_URL = os.environ.get(
    "SENTRY_OIDC_AUTHORIZE_URL", "https://hanzo.id/v1/iam/oauth/authorize"
)
ACCESS_TOKEN_URL = os.environ.get("SENTRY_OIDC_TOKEN_URL", "https://hanzo.id/v1/iam/oauth/token")
USERINFO_URL = os.environ.get(
    "SENTRY_OIDC_USERINFO_URL", "https://hanzo.id/v1/iam/oauth/userinfo"
)

CLIENT_ID = os.environ.get("SENTRY_OIDC_CLIENT_ID", "app-sentry")
CLIENT_SECRET = os.environ.get("SENTRY_OIDC_CLIENT_SECRET", "")

SCOPE = "openid profile email"
