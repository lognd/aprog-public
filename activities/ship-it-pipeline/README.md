# Activity: Ship-It Pipeline

In make-the-linter-happy you ran the quality tools by hand. In
pytest-dojo you wrote the tests they run. One problem remains, and it
is a human problem, not a technical one: somebody has to REMEMBER to
run all of that, every time, forever. This activity is about the robot
that removes the remembering -- CONTINUOUS INTEGRATION -- and about
what comes after the checks pass: deploying the code to a real server,
and handling the secrets (SSH keys, passwords) that deployment needs
without ever committing them to git.

You have touched the edges of this already: env-setup-git is where you
first connected to GitHub, git-mental-models gave you the picture of
commits as permanent history, and git-heist had you dig a leaked
credential out of that history. This activity closes the loop: how
teams make the checks unforgettable, and how secrets are held so there
is never anything to dig out.

## Concepts covered

- What CI is (every push, a robot runs the checks) and what CD adds
- GitHub Actions workflow anatomy: trigger (`on:`), jobs, steps
- Why a red X that blocks merging is a feature, not an obstacle
- Diagnosing "passes locally, fails in CI" -- environment drift and
  lockfiles
- GitHub Secrets: where credentials live, log masking, why fork PRs
  do not get secrets, repository vs environment secrets
- Deploy triggers (push-to-main vs tag/release) and the anatomy of an
  ssh deploy (authenticate, rsync, restart)
- `.env` practices: gitignored `.env`, committed `.env.example`,
  `load_dotenv()`, and one interface -- `os.environ` -- everywhere

## Background

Everything the questions ask about is walked through here. Read this
before launching; come back to it whenever a question stumps you.

### Part 1 -- checks.yml, line by line

A WORKFLOW is a YAML file in your repo under `.github/workflows/`.
Push one and GitHub starts obeying it -- there is no registration step
beyond the file existing. Here is a complete, real checks workflow for
a Python project using uv:

```yaml
name: checks                        # display name in the Actions tab

on: [push, pull_request]            # TRIGGER: run on every push and PR

jobs:
  checks:                           # one JOB, named "checks"
    runs-on: ubuntu-latest          # a fresh Linux virtual machine
    steps:                          # STEPS: commands, run in order
      - uses: actions/checkout@v4   # step 1: clone this repo's code
      - uses: astral-sh/setup-uv@v5 # step 2: install uv on the VM
      - run: uv sync --locked       # step 3: install deps from uv.lock
      - run: uv run ruff check .    # step 4: the linter gate
      - run: uv run ruff format --check .  # step 5: the format gate
      - run: uv run ty check .      # step 6: the type gate
      - run: uv run pytest -q       # step 7: the test gate
```

Read the three levels: `on:` is the TRIGGER (WHEN -- every push, every
pull request), `jobs:` declares machines (each job gets a fresh
virtual machine that exists only for this run), and `steps:` are the
commands (WHAT, in order; the first failing step fails the job). A
`uses:` step runs a published, reusable action -- `checkout` clones
your repo onto the VM, `setup-uv` installs uv. A `run:` step is
literally a shell command, and steps 4-7 are the exact four gates from
make-the-linter-happy. The robot did not learn anything new; it just
never forgets.

Step 3 is the answer to the most common CI mystery, "passes locally,
fails in CI": the VM is built from nothing, so if dependency versions
are not pinned, it may install different versions than your laptop
has. `uv.lock` is a LOCKFILE -- a committed record of the exact
version of everything -- and `uv sync --locked` installs precisely
those versions. Same inputs, same behavior, everywhere.

When this workflow runs on a pull request, its result appears on the
PR as the green check or red X -- and with a branch protection rule,
the red X blocks the merge button. That blocking is the point: the
rule "run the checks before merging" stops living in people's memories
and starts living in a mechanism.

### Part 2 -- deploy.yml, line by line

Deployment means getting the new code onto a server and running. The
oldest and most transparent way is ssh + rsync, and it is worth
understanding line by line even if you later use fancier tooling:

```yaml
name: deploy

on:
  push:
    tags: ["v*"]                    # TRIGGER: only version tags (v1.2.0)

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: webfactory/ssh-agent@v0.9.0   # load the deploy key
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - run: ssh-keyscan -H server.example.com >> ~/.ssh/known_hosts

      - run: rsync -az --delete ./app/ deploy@server.example.com:/srv/app/

      - run: ssh deploy@server.example.com "sudo systemctl restart myapp"
```

The trigger: `on: push: tags: ["v*"]` fires only when someone pushes a
tag starting with `v` -- a deliberate, named release. The alternative,
`on: push: branches: [main]`, deploys every merged change immediately;
that is continuous deployment, and it is a legitimate choice when your
checks are strong and rollback is cheap. Tag-triggered deploys keep a
human decision in the loop. Neither is "the right one"; the tradeoff
is speed of delivery against deliberateness of releases.

The steps, one at a time:

1. **ssh-agent** starts an SSH authentication helper on the VM and
   loads the private key into it -- from `secrets.SSH_PRIVATE_KEY`,
   never from a file in the repo. The key exists on the VM only in
   memory, only for this run.
2. **ssh-keyscan** fetches the server's HOST KEY (the server's own
   identity fingerprint) and appends it to `known_hosts`. Without
   this, the first ssh connection would stop and interactively ask
   "are you sure you want to continue connecting?" -- and a robot
   cannot answer prompts.
3. **rsync** copies the built application to the server.
   `-a` preserves permissions and timestamps, `-z` compresses in
   transit, `--delete` removes server files that no longer exist
   locally, so the server converges to exactly what CI built. rsync
   only transfers what changed, so repeat deploys are fast.
4. **ssh ... restart** tells the service manager on the server to
   restart the app. A running process keeps its already-loaded code
   forever; nothing picks up the new files until this step.

Authenticate, sync, restart -- get in the door, put the code in
place, turn it off and on again.

### Creating the secret

First, generate a DEDICATED deploy keypair. Never use your personal
SSH key for this: your personal key is your identity (it can push to
all your repos), while a deploy key should open exactly one door, so
that leaking it costs one server's access, not your whole account:

```bash
ssh-keygen -t ed25519 -f deploy_key -C "ci-deploy myapp" -N ""
```

That writes `deploy_key` (private) and `deploy_key.pub` (public). The
PUBLIC half goes on the server, appended to
`~deploy/.ssh/authorized_keys`. The PRIVATE half becomes the GitHub
secret -- two ways to set it:

- **Settings UI**: repo -> Settings -> Secrets and variables ->
  Actions -> New repository secret; name it `SSH_PRIVATE_KEY`, paste
  the contents of `deploy_key`.
- **Terminal**: `gh secret set SSH_PRIVATE_KEY < deploy_key`

Then delete the local copy of the private key. Secrets are write-only
once stored: you can replace or remove them, never read them back.
Workflow runs see them as `${{ secrets.SSH_PRIVATE_KEY }}`, the runner
masks their values as `***` if they ever appear in a log, and pull
requests from forks do not receive them at all -- a stranger's PR
controls the code (including the workflow file itself), so it runs
without your credentials.

For production, use an ENVIRONMENT secret instead of a repository
secret: attach the secret to an environment named `production` and add
a required-reviewers rule, and any job declaring
`environment: production` pauses until a human approves it -- an
automated deploy with a manual gate on the one environment that
matters.

Honest alternatives paragraph: ssh + rsync is the transparent
baseline, not the only way. Platform-as-a-service hosts (Render, Fly,
Heroku-alikes) watch your repo and auto-deploy on push with no
workflow of yours at all; containerized setups have CI build and push
an image to a REGISTRY (a versioned store of runnable images) and the
server pulls it; and some setups invert control with a WEBHOOK -- the
server exposes an endpoint that GitHub calls after a push, and the
server updates itself. Every one of these still reduces to the same
three beats -- authenticate, move the artifacts, restart -- just with
different names on the steps.

### .env: configuration and secrets at run time

Your app needs configuration that must not live in the code -- a
database URL with a password in it, an API token. The convention is a
`.env` file in the project root:

```
DATABASE_URL=postgres://user:changeme@localhost/dev
API_TOKEN=sk-fake-not-a-real-token
```

(Those are placeholder values -- a real `.env` holds real ones.) At
run time, `load_dotenv()` from the `python-dotenv` package reads the
file and loads each line into the process's ENVIRONMENT VARIABLES,
and your code reads them from there:

```python
import os
from dotenv import load_dotenv

load_dotenv()                              # reads .env, fills os.environ
db_url = os.environ["DATABASE_URL"]        # same line works everywhere
```

Two rules make this safe and teachable:

- `.env` is ALWAYS in `.gitignore`. It holds real values, so it never
  enters git history. (git-heist showed you why history is forever.)
- A `.env.example` IS committed, holding the same variable names with
  obviously fake values -- exactly like the block above. It documents
  the SHAPE of the configuration; a new teammate copies it to `.env`
  and fills in real values.

In CI and on the server there is no `.env` -- the same variable names
are provided from secrets, mapped into the environment by the
workflow:

```yaml
      - run: uv run pytest -q
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

Your code does not change at all: it reads `os.environ` either way;
only where the value comes from differs. That is the twelve-factor
config rule in one line -- configuration lives in the environment,
not in the code, so the same commit runs unchanged on your laptop, in
CI, and in production.

### Optional: keeping AI assistants out of your .env

This subsection is optional reading and nothing in the activity quizzes
it.

If you use an AI coding assistant that can read files and run commands
(Claude Code, for example), your `.env` is sitting in the one
directory you gave it access to. Assistants are instructed not to go
looking for secrets, but instructions are not mechanisms -- and by now
you know which of those wins. Claude Code supports HOOKS: commands of
yours that run before each tool call and can veto it. This
`.claude/settings.json` blocks reads of any `.env` file:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json,sys; p=json.load(sys.stdin).get('tool_input',{}).get('file_path',''); sys.exit(2 if p.split('/')[-1].startswith('.env') and not p.endswith('.env.example') else 0)\""
          }
        ]
      }
    ]
  }
}
```

Reading it: `PreToolUse` hooks fire before every tool call;
`"matcher": "Read"` scopes this one to file reads; the command
receives a JSON description of the pending call on stdin, pulls out
the target path, and exits with code 2 -- the "block this call" signal
-- for any file named `.env` or `.env.*`, while letting the harmless
`.env.example` through. Exit 0 lets everything else proceed.

Treat this exactly like the runner's `***` masking: defense-in-depth
beside `.gitignore`, not a replacement for it (a shell command could
still `cat .env` unless you extend the matcher to `Read|Bash` and
inspect commands too). The full hook interface -- other events, other
matchers, JSON responses -- is in the Claude Code hooks documentation:
https://code.claude.com/docs/en/hooks

## How it works

The launcher asks thirteen judgment calls, one at a time -- no code is
written. Each question lists its answer options; type the one you
choose. A correct answer shows a short explanation and moves on; a
wrong answer explains the specific misconception behind that choice
and re-prompts. Get all thirteen and the passphrase unlocks.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all thirteen questions and the launcher
prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- when in doubt, find the mechanism</summary>

Half the questions resolve the same way: prefer the answer where a
MECHANISM replaces a thing someone must remember or a person who must
be trusted. The red X, the secrets store, fork-PR isolation, the
lockfile -- each one is a rule moved out of human memory into
machinery.

</details>

<details>
<summary>Hint 2 -- whose fault can it be?</summary>

For the "passes locally, fails in CI" question: the commit is
identical in both places, so the code cannot be the difference. List
what else exists in each place, and the answer is the only thing that
plausibly differs.

</details>

<details>
<summary>Hint 3 -- follow the secret's whole lifetime</summary>

For every secrets question, trace where the value exists over time: a
committed file exists in history forever; a secret exists in GitHub's
encrypted store and briefly in a VM's memory. Choose the answer where
the secret touches the fewest permanent places.

</details>

## Going further

- Add the checks.yml from this README to one of your own repos,
  verbatim, and push a commit with a deliberate ruff violation. Watch
  the Actions tab catch it, then fix and watch it go green.
- Enable branch protection on that repo (Settings -> Branches) and
  require the checks to pass; open a PR with a failing test and
  confirm the merge button locks.
- Read your repo's Actions log for a run and find the masked `***`
  where an action echoed a token. Then read GitHub's docs on
  `add-mask` to see how values become maskable at all.
- Set up the `.env` + `.env.example` pattern in your current project,
  including the `.gitignore` entry, and confirm with `git status` that
  the real file never shows up as trackable.
