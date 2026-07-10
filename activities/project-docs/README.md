# Activity: Project Docs

Every professional software project ships with a set of standard
documentation files: a README (explains what the project is and how to use
it), a LICENSE (states the legal terms under which others may use, copy, or
modify your code), a CHANGELOG (a running log of notable changes between
released versions), a CONTRIBUTORS list (credits everyone who has worked on
the project), a CODE_OF_CONDUCT (the rules for how participants should treat
each other), and a SECURITY policy (instructions for privately reporting
security vulnerabilities instead of filing a public bug). This activity
teaches you what each file is for and what it conventionally contains.

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
- Read the Semantic Versioning specification at semver.org (a MAJOR.MINOR.PATCH
  scheme for numbering releases) and write a CHANGELOG entry for a
  hypothetical v1.0.0 release.
- Find a project on GitHub whose SECURITY.md links to a private disclosure
  process. What information do they ask reporters to include?
