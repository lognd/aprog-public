# Open Questions

All previously open questions are resolved. This file records the decisions made and why, so they can be revisited if assumptions change.

---

## Classification

**Should course/module be required?**
Decision: **Optional.** Not all assignments belong to a course. Requiring it creates friction for general-purpose or reusable assignments.

**Who can add new classification values?**
Decision: **Maintainers only**, via direct commits to `aprog.toml`. Contributors may request new values via a PR or issue. The validator rejects unknown values — this prevents accidental label sprawl.

---

## Templates

**Which templates are needed for MVP?**
Decision: `python-function`, `python-stdin-stdout`, `cpp-cmake`, `cpp-stdin-stdout`. These cover the most common assignment shapes. Other templates in the catalog are planned but not required for MVP.

**Should templates be versioned independently?**
Decision: **Yes.** Each template has its own `version` field in `template.toml`. Assignment `assignment.toml` records `[template] version` to lock the template version used. Template version bumps may require re-running `aprog new` or manual migration; migrations are not automated.

**Should templates be allowed to migrate assignments?**
Decision: **No for MVP.** If a template changes significantly, contributors update the assignment manually. Automated migration is out of scope.

---

## Generated configs

**Should generated public configs be committed?**
Decision: **Yes.** Generated files under `generated/` are committed to `aprog-public`. This makes them reviewable in PRs and keeps the repository self-contained. CI runs `aprog check-generated --all` and fails (exit 4 from `aprog validate`) when any generated file is stale or missing.

**Should generated private configs be committed to `aprog-private`?**
Decision: **Yes.** `verification-config.json` and `private-assignment-manifest.json` are committed to `aprog-private/generated/`. They serve as a verification audit trail and allow CI to check staleness without regenerating.

---

## Private submissions

**Should all private bundles be encrypted?**
Decision: **No by default.** Encryption is optional. Contributors pass `--encrypt` to `aprog submit` or `aprog package-private` to GPG-encrypt the bundle. Organizations that require encryption set `require_encryption = true` in their `aprog.toml` root config; the CLI will then reject unencrypted bundles.

**Should hidden tests be contributor-authored, maintainer-authored, or both?**
Decision: **Contributor-authored.** Hidden tests are included in the private bundle. Maintainers may augment by committing additional test cases directly to `aprog-private/hidden-tests/<slug>/` after intake, but the contributor must provide a baseline set.

**Should private bundles be archived after intake?**
Decision: **No by default.** Bundles are deleted after successful intake. Pass `--archive <dir>` to `aprog intake` to keep a copy. The `aprog-private` repository is the canonical record.

---

## Grader integration

**What function should generated adapters expose?**
Resolved: `run_autograder.py` imports `make_pipeline() -> Pipeline` from `grader.pipeline` and calls it inside a `config()` context manager. See `architecture/generated-configs.md`.

**What manifest fields does the grader package require?**
Resolved: lograder does not consume the AProg manifest. It uses `EnvironmentConfig` set by `run_autograder.py`. See `grader/config.md`.

**What private verification config format is most convenient?**
Resolved: See `architecture/generated-configs.md` for the `verification-config.json` schema.

**How should verification results be reported to CI?**
Resolved: `aprog verify` exits 0 on pass, 1 on fail. See `tools/aprog-verify.md`.

**How should performance tests be configured?**
Resolved: Via `PerformanceCase(time_limit: float)` in `grader/pipeline.py`. See `grader/steps.md`.

---

## Full verification on every PR?

Decision: **No.** Public-only validation (`aprog validate --all`) runs on every PR that touches `assignments/`, `templates/`, `aprog.toml`, or `tools/`. Full verification (`aprog verify`) runs on `workflow_dispatch` (manual trigger) or when a maintainer applies a `verify` label to the PR. Rationale: full verification requires `aprog-private` access and is expensive; it does not need to run on every contributor PR.
