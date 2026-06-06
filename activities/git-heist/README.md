# git-heist

You have inherited a git repository in a sorry state.
A careless developer committed credentials, accidentally pushed a 50MB binary,
and left a feature branch stranded. Your job is to clean it up without losing
any real work -- and collect the passphrase along the way.

## Your objectives

1. Understand the full history of the repository, including all branches.
2. Locate the commit that introduced credentials and remove them cleanly from history.
3. Find and remove the commit that added a large binary file.
4. Reconcile the diverged feature branch with main without losing any of its work.
5. Merge the result into main and read the passphrase.

## Commands you will need

- `git log` / `git log --all --oneline --graph`
- `git show` and `git diff`
- `git rebase -i`
- `git revert`
- `git rebase`
- `git merge`

## Rules

- Do not delete and re-clone. Work with the repo you have.
- The real code changes must survive -- do not lose the bug fix or the utility functions.
- The feature branch work must land on main.

## Getting started

    python3 launch.py

A shell opens inside a fresh copy of the repository.
When you exit, the copy is deleted -- nothing is saved between runs.

## Hints

<details>
<summary>Hint 1 -- Where to start</summary>

Run `git log --all --oneline --graph` to see the full picture: both branches, every commit, and where they diverged.
Then use `git show <hash>` on anything that looks suspicious.

</details>

<details>
<summary>Hint 2 -- Finding the credentials</summary>

`git log -p` prints each commit alongside its full diff.
Look for a commit that adds a file with keys, passwords, or tokens.
Note its hash -- you will need it.

</details>

<details>
<summary>Hint 3 -- Removing commits from history</summary>

`git revert` adds a new commit that undoes a change, but the original commit stays in history.
To actually erase a commit, use interactive rebase: `git rebase -i <parent-hash>`.
In the editor, change `pick` to `drop` on any commit you want gone.
Run this on main to remove both the credentials commit and the binary commit in one pass.

</details>

<details>
<summary>Hint 4 -- Reconciling the branches</summary>

After cleaning main, the feature branch is still rooted at the old history.
Check it out and run `git rebase main` to replay its commits on top of the cleaned main.
Resolve any conflicts, then switch back to main and `git merge feature/user-input`.

</details>

<details>
<summary>Hint 5 -- Checking your work</summary>

`git log --oneline main` should show a straight line with no mention of credentials or a binary.
`git show HEAD:PASSPHRASE.txt` lets you peek at a file without switching branches.
`ls` on main after the merge should show `PASSPHRASE.txt` in the working tree.

</details>

## You'll know you're done when...

`git log --oneline main` shows a clean, linear history with no credentials file
and no binary, the feature branch work is merged in, and you can `cat PASSPHRASE.txt`.
