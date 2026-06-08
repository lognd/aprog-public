# Activity: Get a Linux/Unix Shell

> **Activity 1 of 6 -- start here**
>
> Next: [2. Python](../env-setup-python/)

You need a Linux or macOS terminal before anything else in this course
will work. This activity walks you through getting one and verifies it
by having you run a small binary that prints a passphrase.

<details>
<summary>Why does this course require Linux/Unix?</summary>

<details>
<summary>History of Unix/POSIX/Linux (<i>for the nerds</i>)</summary>
Unix was created at Bell Labs in 1969. Its design -- small programs
that do one thing, composable via pipes, a hierarchical filesystem,
and a unified "everything is a file" interface -- proved so effective
that it became the blueprint for nearly every operating system that
followed. In 1991, Linus Torvalds wrote the Linux kernel as a free,
open-source reimplementation of Unix ideas; combined with the GNU
project's userland tools (gcc, bash, coreutils), it became the
dominant platform for servers, embedded systems, and cloud
infrastructure. macOS is built on Darwin, a direct descendant of BSD
Unix. POSIX (Portable Operating System Interface) is the IEEE standard
that codifies the Unix interface, which is why Linux and macOS share
the same commands and shell syntax despite having different kernels.
</details>
The standard toolchain for systems programming -- gcc, g++, make,
cmake, gdb, valgrind -- was designed for POSIX systems and works best
there. Windows has its own native toolchains (MSVC, MinGW), but they
behave differently in ways that would complicate course materials.
WSL2 gives you a full Linux kernel running alongside Windows, which is
the practical solution.

</details>

---

## Picking the right binary

Once you have a terminal set up, find the correct binary in the `bin/`
directory and run it. If it prints a passphrase, you are done.

| Your situation | Binary to run |
|---|---|
| Windows (most laptops, x86-64) -- inside WSL | `bin/linux-x86_64/shell-check` |
| Windows on ARM (Surface Pro X, Snapdragon) -- inside WSL | `bin/linux-aarch64/shell-check` |
| Linux x86-64, older distro with glibc errors | `bin/linux-x86_64-static/shell-check` |
| Raspberry Pi or other Linux ARM64 board | `bin/linux-aarch64/shell-check` |
| macOS (any Mac, Intel or Apple Silicon) | `bin/macos-universal/shell-check` |

If you run the Windows `.exe` directly it will tell you that you are
not in a Linux environment -- that is intentional.

---

## Option A: Windows -- WSL2

WSL2 (Windows Subsystem for Linux 2) runs a real Linux kernel inside
Windows. It is the recommended environment for this course on Windows.

<details>
<summary>What exactly is WSL2 and how does it work?</summary>

WSL2 uses Microsoft's Hyper-V hypervisor to run a lightweight virtual
machine containing the Linux kernel. Unlike WSL1 (which translated
Linux system calls to Windows ones), WSL2 runs real Linux kernel code.
Your Linux filesystem lives inside a virtual disk image (a `.vhdx`
file). The `wsl` command on Windows is a thin launcher that starts
that VM and attaches your terminal to it. Files in your Windows
filesystem are accessible from Linux at `/mnt/c/`, and vice versa.

</details>

### Minimum requirements

- Windows 10 version 2004 (Build 19041) or later, or Windows 11
- 64-bit x86 or ARM processor with virtualization support
- Virtualization enabled in BIOS/UEFI (see Troubleshooting if unsure)
- 4 GB RAM minimum (8 GB recommended)

### Step 1: Enable WSL

Open **PowerShell as Administrator** -- right-click the Start menu and
choose "Windows PowerShell (Admin)" or "Terminal (Admin)".

```powershell
wsl --install
```

<details>
<summary>What does this command do?</summary>

`wsl --install` does several things in one shot:

1. Enables the **Virtual Machine Platform** Windows feature, which
   exposes Hyper-V APIs needed to run a lightweight VM.
2. Enables the **Windows Subsystem for Linux** feature.
3. Downloads and installs the WSL2 Linux kernel from Microsoft's
   update servers.
4. Downloads and installs Ubuntu from the Microsoft Store as the
   default Linux distribution.

Before WSL existed, running Linux on Windows required a full virtual
machine (VMware, VirtualBox) with significant overhead. WSL2 achieves
near-native Linux performance with much lower resource usage.

</details>

Your computer will restart. After the restart, Ubuntu opens
automatically and asks you to choose a username and password.

**If the command is not found** (older Windows 10 without the WSL
package), run these two commands instead, then restart:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

<details>
<summary>What is dism.exe?</summary>

`dism.exe` is the **Deployment Image Servicing and Management** tool,
a Windows system utility for modifying the operating system image.
`/online` means "operate on the currently running Windows installation"
(as opposed to an offline image file). `/enable-feature` turns on an
optional Windows component. `/all` enables the feature and any
components it depends on. `/norestart` prevents an automatic immediate
restart so you can run both commands before rebooting once.

The two features being enabled are distinct:
- **Microsoft-Windows-Subsystem-Linux** installs the WSL subsystem
  itself -- the infrastructure that lets Linux processes run on Windows.
- **VirtualMachinePlatform** enables the Hyper-V virtual machine
  platform APIs that WSL2 needs to run a real Linux kernel in a
  lightweight VM.

Both are built into Windows 10/11 but are off by default to save
resources. The newer `wsl --install` command calls these same APIs
internally; the `dism.exe` route is just the older manual equivalent.

</details>

Then download and install the WSL2 kernel update from
`https://aka.ms/wsl2kernel`, then run:

```powershell
wsl --set-default-version 2
```

Then install Ubuntu from the Microsoft Store (search "Ubuntu").

### Step 2: Create your Linux user

Ubuntu prompts for a username and password. This is your account
inside the Linux environment -- it is separate from your Windows
account. Choose something you will remember.

<details>
<summary>Why a separate username?</summary>

WSL runs a real Linux user-space. Linux has its own user account
system distinct from Windows. The Linux `sudo` command (which grants
temporary administrator privileges for things like installing packages)
uses this Linux password, not your Windows password.

</details>

### Step 3: Open the WSL terminal

- Search "Ubuntu" in the Start menu, or
- Run `wsl` from any Command Prompt or PowerShell.

You should see a prompt like:

```
yourname@MACHINE:~$
```

The `~` is shorthand for your Linux home directory
(`/home/yourname`). You are now in a Linux shell.

### Step 4: Run the binary

Your Windows files are visible at `/mnt/c/Users/YourName/`. Navigate
to where you downloaded the activity files and run the binary:

```bash
cd /mnt/c/Users/YourName/Downloads/env-setup-shell
chmod +x bin/linux-x86_64/shell-check
./bin/linux-x86_64/shell-check
```

Replace `YourName` with your actual Windows username.

> **Tip -- tab completion:** After typing a few characters of a path
> or filename, press Tab and the shell completes it for you. If
> nothing happens, press Tab twice to see all matching options. Use
> this constantly -- it saves typing and prevents typos.

> **Tip -- paste into the terminal:** Right-click pastes in most
> terminals. If that does not work, try Ctrl+Shift+V (Linux/WSL
> terminals) or Ctrl+V (Windows Terminal).

<details>
<summary>What does cd do, and why is there a ./ before the filename?</summary>

`cd` stands for "change directory." The shell always has a current
working directory -- the folder it is "inside" right now. When you
type a filename without a path, the shell looks for it relative to
that directory. `cd /mnt/c/Users/YourName/Downloads/env-setup-shell`
moves the shell into that folder, so subsequent commands run there.

The `./` prefix means "in the current directory." When you type a
bare name like `shell-check`, the shell does NOT search the current
directory -- it only searches the directories listed in PATH. Adding
`./` explicitly tells it "run this file right here, not something from
PATH." This is a deliberate safety feature: it prevents a malicious
file named `ls` or `cd` in the current folder from silently replacing
a system command.

</details>

<details>
<summary>What does chmod +x do?</summary>

Linux tracks, for every file, whether each user is permitted to read
it, write it, or execute it. A file downloaded from the internet
typically does not have the execute permission set. `chmod +x` sets
the execute bit, telling the kernel that this file is allowed to be
run as a program. Without it, the shell refuses to execute the file
even if it is a valid binary.

</details>

---

## Option B: macOS

macOS is a Unix-based OS (built on Darwin/BSD). The terminal is built
in and works out of the box.

### Step 1: Open Terminal

Press **Cmd + Space**, type "Terminal", and press Enter. Or find it
at Finder > Applications > Utilities > Terminal.

### Step 2: Run the binary

```bash
cd ~/Downloads/env-setup-shell
chmod +x bin/macos-universal/shell-check
./bin/macos-universal/shell-check
```

If macOS blocks the binary with "cannot be opened because the
developer cannot be verified":

```bash
xattr -d com.apple.quarantine bin/macos-universal/shell-check
./bin/macos-universal/shell-check
```

<details>
<summary>What is Gatekeeper and why does it block the binary?</summary>

macOS Gatekeeper checks downloaded executables for a developer
signature from Apple. Binaries distributed through the App Store or
signed with a paid Apple Developer certificate pass automatically.
Unsigned binaries downloaded from the internet are quarantined.

`xattr -d com.apple.quarantine` removes the quarantine extended
attribute that macOS attached to the file when you downloaded it.
After removal, Gatekeeper no longer blocks it.

The `macos-universal` binary contains two compiled slices in one file
-- one for x86_64 (Intel Macs) and one for arm64 (Apple Silicon).
macOS's `lipo` tool combines them and the OS picks the right one at
runtime.

</details>

---

## Option C: Native Linux

Open your terminal emulator and run:

```bash
chmod +x bin/linux-x86_64/shell-check
./bin/linux-x86_64/shell-check
```

`chmod +x` sets the execute permission on the file -- see the
explanation in the WSL section above for details on why this is
necessary.

Use `linux-aarch64` on ARM hardware (`uname -m` tells you your
architecture). If you get a glibc version error on an older distro,
use the static binary:

```bash
chmod +x bin/linux-x86_64-static/shell-check
./bin/linux-x86_64-static/shell-check
```

<details>
<summary>What is glibc and why does the static binary avoid it?</summary>

The GNU C Library (glibc) is the standard C runtime on Linux. When
you compile a program dynamically (the default), it links against the
system's glibc at runtime. If the binary was compiled against a newer
glibc than what your system has, it refuses to run.

A statically linked binary embeds a copy of all needed library code
directly into the executable. It has no runtime dependencies and runs
on any Linux system of the right architecture, regardless of glibc
version. The tradeoff is a larger file size.

</details>

---

## Understanding PATH

PATH is an environment variable that lists the directories your shell
searches when you type a command name. When you type `gcc`, the shell
walks through each directory in PATH, in order, until it finds an
executable named `gcc`, then runs it.

```bash
echo $PATH
# example output:
# /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Entries are separated by `:` on Linux/macOS (`;` on Windows). The
shell searches left to right and uses the first match.

**Why this matters for this course**: later activities install tools
like `g++`, `cmake`, `python3`, `pip`, and `black`. If the directory
containing those executables is not in PATH, commands like
`g++ --version` fail with "command not found" even though the program
is installed.

**Adding `~/.local/bin` to PATH permanently:**

Many tools (pip, pipx) install user-local executables into
`~/.local/bin`. This directory is often not in the default PATH on a
fresh Linux install.

For bash (default on Ubuntu/WSL):
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For zsh (default on macOS):
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

`$HOME` expands to your home directory (e.g., `/home/yourname`), so
`$HOME/.local/bin` resolves to `/home/yourname/.local/bin`.

<details>
<summary>What is .bashrc and why do we write to it?</summary>

`.bashrc` is a shell script that bash runs automatically every time
you open a new interactive terminal session. It lives in your home
directory (the `.` prefix makes it a hidden file on Unix -- `ls -a`
shows hidden files). It is the standard place to put configuration
that should apply to every terminal you open: PATH modifications,
aliases, prompt customization, and so on.

`>>` appends a line to the file without overwriting it. `>` would
overwrite, which would destroy your existing configuration.

`source ~/.bashrc` (or equivalently `. ~/.bashrc`) runs the file in
the current shell session right now, without opening a new terminal.
Without `source`, the change would only take effect the next time you
open a new terminal.

`.zprofile` is the zsh equivalent for login shells (the kind macOS
Terminal opens). zsh has several config files with subtly different
loading rules; `.zprofile` is the right one for PATH on macOS.

</details>

<details>
<summary>What does export do?</summary>

In bash and zsh, a variable assignment like `PATH="..."` sets the
variable only in the current shell process. Child processes -- programs
you run from that shell, including your compiler, your IDE's terminal,
and subprocess calls within scripts -- do not inherit it.

`export` marks the variable to be copied into the environment of every
child process spawned from this shell. The environment is a set of
key-value pairs that the operating system passes to a new process when
it is created (via the `execve` system call). Programs read their
environment at startup using `getenv()` in C or `os.environ` in
Python. Without `export PATH`, a child process like `gcc` would not
know where to look for executables and libraries.

You can see the full exported environment with `env` or `printenv`.

</details>

**On Windows**: installer GUIs often show a checkbox labeled "Add to
PATH" during installation. Always check it. It does the same thing as
the commands above but writes to the Windows registry instead of a
shell config file.

---

## TROUBLESHOOTING

### WSL: "Please enable the Virtual Machine Platform Windows feature"

Run in PowerShell as Administrator, then restart:

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

This works on Windows 10 Home, Pro, and Enterprise. Windows 10 Home
does not have full Hyper-V but does support the Virtual Machine
Platform feature that WSL2 needs.

### WSL: "Virtualization is not enabled in BIOS" or error 0x80370102

Your CPU supports virtualization but it is disabled in firmware.
Restart your computer and enter the BIOS/UEFI setup:

- The key to press during boot varies: Delete, F2, F10, or F12 are
  common. The manufacturer name and key are usually shown briefly at
  the bottom of the screen during boot.
- Navigate to the CPU or Advanced section.
- **Intel CPUs**: enable "Intel Virtualization Technology (VT-x)"
- **AMD CPUs**: enable "AMD-V" or "SVM Mode"
- Save and exit.

If you cannot find this setting or cannot access your BIOS, contact
your instructor.

### WSL: install times out or gives HTTP errors

Try a different network (mobile hotspot works well). Or install just
the WSL infrastructure without a distribution, then add Ubuntu from
the Store separately:

```powershell
wsl --install --no-distribution
```

### WSL: terminal opens and immediately closes

Usually a VPN or antivirus interfering with the WSL network stack.
Disable your VPN temporarily. If that fixes it, add a WSL exclusion
in your VPN software.

### macOS: "Operation not permitted" running the binary

```bash
xattr -d com.apple.quarantine bin/macos-universal/shell-check
```

### macOS: "Bad CPU type in executable"

Use the `macos-universal` binary, not a Linux binary. The universal
binary contains both x86_64 and arm64 slices and works on all Macs.

### Linux: "GLIBC_2.XX not found"

Use `bin/linux-x86_64-static/shell-check`. It has no glibc dependency.
