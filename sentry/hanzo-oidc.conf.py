# Hanzo IAM (hanzo.id) OIDC SSO — canonical settings for Hanzo Sentry.
#
# This is the SOURCE OF TRUTH for the SSO wiring. It is mirrored verbatim into
# the k8s ConfigMap `sentry-config` (universe/infra/k8s/sentry) so the deployed
# instance and this repo never drift. Append to / import from sentry.conf.py:
#
#     with open("/etc/sentry/hanzo-oidc.conf.py") as _f:
#         exec(_f.read())
#
# Requires the `sentry-auth-oidc` plugin (added by sentry/enhance-image.sh).
# Secrets come from the environment, injected from the KMS-synced `sentry-oidc`
# secret (never hard-code — KMS-only, hashed at rest).

# --- IAM as the identity provider --------------------------------------------
# `env(...)` is defined by sentry.conf.py (self-hosted helper).
OIDC_CLIENT_ID = env("OIDC_CLIENT_ID") or "hanzo-sentry"     # <org>-<app> IAM app
OIDC_CLIENT_SECRET = env("OIDC_CLIENT_SECRET")               # from KMS: sentry-oidc/CLIENT_SECRET
OIDC_SCOPE = env("OIDC_SCOPE") or "openid email profile"

# Discovery: the plugin fetches <OIDC_DOMAIN>/.well-known/openid-configuration.
# Confirm the exact authorize/token/userinfo endpoints from that document at
# go-live — hanzo.id is Casdoor-backed (endpoints below are the Casdoor
# convention; jwks_uri is confirmed live at hanzo.id/.well-known/jwks).
OIDC_DOMAIN = env("OIDC_DOMAIN") or "https://hanzo.id"
OIDC_ISSUER = env("OIDC_ISSUER") or "Hanzo IAM"

# Explicit endpoints — used only if a plugin build cannot auto-discover.
# OIDC_AUTHORIZATION_ENDPOINT = "https://hanzo.id/login/oauth/authorize"
# OIDC_TOKEN_ENDPOINT         = "https://hanzo.id/api/login/oauth/access_token"
# OIDC_USERINFO_ENDPOINT      = "https://hanzo.id/api/userinfo"
# OIDC_JWKS_URI               = "https://hanzo.id/.well-known/jwks"

# --- Behind Traefik TLS (X-Forwarded-* set by ingress) -----------------------
# Mirrors the Insights Django pattern: the ingress forwards the public host so
# Sentry builds correct https:// OIDC redirect_uris.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# --- Multi-tenant note -------------------------------------------------------
# Sentry SSO is configured PER-ORGANIZATION (Settings -> Auth -> link provider).
# "org == JWT `owner`" is NOT native to Sentry. Two supported shapes at go-live:
#   1. Single Hanzo org, IAM as the sole IdP, auto-link members by verified
#      email domain (simplest; one Sentry org == the Hanzo tenant boundary).
#   2. Per-Hanzo-org Sentry organizations, each linked to the same IAM app,
#      brokered by api.hanzo.ai stamping org=owner (see go-live plan Phase 4).
