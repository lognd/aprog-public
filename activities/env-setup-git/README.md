# Activity: Set Up Git and GitHub

> **Activity 7 of 8**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
> - [2. Python](../env-setup-python/)
>
> Next: [8. Discord](../env-setup-discord/)

This activity installs and configures three tools:

- **git** -- the version control program that runs on your computer.
  It records every change you make as a "commit" and lets you browse,
  share, and revert your project history.
- **GitHub** -- the website that hosts your git repositories in the
  cloud. A repository (or "repo") is a project folder that git is
  tracking the history of. You push commits here so they are backed
  up and can be submitted for grading.
- **gh** (GitHub CLI) -- an official command-line tool that
  authenticates git with GitHub, lets you clone and create
  repositories, and opens pull requests from the terminal.

<details>
<summary>What is the difference between git and GitHub?</summary>

**Git** is a program that runs on your computer. It tracks every
change you make to a set of files, stores the full history, and lets
you travel back to any past state. It also handles merging work from
multiple people. Git works entirely locally -- no internet required.

**GitHub** is a website that hosts git repositories in the cloud.
It gives you a URL others can clone from, a web interface to browse
history, and tools for collaboration (pull requests, issues, code
review). GitHub is one of several hosting options; others include
GitLab and Bitbucket. This course uses GitHub.

The relationship: git is the tool; GitHub is the storage. You commit
locally with git and push to GitHub to back up and share your work.

</details>

---

## Step 1: Install git

### Linux / WSL

```bash
sudo apt update
sudo apt install -y git
```

Verify:

```bash
git --version
```

### macOS

git is included with the Xcode Command Line Tools installed in the
compiler activity. Verify it is present:

```bash
git --version
```

If it is missing, run `xcode-select --install`.

### Windows

Use git inside WSL following the Linux instructions above. Do not
install Git for Windows separately -- the WSL git is what your
terminal, IDE, and scripts will all use.

---

## Step 2: Configure your identity

Every commit you make is stamped with your name and email. Set them
once globally:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the same email address as your GitHub account. If they do not
match, your commits will not be attributed to your profile.

<details>
<summary>Where is this stored?</summary>

`git config --global` writes to `~/.gitconfig` in your home directory.
You can view the full file with `cat ~/.gitconfig` or query individual
values with `git config --global user.name`. Project-level config
(in `.git/config` inside a repository) overrides global config for
that repo only.

</details>

Verify both are set:

```bash
git config --global user.name
git config --global user.email
```

---

## Step 3: Create a GitHub account

Go to https://github.com and sign up if you do not already have an
account. Use an email address you will have long-term -- your GitHub
profile accumulates over time and is often looked at by employers.

---

## Step 4: Install the GitHub CLI

The GitHub CLI (`gh`) is an official command-line tool for GitHub.
It authenticates git operations, lets you clone and create
repositories, open pull requests, and interact with GitHub without
leaving the terminal.

### Linux / WSL

```bash
sudo apt install -y gh
```

If that fails (older Ubuntu versions may not have it in the default
repos):

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
  https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install -y gh
```

<details>
<summary>What are these commands doing?</summary>

GitHub hosts `gh` in its own apt repository (a package source outside
Ubuntu's default repos). Before you can install from it, apt needs to
trust its signing key and know the repository URL.

`curl -fsSL URL | sudo dd of=FILE` downloads the GPG signing key and
writes it to `/usr/share/keyrings/`. GPG keys are how apt verifies
that packages have not been tampered with.

`echo "deb ..." | sudo tee FILE` writes the repository definition --
the URL and key reference -- into a `.list` file that apt reads.

After that, `apt update` picks up the new source and `apt install gh`
fetches and installs the package from it.

</details>

### macOS

```bash
brew install gh
```

### Windows (native -- PowerShell or Command Prompt)

If your IDE runs natively on Windows (CLion, PyCharm without WSL
gateway), you also need `gh` available in a Windows terminal.

**Option 1 -- winget** (built into Windows 10/11):

```
winget install --id GitHub.cli
```

Open a new terminal after installation.

**Option 2 -- installer**: Download the `.msi` from
https://cli.github.com and run it.

Verify in PowerShell or Command Prompt:

```
gh --version
```

Verify (WSL or macOS/Linux):

```bash
gh --version
```

---

## Step 5: Authenticate with GitHub

### Browser login (recommended)

Run the login wizard in your WSL terminal (or macOS/Linux terminal):

```bash
gh auth login
```

When prompted:

1. **What account?** -- GitHub.com
2. **Preferred protocol for git operations?** -- HTTPS (recommended)
   or SSH (see below)
3. **How to authenticate?** -- Login with a web browser

`gh` prints a one-time code and opens your browser. Paste the code
when prompted, approve the authorization, and return to the terminal.

### Token login (alternative)

If the browser flow does not work (for example in a headless
environment or a CI context), you can authenticate with a Personal
Access Token instead:

1. Go to https://github.com/settings/tokens
2. Click **Generate new token > Generate new token (classic)**.
3. Give it a name, set an expiration, and check the **repo** scope.
4. Click **Generate token** and copy the value immediately.

Then pipe the token to `gh`:

```bash
echo "YOUR_TOKEN_HERE" | gh auth login --with-token
```

Replace `YOUR_TOKEN_HERE` with the token you copied. Do not add
quotes or extra spaces.

### Windows users: authenticate twice

If your IDE (CLion, PyCharm) runs natively on Windows -- not through
the WSL gateway -- it uses the Windows `gh` credential helper, which
is separate from the WSL one.

You must run `gh auth login` (or the token method) in **two places**:

1. Inside your WSL terminal (authenticates git in WSL)
2. In a Windows PowerShell or Command Prompt (authenticates your IDE)

Both sessions must be authenticated for everything to work.

<details>
<summary>HTTPS vs SSH -- which should I choose?</summary>

**HTTPS** (recommended for beginners): `gh auth login` installs a
credential helper that automatically provides your token whenever git
needs to authenticate. You never type a password. This is the simpler
setup.

**SSH**: git uses an SSH key pair instead of a token. `gh` can
generate and upload the key for you automatically during login -- if
you choose SSH, answer "Yes" when it asks to generate a new SSH key.
SSH is preferred by many developers because the key never expires and
works without a browser.

Either choice gives you full access. You can switch later with
`gh auth login` again.

</details>

<details>
<summary>What does gh auth login actually do under the hood?</summary>

It authenticates your terminal session against the GitHub API and
stores a token in your system's secure credential store (or in
`~/.config/gh/hosts.yml`). For HTTPS git operations, it registers
itself as a git credential helper, so when git needs credentials for
a `github.com` URL it asks `gh` for them automatically. You never
type your password again.

</details>

Verify authentication worked:

```bash
gh auth status
```

You should see your username and a confirmation that you are logged in.

---

## Step 6: Generate a token for IDE integration

IDEs connect to GitHub directly to show pull requests, browse
repositories, and resolve conflicts. They need a Personal Access
Token (PAT) to do this.

> If you chose HTTPS in the previous step, `gh auth login` already
> handles git operations in the terminal. This token is specifically
> for IDE plugins that make their own API calls.

### Generate the token

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** > **Generate new token (classic)**.
3. Give it a descriptive name like "CLion" or "IDE".
4. Set an expiration (90 days is a reasonable default; you can
   regenerate when it expires).
5. Under **Select scopes**, check **repo** (the top-level checkbox).
   This grants full access to your repositories.
6. Click **Generate token** at the bottom.
7. **Copy the token immediately.** GitHub will not show it again after
   you leave the page. Paste it somewhere safe temporarily.

<details>
<summary>What is a Personal Access Token?</summary>

A PAT is a string that acts like a password but with a defined scope
and expiration. It identifies you to the GitHub API without exposing
your account password. The `repo` scope grants read/write access to
your repositories. Fine-grained tokens (the alternative) let you
restrict access to specific repositories and actions, which is useful
for automation but more setup than needed for IDE use.

</details>

### Add the token to CLion or PyCharm

1. Open **Settings** (Ctrl+Alt+S / Cmd+,).
2. Navigate to **Version Control > GitHub**.
3. Click **+** > **Log In with Token...**.
4. Paste your token and click **Add Account**.

CLion and PyCharm share this configuration -- set it in one and it
appears in both.

### Add the token to VS Code

The GitHub Pull Requests and Issues extension handles authentication
via OAuth (the same browser flow as `gh auth login`). Install the
extension and click **Sign in to GitHub** when prompted -- no manual
token needed.

If you prefer to use a token manually: open the Command Palette
(Ctrl+Shift+P), run **GitHub: Set Personal Access Token**, and paste
your token.

---

## Verify completion

Open your WSL terminal (or any terminal on macOS/Linux), navigate to
this activity's folder, and run:

```bash
python3 launch.py
```

<details>
<summary>What is launch.py and how do I navigate to it?</summary>

`launch.py` is the verification script for this activity. It checks
that git is installed, your identity is configured, `gh` is installed,
and you are authenticated. When everything passes it prints a
passphrase.

To navigate to the right folder:

```bash
cd ~/Downloads/env-setup-git
python3 launch.py
```

</details>

The script checks your setup and prints a passphrase when everything
passes. Submit that to record completion.

---

## TROUBLESHOOTING

### "git: command not found"

```bash
sudo apt install git
```

### git config values are empty

Run both config commands from Step 2. Make sure you are not using
placeholder text -- the name and email must be non-empty strings.

### "gh: command not found" after installation

Open a new terminal. If it is still missing, check that
`/usr/bin/gh` or `/usr/local/bin/gh` exists:

```bash
which gh
ls /usr/bin/gh /usr/local/bin/gh 2>/dev/null
```

If neither exists, re-run the installation commands from Step 4.

### gh auth login: browser does not open in WSL

Copy the URL printed to the terminal and open it manually in your
Windows browser. Paste the one-time code when prompted on the page.

Alternatively, use the token method from Step 5 to avoid the browser
flow entirely.

### IDE cannot push or pull even though WSL works

Your IDE may be running on Windows natively and using the Windows `gh`
credential helper, which is separate from WSL's. Open PowerShell and
run `gh auth login` (or the token method) there as well.

### "gh auth status" shows "not logged in"

Re-run `gh auth login` and complete the browser flow. If authentication
appeared to succeed but status still fails, try:

```bash
gh auth logout
gh auth login
```

### Token expired in CLion

Go to **Settings > Version Control > GitHub**, remove the old account
entry, and add a new one with a freshly generated token from
https://github.com/settings/tokens.

---

## Learn more

> Reference material for when you start using git actively. No need
> to read this now.

### Essential git commands

| Command | What it does |
|---|---|
| `git init` | Create a new repository in the current directory |
| `git clone URL` | Download a repository from a URL |
| `git status` | Show which files have changed since the last commit |
| `git add FILE` | Stage a file (mark it to be included in the next commit) |
| `git add .` | Stage all changed files in the current directory |
| `git commit -m "message"` | Save a snapshot of staged changes with a description |
| `git push` | Upload your local commits to GitHub |
| `git pull` | Download and merge new commits from GitHub |
| `git log --oneline` | Show the commit history, one line per commit |
| `git diff` | Show what changed in unstaged files |
| `git branch` | List branches; `git branch NAME` creates one |
| `git switch NAME` | Switch to a branch |
| `git switch -c NAME` | Create and switch to a new branch |

### gh commands for common tasks

```bash
gh repo clone owner/repo        # clone a GitHub repo
gh repo create                  # create a new GitHub repo interactively
gh pr create                    # open a pull request for the current branch
gh pr list                      # list open pull requests
gh issue list                   # list open issues
```

### SSH key setup (manual alternative to gh auth login)

If you prefer SSH keys without using `gh auth login`:

```bash
# Generate a key (accept the default path)
ssh-keygen -t ed25519 -C "you@example.com"

# Start the SSH agent and add the key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Print the public key -- copy this entire line
cat ~/.ssh/id_ed25519.pub
```

Then: GitHub > Settings > SSH and GPG keys > New SSH key > paste the
public key.

Test the connection:

```bash
ssh -T git@github.com
```

You should see "Hi username! You've successfully authenticated."

<details>
<summary>What is a public/private key pair?</summary>

SSH uses asymmetric cryptography. You generate two mathematically
linked keys: a private key (stays on your machine, never shared) and
a public key (safe to give to anyone). GitHub stores your public key.
When you connect, your machine proves it holds the matching private
key by solving a cryptographic challenge, without ever transmitting
the private key itself. This is more secure than a password because
there is nothing to intercept -- the private key never leaves your
machine.

</details>

### What is .gitconfig?

`~/.gitconfig` is your global git configuration file. View it with:

```bash
cat ~/.gitconfig
```

It stores your name, email, preferred editor, aliases, and other
settings. Each git repository also has a local `.git/config` that
overrides global settings for that project.

### What is .git/?

Every git repository contains a hidden `.git/` directory at its root.
This is where git stores the full history, branch references,
configuration, and the staging area. You should never modify it
manually. Deleting it removes the entire history and makes the
directory a plain folder again (the files remain but git tracking is
gone).
