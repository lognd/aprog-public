# Activity: Git Mental Models

You have probably already run `git commit`, `git branch`, `git merge`, and
maybe `git rebase` -- typed them because a tutorial or an instructor told you
to, and watched them work. This activity does not ask you to run any of
those commands. Instead it asks you to explain, in plain language, what each
one actually DOES underneath -- what a commit really is, what a branch really
is, and why merge and rebase produce different-looking histories from the
exact same starting point. Every question shows a small diagram of commits
and branches (using letters like `A`, `B`, `C` to stand for individual
commits) and asks a conceptual question about it.

## Background

### The object graph: a commit is a snapshot, not a diff

It is tempting to think of a commit as "the changes I made" -- a diff. That
is not what git stores. Every commit is a full SNAPSHOT of your entire
tracked file tree at that moment, plus a pointer back to its PARENT commit
(the commit that came immediately before it). Chaining those parent pointers
together is what makes "history" a real, walkable sequence:

```
A---B---C
```

Here, `C` points back at `B`, and `B` points back at `A`. `git diff` and
`git show` compute a difference between two snapshots ON DEMAND, for your
convenience when reading history -- but that computed diff is never what got
stored. Git is smart enough internally to avoid literally duplicating every
byte of every file in every commit (unchanged files are shared behind the
scenes), but conceptually, think of each commit as a complete picture of the
project at that instant, not a delta.

### A branch is a pointer, not a copy

A BRANCH is a named, movable pointer to a single commit. Nothing more.

```
A---B---C
         ^
       main
```

When you run `git branch feature`, git does not copy any files or duplicate
any commits. It writes down one small fact: "the name `feature` currently
points at commit C." That is the entire operation, which is why creating a
branch is close to instantaneous no matter how large the repository is:

```
A---B---C
         ^
    main, feature   (two names, same commit)
```

### HEAD: where you are right now

HEAD answers the question "what commit am I currently looking at?" Normally,
HEAD does not point directly at a commit -- it points at a branch NAME, and
that branch name points at a commit. When you commit, git creates the new
commit with the old commit as its parent, then drags the CURRENT branch's
pointer forward to the new commit. Because HEAD is just following the
branch, it "moves" too, without anything having to update it directly.

```
before commit:            after commit:
A---B---C                 A---B---C---D
         ^                             ^
    main, HEAD                    main, HEAD
```

### Merge vs. rebase: two ways to reconcile the same fork

Both of the diagrams below start from the exact same graph -- two branches
that diverged after `C`:

```
starting point:
A---B---C
     \
      D---E   (feature)
```

**Merge** creates a brand new commit with TWO parents, one from each branch.
Nothing about the existing commits changes; both lines of history are kept,
and the graph honestly shows that a divergence happened and was later
rejoined -- a "knot":

```
git merge feature   (while on main)

A---B---C-------M
     \         /
      D-------E
```

`M` has two parents: `C` and `E`. Every one of `A`, `B`, `C`, `D`, `E` is
still present, unchanged, and reachable. This is the most important fact
about merge: it never rewrites or discards anything, it only adds.

**Rebase** takes a completely different approach: it REPLAYS your commits,
one at a time, on top of a new base, as if you had started your work from
there in the first place.

> Rebase re-records your work as if you had started from the new base -- it
> plays your commits back on top of it.

```
git rebase main   (while on feature)

A---B---C
              \
               D'---E'   (feature, after rebase)
```

`D` and `E` are not moved -- they are left behind, unreferenced by any
branch. `D'` and `E'` are brand new commits, with the same code changes but
different commit hashes (a commit's hash depends on its parent, and the
parent changed), sitting in a single straight line on top of `C`. This is
why rebase is often described as producing a "clean" history: there is no
visible fork at all, even though one really happened.

Neither approach is free. Merge preserves the true, honest shape of history
(the divergence really is visible) at the cost of a knot in the graph.
Rebase produces a clean straight line at the cost of the original commits'
identities (and the visible record that a divergence happened at all). Which
one to reach for is a judgment call every team makes, sometimes per-branch.

### Why you never rebase a shared branch

Because rebase gives every replayed commit a NEW hash, rebasing a branch
that someone else has already pulled and built more commits on top of is
dangerous: their commits still point at the OLD, now-abandoned version of
your commits. When they try to sync, git has no way to cleanly reconcile
their history (built on the old commits) with your rewritten one (built on
new commits with new hashes) -- the two histories look unrelated even though
they represent similar work. The rule that follows directly from this: only
rebase branches that are still entirely local to you. Once a branch is
shared and others may have pulled it, add to it with ordinary commits or
merges -- never rewrite its existing history.

### The staging area (index): a loading dock between your files and history

Between your working tree (the files you are actually editing) and history
(the permanent chain of commits) sits a third area called the STAGING AREA,
or the INDEX. `git add <file>` does not touch history at all -- it copies a
snapshot of that file's current contents onto the loading dock, ready to be
included in your NEXT commit. Only `git commit` actually seals whatever is
on the loading dock into a real, permanent commit.

```
working tree           staging area (index)         history
readme.txt (edited)    [ nothing staged yet ]        A---B---C

              git add readme.txt
                      |
                      v
working tree           staging area (index)         history
readme.txt (edited)    [ readme.txt snapshot ]        A---B---C

              git commit -m "..."
                      |
                      v
working tree           staging area (index)         history
readme.txt (unchanged) [ cleared ]                    A---B---C---D
```

### What problem this whole system solves

Step back from the individual commands and there are really only two
problems the entire commit/branch/merge/rebase system is built to solve:

1. **Parallel work without constant coordination.** Because branches are
   free to create and commits never overwrite each other, many people (or
   one person juggling several experiments) can work independently at the
   same time and reconcile later, instead of taking turns.
2. **A complete, permanent, restorable history.** Because commits are
   immutable snapshots chained together, nothing is ever silently lost --
   any past state of the project can be found, compared, or restored.

## What each command conceptually does

| Command | What it conceptually does |
|---|---|
| `git commit` | Seals whatever is staged into a new permanent snapshot, with the previous commit as its parent, and drags the current branch's pointer forward to it |
| `git branch NAME` | Creates a new named pointer at the current commit -- copies nothing |
| `git checkout NAME` / `git switch NAME` | Moves HEAD to follow a different branch (or a specific commit), and updates your working files to match that commit's snapshot |
| `git merge OTHER` | Reconciles two lines of history by creating one new commit with two parents (or, if the current branch has not diverged, just slides its pointer forward -- a fast-forward, no new commit) |
| `git rebase OTHER` | Replays your current branch's commits, one at a time, onto the tip of `OTHER`, producing new commits with new identities and a straight-line history |
| `git add FILE` | Stages a snapshot of `FILE`'s current contents onto the loading dock, ready for the next commit -- history is untouched |
| `git status` | Reports the difference between your working tree, the staging area, and the last commit -- what is staged, unstaged, and untracked |
| `git log` | Walks the parent-pointer chain backward from the current commit (or any given commit) and prints what it finds |
| `git fetch` | Downloads new commits and branch-pointer updates from a remote and updates your local record of them -- your current branch does not move |
| `git pull` | Fetch, immediately followed by merging (or rebasing, depending on configuration) the newly fetched commits into your current branch |
| `git push` | Uploads your local commits to a remote and asks it to move its branch pointer to match yours |

## Concepts covered

- Commits as immutable snapshots chained by parent pointers, not diffs
- Branches as named, movable pointers -- creating one copies nothing
- HEAD as "the branch you are currently following"
- Merge commits: two parents, both histories fully preserved
- Fast-forward merges: no new commit, just a pointer slide, only possible
  when the target branch has not diverged
- Rebase as replay: same changes, new commit identities, linear history
- Why rebasing a shared branch breaks other people's history
- The staging area (index) as the holding area between working tree and
  history
- `fetch` (download only) vs `pull` (download and reconcile)

## How it works

Twelve questions, each showing a small ASCII diagram of commits and
branches. Every question asks you to identify what is conceptually true
about the diagram -- what a command creates, how many parents a commit has,
whether two branches would fast-forward or need a real merge, and so on.
Each question lists the exact set of allowed answers; type one of them
exactly. Every wrong answer you might reasonably pick has its own
explanation of why it is wrong, and the right answer comes with a full
explanation of the underlying model, not just a one-line confirmation.

## Getting started

```bash
python3 launch.py
```

No repository, no shell, no git commands to actually run -- this activity is
entirely about reasoning through diagrams on paper (or in your head).

## You will know you are done when...

You have answered all twelve questions correctly and the launcher prints
the passphrase.

## Hints

<details>
<summary>Hint 1 -- distinguishing what a command does from what it looks like it does</summary>

Several questions offer an answer that sounds plausible but describes what
you might expect a command to do from its name, not what it actually does
under the hood (for example, assuming `git branch` copies files, or that
`git commit` moves HEAD directly instead of moving the branch it follows).
When in doubt, go back to the object-graph model in the Background section:
commits are snapshots with parent pointers, branches are movable names, and
HEAD just follows whichever branch is checked out.

</details>

<details>
<summary>Hint 2 -- fast-forward vs. true merge</summary>

Ask one question: has the branch you are merging INTO gained any commits of
its own since the two branches diverged? If no, it is a fast-forward (just a
pointer slide). If yes, a real two-parent merge commit is required, because
there are now genuinely two paths that must be joined.

</details>

<details>
<summary>Hint 3 -- what makes a commit hash change</summary>

A commit's hash is computed from its content, including which commit it
lists as its PARENT. If a commit's parent changes (which is exactly what
happens to every commit rebase replays), the hash changes too, even if the
code change itself is identical.

</details>

## Going further

- For hands-on practice with the destructive side of history rewriting --
  actually running `git rebase -i` to drop bad commits and reconcile a
  diverged branch -- see the [git-heist](../git-heist/) activity. This
  activity built the mental model; git-heist is where you use it.
- [learngitbranching.js.org](https://learngitbranching.js.org) is a free,
  interactive visualizer where you can type real git commands and watch the
  commit graph animate in response. It is an excellent way to check your
  mental model against real command behavior once you have worked through
  this activity's questions.
- Pick any real git repository you have locally and run
  `git log --all --oneline --graph`. Can you point at a spot in the graph
  and correctly say whether it is a merge commit (two parents) or an
  ordinary commit? Use `git show <hash>` to check your answer -- a merge
  commit's output starts with two `parent` lines instead of one.
- Rebase a small local branch of your own onto a moved `main` and run
  `git log --oneline` before and after. Note that the commit hashes changed
  even though the code did not. Then run `git reflog` -- can you still find
  the original, now-abandoned commits?
