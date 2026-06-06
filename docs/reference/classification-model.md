# Classification Model

Valid classification values are defined in `aprog-public/aprog.toml`. The validator rejects any `language`, `difficulty`, `topic`, `concept`, or `label` that is not declared there.

To see what values are registered:

```bash
cat aprog.toml                  # see all declared values
aprog list --language python    # filter assignments by field
```

## Fields

| Field | Required | Where declared |
|---|---|---|
| `language` | yes | `aprog.toml [classification.languages]` |
| `difficulty` | yes | `aprog.toml [classification.difficulties]` |
| `topics` | yes (non-empty) | `aprog.toml [classification.topics]` |
| `concepts` | no | `aprog.toml [classification.concepts]` |
| `labels` | no | `aprog.toml [labels]` |
| `course` | no | free-form string |
| `module` | no | free-form string |

## Example `aprog.toml` excerpt

```toml
[classification.languages.python]
name = "Python"

[classification.languages.cpp]
name = "C++"

[classification.difficulties.easy]
name = "Easy"
rank = 1

[classification.difficulties.medium]
name = "Medium"
rank = 2

[classification.topics.data-structures]
name = "Data Structures"

[labels.starter-code]
name = "Starter code provided"

[organization]
require_encryption = false
require_hidden_tests = true
default_grader_visibility = "after_due_date"
```

## Adding new values

Only maintainers may add new classification values. Open a PR that edits `aprog.toml` under the appropriate table. Do not add a new topic or language in the same PR as an assignment -- the value must be in `aprog.toml` before the assignment can reference it.
