# Sentinel

Error tracking and performance monitoring for the Hanzo ecosystem.

**Upstream**: [getsentry/sentry](https://github.com/getsentry/sentry) under FSL-1.0-Apache-2.0 (Functional Source License, with Apache-2.0 as the Change License). LICENSE.md retained as-is from upstream.

**Repo**: `github.com/hanzoai/sentry`
**Branded as**: Sentinel / `sentry.hanzo.ai`

## Integration

- Auth: Hanzo IAM (hanzo.id) OIDC SSO
- Storage: PostgreSQL (`sql.hanzo.svc`) + ClickHouse (via hanzoai/datastore)
- Ingress: `sentry.hanzo.ai`
- Deployed via universe k8s manifests

## License notes

FSL-1.0-Apache-2.0 means the source is available now under FSL terms, and
auto-relicenses to Apache-2.0 after the change date defined in
upstream's LICENSE.md. Honor both upstream license file and the original
copyright headers.
