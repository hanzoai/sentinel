#!/bin/bash
set -euo pipefail

# Hanzo Sentry — image enhancement, baked into ghcr.io/hanzoai/sentry at build
# time (sentry/Dockerfile runs this if present). See:
#   https://develop.sentry.dev/self-hosted/#enhance-sentry-image
#
# Adds Hanzo IAM (hanzo.id) OIDC single-sign-on via the community
# `sentry-auth-oidc` provider. The matching runtime settings live in
# sentry/hanzo-oidc.conf.py (mirrored into the k8s ConfigMap `sentry-config`).
#
# NOTE (go-live): pin `sentry-auth-oidc` to the release verified against the
# pinned Sentry version (currently 26.3.1) before shipping — leave unpinned only
# on this staging branch. CI must `python -c "import oidc"` as a smoke gate.
pip install sentry-auth-oidc
