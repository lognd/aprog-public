"""Single source of truth for version constants shared across generation and manifests."""

from __future__ import annotations

#: Bumped whenever the generated-config output format changes, so stale
#: generated files can be detected via source-hash comparison.
GENERATOR_VERSION = "0.1"

#: Bumped whenever the manifest/verification-config JSON schema changes.
SCHEMA_VERSION = "0.1"
