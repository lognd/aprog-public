# Tool Design: `aprog verify`

Runs full maintainer verification for an assignment.

## Usage

```bash
aprog verify <assignment-slug> \
  --public ../aprog-public \
  --private ../aprog-private
```

## Responsibilities

`aprog verify` should:

- ensure public validation passes
- ensure the private solution directory exists
- ensure the grader file (`grader/pipeline.py`) exists in the private bundle
- ensure hidden tests are discoverable, if present
- invoke the grader against the reference solution
- report whether the reference solution passes all tests

## Verification flow

1. Run `aprog validate <slug>` for public validation. Abort if it fails.

2. Build the normalized private manifest from `verification-config.json`.

3. Set up `EnvironmentConfig` with `root_directory` pointing to the reference solution:

   ```python
   with config(root_directory=private_repo / "solutions" / slug):
       pipeline = make_pipeline()
       score = pipeline()
   ```

4. Check the result. Verification passes if:
   - the pipeline did not stop early (no fatal `Err` return before the final step)
   - `score.total().earned >= score.total().possible` (reference solution earns full non-extra-credit points)

5. Emit a pass/fail report to stdout. Exit 0 on pass, 1 on fail.

6. On success, update `verification-config.json` in `aprog-private`:
   - set `verification_state` to `"verified"`
   - record the current `private_source_hash`

## Exit codes

| Code | Meaning |
|---:|---|
| 0 | Verification passed |
| 1 | Verification failed |
| 2 | Usage error |
| 3 | Private repository missing or inaccessible |
| 4 | Solution directory missing |
| 5 | Grader pipeline file missing |
