#!/bin/bash
set -euo pipefail

# Hanzo Sentry — image enhancement, baked into ghcr.io/hanzoai/sentry at build
# time (sentry/Dockerfile runs this if present). See:
#   https://develop.sentry.dev/self-hosted/#enhance-sentry-image
#
# The build context is ./sentry (see hanzo.yml), copied to /usr/src/sentry.
SRC=/usr/src/sentry

# 1. Hanzo IAM (hanzo.id) OIDC single-sign-on via the community
#    `sentry-auth-oidc` provider. Runtime settings live in
#    sentry/hanzo-oidc.conf.py (mirrored verbatim into the k8s ConfigMap
#    `sentry-config`).
#
# NOTE (go-live): pin `sentry-auth-oidc` to the release verified against the
# pinned Sentry version (currently 26.3.1) before shipping — leave unpinned only
# on this staging branch. CI must `python -c "import oidc"` as a smoke gate.
pip install sentry-auth-oidc

# 2. Bake the self-hosted Django config into the image and wire the OIDC loader.
#    sentry/sentry.conf.example.py IS the intended /etc/sentry/sentry.conf.py
#    (docker-compose mounts it via install.sh; a k8s image bakes it here). The
#    appended hook exec's /etc/sentry/hanzo-oidc.conf.py at settings import —
#    that file is provided at runtime by the `sentry-config` ConfigMap (subPath),
#    and also baked below as a self-contained fallback. Both are byte-identical
#    to sentry/hanzo-oidc.conf.py, so the image and the cluster never drift.
install -D -m 0644 "$SRC/sentry.conf.example.py" /etc/sentry/sentry.conf.py
install -D -m 0644 "$SRC/hanzo-oidc.conf.py"     /etc/sentry/hanzo-oidc.conf.py
cat >> /etc/sentry/sentry.conf.py <<'PY'

# --- Hanzo IAM OIDC SSO overlay (appended by sentry/enhance-image.sh) --------
_p = "/etc/sentry/hanzo-oidc.conf.py"
if __import__("os").path.exists(_p):
    exec(open(_p).read())
PY

# 3. Smoke gates: the plugin must import and the baked config must compile.
python -c "import oidc"
python -c "compile(open('/etc/sentry/sentry.conf.py').read(), 'sentry.conf.py', 'exec')"
