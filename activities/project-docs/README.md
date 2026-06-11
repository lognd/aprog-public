# project-docs

## What you will practice

- Writing standard open-source project documentation files
- Understanding the purpose and conventional structure of README,
  LICENSE, CHANGELOG, CONTRIBUTORS, CODE_OF_CONDUCT, and SECURITY files
- Applying Markdown heading conventions used in real projects

## How it works

You are dropped into a shell with a minimal C++ project that has no
documentation at all. Your job is to create six documentation files,
each containing the required section headers.

The launcher tells you exactly which headers each file must contain.
You write the content under each header yourself. The validator only
checks that the required headers are present -- it does not grade your
writing.

Required files and required headers:

- `README.md` -- `# <title>`, `## Description`, `## Installation`,
  `## Usage`, `## Contributing`, `## License`
- `LICENSE` -- any content (non-empty)
- `CHANGELOG.md` -- `## [Unreleased]`, `### Added`, `### Changed`,
  `### Fixed`
- `CONTRIBUTORS.md` -- `## Contributors`
- `CODE_OF_CONDUCT.md` -- `## Our Pledge`
- `SECURITY.md` -- `## Reporting a Vulnerability`

## How to run

```
python3 launch.py
```

Type `exit` when you have created all six files and are ready for the
validator to check your work.
