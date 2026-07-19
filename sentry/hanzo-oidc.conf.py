# Hanzo IAM (hanzo.id) OIDC SSO — canonical settings for Hanzo Sentry.
#
# This is the SOURCE OF TRUTH for the SSO wiring. It is mirrored VERBATIM into
# the k8s ConfigMap `sentry-config` (universe/infra/k8s/sentry/config.yaml) so
# the deployed instance and this repo never drift. It is loaded by the OIDC
# exec hook that sentry/enhance-image.sh appends to /etc/sentry/sentry.conf.py:
#
#     _p = "/etc/sentry/hanzo-oidc.conf.py"
#     if __import__("os").path.exists(_p): exec(open(_p).read())
#
# Requires the `sentry-auth-oidc` plugin (added by sentry/enhance-image.sh).
# Secrets come from the environment, injected from the KMS-synced `sentry-oidc`
# secret (never hard-code — KMS-only, hashed at rest).

# --- Hanzo IAM as the SOLE identity provider ---------------------------------
# Standard OAuth2 **authorization-code** flow with a CONFIDENTIAL client
# (client_secret from KMS). Hanzo IAM (Casdoor-backed) is a standard OIDC
# provider; PKCE is NOT required and NOT enabled here — this is a server-side
# confidential client, not a public/native client. Do NOT turn on a PKCE
# requirement: the redirect exchange is authenticated by OIDC_CLIENT_SECRET.
# `env(...)` is defined by sentry.conf.py (self-hosted helper).
OIDC_CLIENT_ID = env("OIDC_CLIENT_ID") or "hanzo-sentry"      # <org>-<app> IAM app
OIDC_CLIENT_SECRET = env("OIDC_CLIENT_SECRET")                # from KMS: sentry-oidc/CLIENT_SECRET
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

# --- OIDC-only: IAM is the one and only way in -------------------------------
# sentry-auth-oidc registers "oidc" as the sole social-auth provider. With
# self-registration and ad-hoc org creation both OFF, the ONLY path to an
# account is through Hanzo IAM. `auth.allow-registration` is pinned off in the
# system config (config.yml) as well — belt and suspenders. At go-live, set the
# Hanzo org's Auth to "require SSO" (Settings -> Auth) to retire the residual
# username/password form for members. Bootstrap seeds ONE org, "Hanzo".
SENTRY_FEATURES["auth:register"] = False          # hide the self-serve signup form
SENTRY_FEATURES["organizations:create"] = False   # single Hanzo tenant; no ad-hoc orgs

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
