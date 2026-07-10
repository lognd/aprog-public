# Study Guide 4: Command-Line & Compilation

This module builds fluency navigating an unfamiliar codebase from the shell
alone, cleaning up a git history that has gone wrong, and understanding what
`g++` actually does in the four hidden stages between source code and a
runnable binary.

## Know before you start

- A working shell and the ability to run commands in it
  [assumed: row 2 -- Environment Setup]
- `g++` installed and able to compile a single-file program
  [assumed: row 2 -- Environment Setup]
- git and the `gh` CLI installed and configured
  [assumed: row 2 -- Environment Setup]

## Taught here

Concept: navigating an unfamiliar directory tree from the shell
- Know that `pwd` prints the current working directory and `ls` lists its
  contents; `ls -a` also shows hidden entries (names starting with `.`),
  and `ls -la` adds permissions, size, and modification time.
- Be able to use `cd <path>` to move between directories without a file
  browser or IDE.
- Know that `cat <file>` dumps a whole file, while `head -n 20 <file>`
  shows only the first lines -- useful for a quick look at a long file.
- Know that a file's extension is only a hint about its content, not a
  guarantee; `file <path>` inspects the actual bytes and reports the real
  file type (ASCII text, ELF binary, compressed archive, etc.).
- Know that `strings <path>` extracts every printable run of characters
  from any file, including binaries, which is useful for finding readable
  text hidden inside a non-text file.
- Be able to combine `find . -name "<pattern>"` (search by filename across
  a whole tree) with `grep -r "<text>" <dir>` (search by file content
  across a whole tree) as the core loop for exploring an unfamiliar
  codebase: narrow with `find`, then search inside with `grep`.
- Be able to use `grep -rl "int main" .` to locate the file that defines a
  program's entry point in one command.

Concept: compiling a multi-file project by hand
- Know that `-I<dir>` adds `<dir>` to the compiler's header search path, so
  `#include` directives can find headers that are not in the same
  directory as the source file including them.
- Be able to construct a manual `g++ -I <header-dir> -o program
  <path-to-main.cpp>` command for a project with headers in a separate
  directory.
- Know that a missing symbol error or a triggered `#error` preprocessor
  directive during compilation is informative signal about which header or
  source file is wrong, not just a failure to move past.

Concept: the four compilation stages
- Know the four stages `g++` runs internally, in order: preprocess (`cpp`,
  `.cpp` -> `.i`), compile (`cc1plus`, `.i` -> `.s` assembly), assemble
  (`as`, `.s` -> `.o` object code), and link (`ld`, `.o` files ->
  executable).
- Know that `.s` (assembly) is a human-readable listing of the exact CPU
  instructions the program will run, while `.o` (object code) is the same
  instructions translated into raw bytes -- not yet a runnable program.
- Be able to invoke each stage separately: `g++ -E` (preprocess only),
  `g++ -S` (compile to assembly only), `g++ -c` (assemble only), and plain
  `g++` object files together (link only).
- Know that a translation unit is one `.cpp` file plus everything it
  `#include`s; the four stages run on each translation unit independently
  before the link step combines all resulting object files.
- Be able to check whether a file needs rebuilding by comparing
  modification times with `[ file_a -nt file_b ]` (true if file_a is newer
  than file_b), the same idea Make itself uses internally as its
  dependency graph.
- Be able to redirect a compiler's error output to a log file with `2>`
  (overwrite) or `2>>` (append), and chain commands with a pipe (`|`), for
  example piping `g++ -E` output into `wc -l` to count preprocessed lines.

Concept: git history surgery
- Be able to read the full history of a repository across all branches
  with `git log --all --oneline --graph`, and inspect one commit's diff
  with `git show <hash>` or a full-history diff view with `git log -p`.
- Know that `git revert` adds a new commit that undoes a change but leaves
  the original commit in history, whereas interactive rebase (`git rebase
  -i <parent-hash>`) can actually erase a commit by changing `pick` to
  `drop` in the editor it opens.
- Be able to reconcile a feature branch that diverged from main (each has
  commits the other lacks) by running `git rebase main` on the feature
  branch to replay its commits on top of the cleaned main, resolving any
  conflicts, then fast-forward merging with `git merge <branch>`.
- Know that `git reflog` records a log of where branch tips have pointed,
  which is the safety net for recovering from a bad rebase.

## Study checklist

- [ ] Given an unfamiliar project tree, describe the sequence of shell
      commands you would run to find `main` and figure out what it needs.
- [ ] Name the four compilation stages in order and the file extension each
      one produces.
- [ ] Explain why `git revert` is not sufficient when you need a commit
      erased entirely from history, and what to use instead.
- [ ] Explain how to reconcile two branches that have each gained commits
      since they diverged, using rebase.

## Practiced in

`terminal-archeology`, `git-heist`, `shell-build-pipeline`
