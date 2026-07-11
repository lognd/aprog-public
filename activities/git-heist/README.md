# Activity: Git Heist

You have inherited a git repository in a sorry state. A careless developer
committed credentials, accidentally pushed a 50MB binary, and left a feature
branch stranded. Your job is to clean it up without losing any real work --
and collect the passphrase along the way.

## Concepts covered

- Reading git history with `git log --all --oneline --graph`
- Identifying problematic commits with `git show` and `git log -p`
- Erasing commits from history with interactive rebase (`git rebase -i`)
- Rebasing a diverged branch onto a cleaned history
- Fast-forward merging after a successful rebase

## How it works

A shell opens inside a fresh copy of the repository. You navigate the git
history, remove problematic commits, and reconcile a diverged feature branch.
When you exit, the copy is deleted -- nothing is saved between runs.

You must accomplish five things:

1. Understand the full history of the repository, including all branches.
2. Locate the commit that introduced credentials and remove it cleanly from
   history.
3. Find and remove the commit that added a large binary file.
4. Reconcile the diverged feature branch with main without losing any of
   its work.
5. Merge the result into main and read the passphrase.

The real code changes must survive -- do not lose the bug fix or the
utility functions. Do not delete and re-clone; work with the repo you have.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the repository.

### Step 1 -- survey the history

```bash
git log --all --oneline --graph
```

Look at both branches, every commit, and where they diverged. Use
`git show <hash>` on anything that looks suspicious.

### Step 2 -- remove the bad commits

Find the credentials commit and the binary commit. Use interactive
rebase -- a rebase that pauses to let you edit, reorder, or delete
individual commits one by one, instead of just replaying all of them --
to drop both from history:

```bash
git rebase -i <parent-hash>
```

This opens a text editor with a list of commits, one per line, each
prefixed with a command word like `pick`. Change `pick` to `drop` on the
commits you want gone, then save and close the editor.

<details>
<summary>What does this editor look like?</summary>

This activity sets your editor to `nano` for the duration of the shell, so
you do not need to know any other editor's keys. Nano shows its commands at
the bottom of the screen: use the arrow keys to move the cursor, type over
`pick` to change it to `drop`, then press `Ctrl+O` (Write Out) and `Enter`
to save, and `Ctrl+X` to exit.

</details>

### Step 3 -- reconcile the feature branch

The feature branch diverged from main some time ago -- it and main each
have commits the other does not, because they were built up separately
after that point. Check out the feature branch and rebase it on top of
the cleaned main:

```bash
git rebase main
```

Resolve any conflicts, then switch back to main and merge:

```bash
git merge feature/user-input
```

<details>
<summary>What is a conflict?</summary>

A conflict happens when git tries to replay or combine a change and cannot
tell automatically how to merge it -- usually because the same lines of a
file were edited differently on each branch. Git pauses and marks the file
with `<<<<<<<` / `=======` / `>>>>>>>` markers showing both versions; you
edit the file to keep the correct text, remove the markers, then run
`git add <file>` followed by `git rebase --continue` (or `git commit` for a
plain merge) to finish. This particular puzzle does not require resolving
any conflicts, but it is good to know what the term means before you run
into one for real.

</details>

### Step 4 -- exit

```
exit
```

The launcher verifies the history and prints the passphrase if everything
is correct.

## You will know you are done when...

`git log --oneline main` shows a clean, linear history with no credentials
file and no binary, the feature branch work is merged in, and you can
`cat PASSPHRASE.txt`.

## Going further

- After finishing, read about `git filter-repo` -- the modern replacement
  for `git filter-branch`. How does it differ from interactive rebase for
  removing a file from all commits in history?
- What does `git reflog` show after a rebase? Why does it exist and how
  could you use it to recover from a bad rebase?
- Look up the BFG Repo Cleaner and compare it to `git filter-repo` for
  the specific task of removing large binary files.

## Hints

<details>
<summary>Hint 1 -- where to start</summary>

Run `git log --all --oneline --graph` to see the full picture: both
branches, every commit, and where they diverged. Then use `git show <hash>`
on anything that looks suspicious.

</details>

<details>
<summary>Hint 2 -- finding the credentials</summary>

`git log -p` prints each commit alongside its full diff. Look for a commit
that adds a file with keys, passwords, or tokens. Note its hash -- you will
need it.

</details>

<details>
<summary>Hint 3 -- removing commits from history</summary>

`git revert` adds a new commit that undoes a change, but the original
commit stays in history. To actually erase a commit, use interactive
rebase: `git rebase -i <parent-hash>`. In the editor, change `pick` to
`drop` on any commit you want gone. Run this on main to remove both the
credentials commit and the binary commit in one pass.

</details>

<details>
<summary>Hint 4 -- reconciling the branches</summary>

After cleaning main, the feature branch is still rooted at the old history.
Check it out and run `git rebase main` to replay its commits on top of the
cleaned main. Resolve any conflicts, then switch back to main and
`git merge feature/user-input`.

</details>

<details>
<summary>Hint 5 -- checking your work</summary>

`git log --oneline main` should show a straight line with no mention of
credentials or a binary. `git show HEAD:PASSPHRASE.txt` lets you peek at a
file without switching branches. `ls` on main after the merge should show
`PASSPHRASE.txt` in the working tree.

</details>
