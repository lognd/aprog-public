# Study Guide 61: Large Projects

This is a synthesis lecture, not a new-machinery lecture: it takes
practices already taught piecemeal across the course -- reading
unfamiliar code, structuring a multi-file build, using git as a team
instead of solo, managing external dependencies, testing discipline, and
writing documentation -- and reframes them as the habits that separate a
single-file homework program from a project other people can safely work
inside. No artifact accompanies this row; it is taught in lecture.

## Know before you start

- Shell navigation and exploring an unfamiliar filesystem
  [assumed: row 2 -- Environment Setup]
- Reading an unfamiliar codebase using only shell commands, with no IDE
  index to lean on [assumed: row 4 -- Command-Line & Compilation
  (terminal-archeology)]
- git basics: commits, branches, and history [assumed: row 2 --
  Environment Setup; row 4 -- Command-Line & Compilation (git-heist)]
- Makefile and CMake project structure for a single project
  [assumed: row 8 -- Makefile & CMake]
- README and project-organization conventions for one project
  [assumed: row 9 -- C++ Standards, Project Organization, README]
- Static and dynamic libraries as units of already-compiled, reusable
  code [assumed: row 40 -- Libraries]
- Unit testing with a real test framework [assumed: row 17 -- Testing
  Tools]
- The named design patterns and what problem each one solves
  [assumed: row 24 -- Design Patterns]

## Taught here

Concept: reading unfamiliar codebases at scale
- Know that the skill exercised in row 4's terminal-archeology activity
  (using only shell commands -- `ls`, `grep`, `find`, reading files
  directly -- to orient inside a codebase with no prior explanation)
  is exactly the skill a large, real project demands on day one of a new
  job or when picking up an unfamiliar open-source repository, just at a
  larger scale: dozens or hundreds of files instead of a handful.
- Know a practical entry strategy for an unfamiliar large codebase:
  start from the README and build instructions, find the program's
  actual entry point (e.g. `main()`), then trace outward one function
  call at a time rather than trying to read every file in isolation.
- Know that `grep`/code search across a whole repository (searching for a
  function or variable name everywhere it is used) is usually a faster,
  more reliable way to understand how a piece of code is actually used
  than reading its own file in isolation.

Concept: project layout and build systems at scale
- Know that the file layout conventions from row 9 (separating headers
  from source, a consistent directory structure) and the CMake project
  structure from row 8 exist specifically so a build system, and a human
  reader, can scale from one file to hundreds without ad hoc rules
  re-invented per project.
- Know that a large project typically splits into multiple build targets
  (e.g. a core library plus a separate executable, or several
  executables sharing one library) so that pieces can be built, tested,
  and reused independently -- this is the direct scaling-up of row 40's
  static/dynamic library split from "one library by hand" to "how a real
  project is actually organized."
- Know that a large project's `CMakeLists.txt` is usually split across
  multiple files (one per subdirectory, `add_subdirectory()`-linked into
  a root file) rather than kept as one flat file, for the same reason
  source itself is split into multiple files: so one team member's
  change to one subsystem's build rules does not require touching
  everyone else's.

Concept: versioning and collaboration
- Know that git branches let multiple people (or one person working on
  multiple features) develop changes in isolation without one person's
  in-progress work breaking another's, merging back into a shared branch
  only once ready.
- Know a pull request (PR) is a request to merge one branch's changes
  into another, reviewed by other people before merging -- the
  collaborative layer git-heist's solo history navigation does not by
  itself require, but every real team project runs on.
- Know code review's actual purpose: catching bugs and design problems
  before they reach the shared branch, spreading knowledge of the
  codebase across more than one person, and creating a second set of
  eyes on any change that affects other people's work.
- Know that clean, descriptive commit history (small, logically separate
  commits with clear messages, the discipline row 4's git-heist forces
  students to read and reconstruct) becomes far more valuable at project
  scale, where `git log`/`git blame` are often the only record of *why*
  a change was made, long after the person who wrote it has moved on.

Concept: dependency management at scale
- Know that a large project typically depends on many external libraries
  at once (row 40's static/dynamic library mechanics, multiplied), and
  that manually tracking and building each one by hand does not scale --
  this is the problem package managers solve.
- Know that CMake's `find_package()` (used by sfml-canvas's grader to
  locate SFML) is one mechanism for locating an already-installed
  dependency; C++ package managers (e.g. Conan, vcpkg) automate fetching
  and building dependencies a project declares, rather than requiring
  every contributor to install them by hand.
- Know Python's equivalent story from row 45 onward: `uv`/`pip` installing
  packages declared in a project's dependency file, and a virtual
  environment isolating one project's dependency versions from another's
  -- the same underlying problem (which exact library version does this
  project need, and where does it come from) in a different ecosystem.
- Know that pinning exact dependency versions (rather than "latest") is
  what keeps a build reproducible: the same declared dependencies should
  produce the same behavior on a teammate's machine, in CI, and on a
  grading server months later.

Concept: testing discipline at scale
- Know that the unit testing habits from row 17 (a real test framework,
  one focused test per behavior) scale up into a project-wide test
  suite, typically run automatically on every proposed change via
  continuous integration (CI) -- an automated system that builds and
  tests a project on every push or pull request, catching regressions
  (a previously working behavior breaking) before a human reviewer even
  looks at the change.
- Know that a large project's test suite is what makes large-scale
  refactoring safe: without tests, a change that alters unrelated
  behavior can go unnoticed until a user hits it; with tests, the same
  break is usually caught within minutes.

Concept: documentation at scale
- Know that the README and project-organization conventions from row 9,
  written for a single small project, become load-bearing at scale: a
  large project's README is often the only thing standing between a new
  contributor and hours of guessing, and out-of-date documentation
  actively misleads rather than merely failing to help.
- Know that documentation belongs alongside the code it describes (this
  course's own convention of updating `docs/` in the same change as the
  code) specifically so it does not silently drift out of sync as the
  code changes.

Concept: design lessons that only pay off at scale
- Know that the design patterns from row 24 (recognized, named solutions
  to recurring design problems) exist largely because large projects
  repeatedly hit the same handful of structural problems -- a shared
  vocabulary lets a team discuss a design in a few words ("just make it
  a Strategy") instead of re-explaining the same structure from scratch
  every time.
- Know that a code smell (a surface pattern in code that often, but not
  always, indicates a deeper design problem -- e.g. a very long function,
  duplicated logic, a class doing several unrelated jobs) is a heuristic
  for where to look, not an automatic verdict; refactoring (restructuring
  code's internal design without changing its external behavior) is the
  response once a real problem is confirmed.
- Know that refactoring is only safe to do confidently at scale when a
  test suite already exists to confirm external behavior did not change
  -- tying this concept directly back to the testing-discipline point
  above.

## Study checklist

- [ ] Describe an entry strategy for orienting inside an unfamiliar
      large codebase using only the shell.
- [ ] Explain why a large project's CMake setup is usually split across
      multiple files instead of kept flat.
- [ ] Explain what a pull request and code review add on top of git
      branches alone.
- [ ] Explain why pinning dependency versions matters for a reproducible
      build.
- [ ] Explain how continuous integration changes what a test suite is
      actually for at project scale.
- [ ] Explain why documentation living next to code, rather than
      separately, matters more as a project grows.
- [ ] Explain the relationship between a code smell, refactoring, and a
      test suite.

## Practiced in

none -- lecture only
