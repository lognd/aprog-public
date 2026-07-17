# Tickets

Central ledger managed by `frob ticket` -- one section per ticket.

<!-- ticket:T-0001 -->
```yaml
id: T-0001
title: Fix docs index root mismatch causing DOC001 orphan-doc suppression
state: queued
kind: docs
origin: human
created: '2026-07-17'
blocked_by: []
parent: null
scope:
- docs/README.md
evidence: []
attachments: []
```
frob.toml sets [gates.docs] include = [] to fully disable DOC001 because DOC001's root-reachability walk only recognizes docs/index.md + top-level README.md as roots. This repo's real docs index is docs/README.md, which links only ~17 of the ~93 files under docs/. Real orphans: the entire docs/study-guides/ curriculum (62 guides + README), docs/course-arc.md, docs/curriculum-map.md, docs/readme-style.md, and 9 docs/tools/aprog-*.md command pages. Fix: either link these from docs/README.md (or a new docs/index.md), or restructure study-guides/tools into their own linked indices, then flip [gates.docs] include back to the default.

<!-- ticket:T-0002 -->
```yaml
id: T-0002
title: Add unit tests to close TEST001/TEST002 warnings on src/aprog CLI surface
state: queued
kind: feature
origin: human
created: '2026-07-17'
blocked_by: []
parent: null
scope:
- src/aprog/**,tests/unit/**
evidence: []
attachments: []
```
frob check --only gates reports 1081 TEST001 (no frob:tests unit edge) + related TEST002 warnings, mostly on src/aprog/commands, src/aprog/models, src/aprog/utils public symbols. These are currently warn-severity legacy debt (see [gates.severity] in frob.toml). Pick a slice of commands/models per ticket and bind frob:tests directives to existing/new unit tests until TEST001/TEST002 can be flipped back to error for that slice.

<!-- ticket:T-0003 -->
```yaml
id: T-0003
title: Bind integration tests for src/aprog/utils and src/aprog/paths.py interfaces
state: queued
kind: feature
origin: human
created: '2026-07-17'
blocked_by: []
parent: null
scope:
- src/aprog/utils/**,src/aprog/paths.py,tests/integration/**
evidence: []
attachments: []
```
TEST003 flags src/aprog/utils and src/aprog/paths.py as interfaces (public symbols imported cross-package) with 0/1 integration edges. Add frob:tests ... kind="integration" edges bound to real tests/integration/ coverage for these two.
