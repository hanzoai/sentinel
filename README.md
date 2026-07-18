<p align="center"><img src=".github/hero.svg" alt="Hanzo Sentry" width="880"></p>

# Hanzo Sentry

Error, performance, and uptime tracking for the Hanzo cloud — a Hanzo-branded
distribution of [Sentry](https://sentry.io/) self-hosted (v26.3.1), wired to
**Hanzo IAM** (`hanzo.id`) OIDC single-sign-on and deployed on the shared
`hanzo-k8s` cluster at **sentry.hanzo.ai**.

This repo is an *orchestration* fork: it pins upstream Sentry component images
(`sentry`, `snuba`, `relay`, `symbolicator`, `taskbroker`, `vroom`,
`uptime-checker`) and layers Hanzo integration on top. It is **not** vanilla
Sentry and must never run as such.

## Hanzo integration

| Concern | Where |
|---------|-------|
| IAM SSO (hanzo.id OIDC) | `sentry/enhance-image.sh` (adds `sentry-auth-oidc`) + `sentry/hanzo-oidc.conf.py` |
| Image | `ghcr.io/hanzoai/sentry` (built by CI from `sentry/Dockerfile`; see `hanzo.yml`) |
| K8s deploy | `universe/infra/k8s/sentry/` (mirrors `.../insights/`) |
| Secrets | KMS `kms.hanzo.ai`, project `hanzo-sentry` (KMS-only, never in git) |
| Routing | Traefik file-route in `universe .../ingress/routes.yaml` → `sentry.hanzo.ai` |

## Local / self-hosted (upstream flow)

The upstream `docker-compose.yml` + `./install.sh` path still works for local
proofs-of-concept. Docs: <https://develop.sentry.dev/self-hosted/>.

Upstream project and license terms are retained; see `LICENSE.md`.
