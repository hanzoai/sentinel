<p align="center"><img src=".github/hero.svg" alt="Sentinel" width="880"></p>

# Sentinel

Error tracking and performance monitoring for the Hanzo cloud. Sentinel receives
events from your applications, groups them into issues, and tells you which ones
are new, regressed, or getting worse.

Sentinel speaks the **Sentry wire protocol**, so the existing ecosystem of client
SDKs reports to it unchanged — a DSN pointing at your Sentinel instance is the
only configuration difference. There is no Sentinel-specific SDK to adopt, and
none is planned; the protocol is the interface.

## Running it

The deployed image is `ghcr.io/hanzoai/sentry`. Deployment is declared in the
`universe` repository and reconciled by Hanzo CD, like every other service.

## Attribution and licensing

Sentinel is a fork of [Sentry](https://github.com/getsentry/sentry) by Functional
Software, Inc., used under the **Functional Source License, Version 1.0, Apache
2.0 Change License** (`FSL-1.0-Apache-2.0`). See [`LICENSE`](LICENSE) for the
terms and [`NOTICE`](NOTICE) for attribution; both are required and are kept
current.

The FSL grants no trademark rights. "Sentry" is a trademark of Functional
Software, Inc., and this project is neither affiliated with nor endorsed by them.
Upstream marks are not used as branding here — where the name appears in this
codebase it refers to the module namespace (`src/sentry/`), the wire protocol, or
upstream attribution, none of which are brand usage.
