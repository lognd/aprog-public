# Activity: Project Docs

Every professional software project ships with a set of standard
documentation files: a README, a license, a changelog, a contributors list,
a code of conduct, and a security policy. This activity teaches you what
each file is for and what it conventionally contains.

## Concepts covered

- The purpose of README, LICENSE, CHANGELOG, CONTRIBUTORS, CODE_OF_CONDUCT, and SECURITY files
- Conventional Markdown heading structure for each documentation file
- What each section of a README is expected to contain
- Why open-source projects standardize these file names and locations

## How it works

You are dropped into a shell with a minimal C++ project that has no
documentation at all. Your job is to create six documentation files, each
containing the required section headers. The launcher tells you exactly
which headers each file must contain. You write the content under each
header yourself. The validator only checks that the required headers are
present -- it does not grade your writing.

Required files and required headers:

- `README.md` -- `# <title>`, `## Description`, `## Installation`,
  `## Usage`, `## Contributing`, `## License`
- `LICENSE` -- any content (non-empty)
- `CHANGELOG.md` -- `## [Unreleased]`, `### Added`, `### Changed`,
  `### Fixed`
- `CONTRIBUTORS.md` -- `## Contributors`
- `CODE_OF_CONDUCT.md` -- `## Our Pledge`
- `SECURITY.md` -- `## Reporting a Vulnerability`

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project. Type `exit` when you
have created all six files and are ready for the validator to check your
work.

## You will know you are done when...

All six files pass the validator and the program prints the passphrase.

## Going further

- Look at the LICENSE file in three popular open-source projects (e.g., Linux,
  React, curl). Which license does each use, and why might they have chosen it?
- Read the Semantic Versioning specification at semver.org and write a CHANGELOG
  entry for a hypothetical v1.0.0 release.
- Find a project on GitHub whose SECURITY.md links to a private disclosure
  process. What information do they ask reporters to include?
