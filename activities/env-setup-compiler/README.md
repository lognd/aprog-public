# Activity: Install C/C++ Compilers

> **Activity 3 of 7**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
> - [2. Python](../env-setup-python/)
>
> Next: [4. Build Tools](../env-setup-build-tools/)

This course uses C and C++. You need two compiler families installed:
**GCC/G++** (the GNU Compiler Collection) and **Clang/Clang++** (the
LLVM compiler). Both are industry-standard and free.

<details>
<summary>What is a compiler and why do you need two?</summary>

A compiler is a program that reads your source code (text in `.c` or
`.cpp` files) and translates it into machine code -- the binary
instructions that your CPU can execute directly. Without a compiler,
your source files are just text; they cannot run.

**GCC** (the `gcc` and `g++` executables) is the GNU Compiler
Collection. It has been the dominant Linux compiler for decades and is
what most Linux distributions ship. `gcc` compiles C; `g++` compiles
C++ and links the C++ standard library.

**Clang** (the `clang` and `clang++` executables) is the LLVM
project's compiler. It produces high-quality diagnostic messages
("error: did you mean X?"), which makes it easier to understand
compiler errors. Many IDEs use `clangd` (the Clang language server)
for real-time error checking and autocompletion.

Having both installed lets you cross-check compiler behavior,
use the better diagnostics from Clang while submitting with GCC, and
run tools like `clang-tidy` and `clangd` that depend on the LLVM
toolchain. Most professional C++ shops use both.

</details>

---

## Linux (Ubuntu / Debian -- including WSL)

This is the primary environment for the course. WSL users: run all of
these commands inside the WSL terminal.

### Install GCC and G++

```bash
sudo apt update
sudo apt install -y build-essential
```

<details>
<summary>What is sudo, apt, and build-essential?</summary>

`sudo` ("superuser do") runs the following command as root -- the
Linux administrator account. Package installation writes files to
system directories like `/usr/bin/` and `/usr/lib/` that ordinary
users are not allowed to touch. `sudo` asks for your Linux password
(the one you set when creating your WSL user), then grants elevated
privileges for that one command only. It is much safer than logging
in as root permanently.

`apt` is the Advanced Package Tool, Debian/Ubuntu's package manager.
It downloads software from curated repositories hosted on Ubuntu's
servers, verifies their cryptographic signatures, and installs them
along with any dependencies. `apt update` refreshes the local list
of available packages -- it does not install anything, it just
synchronizes the index. `apt install` then reads from that index to
find and install what you asked for. The `-y` flag answers "yes"
automatically to any confirmation prompts.

`build-essential` is a meta-package -- a package that has no files of
its own but pulls in a set of others as dependencies. It installs:

- `gcc` -- the C compiler
- `g++` -- the C++ compiler
- `make` -- the build automation tool (covered in the next activity)
- `libc6-dev` -- C standard library headers such as `<stdio.h>` and
  `<stdlib.h>` that your code `#include`s

</details>

Verify the installation:

```bash
gcc --version
g++ --version
```

You should see output like `gcc (Ubuntu 13.x.x ...) 13.x.x`. The
exact version does not matter as long as it is GCC 11 or later.

### Install Clang

```bash
sudo apt install -y clang clangd clang-format clang-tidy
```

<details>
<summary>What are clangd, clang-format, and clang-tidy?</summary>

These are separate tools built on the LLVM/Clang infrastructure:

**clangd** is the Clang Language Server. It implements the Language
Server Protocol (LSP), which is a standard interface that IDEs and
editors use to request things like "what is the type of this
variable?", "go to the definition of this function", and "show me all
the errors in this file." Your IDE connects to `clangd` in the
background and displays its results. Without `clangd`, your IDE has
no way to understand your C++ code.

**clang-format** automatically reformats C/C++ source code to follow
a consistent style. You can configure it with a `.clang-format` file
in your project. IDEs can invoke it on save so you never have to
think about formatting.

**clang-tidy** is a static analysis tool -- it reads your code
without running it and reports potential bugs, style violations, and
dangerous patterns. It catches things like using a pointer after
freeing it or forgetting to initialize a variable.

</details>

Verify:

```bash
clang --version
clang++ --version
clangd --version
```

---

## Linux (Fedora / RHEL / Rocky)

```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install clang clang-tools-extra
```

---

## Linux (Arch / Manjaro)

```bash
sudo pacman -S base-devel clang
```

---

## macOS

### Install GCC and Clang (Xcode Command Line Tools)

```bash
xcode-select --install
```

A dialog appears. Click Install.

<details>
<summary>What does xcode-select --install actually install?</summary>

The Xcode Command Line Tools package includes:

- `clang` and `clang++` -- Apple's fork of Clang, aliased to `gcc`
  and `g++` on macOS. When you type `gcc` on macOS you are actually
  running Apple Clang.
- `make` -- GNU Make
- `git` -- version control
- Various UNIX utilities and header files

Apple maintains their own fork of Clang because Clang's permissive
BSD license lets them modify and redistribute it without open-sourcing
Apple-specific changes. The GNU GPL license that covers GCC does not
permit that.

For most of this course, Apple Clang behaves identically to upstream
Clang. If you need actual GNU GCC, install it via Homebrew below.

</details>

After installation, the `gcc` and `g++` commands on macOS point to
Apple Clang. Verify:

```bash
gcc --version    # will say "Apple clang version X.X.X"
clang --version
```

### Install GNU GCC via Homebrew

macOS's `gcc` is actually Clang under the hood. For actual GNU GCC:

```bash
brew install gcc
```

Homebrew installs it as `gcc-14` (or whichever version is current) to
avoid shadowing Apple's `gcc`. To compile with real GCC explicitly:

```bash
gcc-14 hello.c -o hello
g++-14 hello.cpp -o hello
```

### Install clang-format and clang-tidy

```bash
brew install llvm
```

This installs the full LLVM suite including `clang-format` and
`clang-tidy` as standalone executables. Add to PATH:

```bash
echo 'export PATH="$(brew --prefix llvm)/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

<details>
<summary>What does source do here, and what is $(brew --prefix llvm)?</summary>

`source ~/.zprofile` executes the file in the current shell session
immediately, without opening a new terminal. The shell config file
(`.zprofile`, `.bashrc`, etc.) is only read automatically when a new
session starts. `source` is how you apply a change you just made to
the file without logging out and back in.

`$(...)` is command substitution: the shell runs the command inside
and replaces the whole `$(...)` with its output before passing the
string to `echo`. `brew --prefix llvm` prints the directory where
Homebrew installed LLVM (e.g., `/opt/homebrew/opt/llvm`). So the
full expression expands to something like:
`export PATH="/opt/homebrew/opt/llvm/bin:$PATH"`.
This is better than hardcoding the path because it stays correct if
Homebrew's prefix changes (Intel vs Apple Silicon Macs install to
different locations).

</details>

---

## Windows -- use WSL (recommended)

Install inside your WSL terminal following the Linux instructions
above. This is the recommended path for this course.

### Windows native: MSYS2/MinGW-w64

If you need to build native Windows executables (not WSL):

1. Download the MSYS2 installer from https://www.msys2.org and run it.
   Accept the default install path (`C:\msys64`).
2. Open the **MSYS2 UCRT64** terminal from the Start menu.
3. Update the package database:
   ```
   pacman -Syu
   ```
   Close and reopen when prompted.
4. Install GCC and Clang:
   ```
   pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-clang
   ```
5. Add `C:\msys64\ucrt64\bin` to your Windows PATH:
   - Open Start > "Edit the system environment variables"
   - User Variables > Path > Edit > New > type `C:\msys64\ucrt64\bin`
   - Click OK all the way out, then open a new terminal.

<details>
<summary>What is MSYS2 and what is MinGW-w64?</summary>

**MSYS2** is a software distribution for Windows that provides a
Unix-like shell environment and a package manager (`pacman`, the same
one Arch Linux uses). It is the successor to MSYS and Cygwin.

**MinGW-w64** (Minimalist GNU for Windows, 64-bit) is a port of GCC
and associated GNU tools that produce native Windows executables (`.exe`
files that link against `MSVCRT.dll` or `ucrt.dll`, not a Unix
compatibility layer). The "UCRT64" environment links against the
Universal C Runtime, which is the modern Windows C runtime shipping
with Windows 10+.

When you compile with MinGW-w64 GCC, you get `.exe` files that run
without MSYS2 installed. This is different from Cygwin, where
executables require `cygwin1.dll` to run.

</details>

### Windows native: MSVC (cl.exe)

Microsoft's own compiler is included with Visual Studio:

1. Download Visual Studio Community (free) from
   https://visualstudio.microsoft.com
2. Select the "Desktop development with C++" workload.
3. Open a "Developer Command Prompt for VS" from the Start menu.
   `cl.exe` is now on PATH in that terminal.

<details>
<summary>Why is cl.exe not the same as gcc?</summary>

`cl.exe` uses different command-line flags than GCC/Clang. For
example, GCC uses `-O2` for optimization; MSVC uses `/O2`. GCC uses
`-Wall` for warnings; MSVC uses `/W4`. CMake handles most of these
differences automatically when it detects which compiler it is using,
but you will see different flag syntax in error messages and build
logs.

The course materials and autograder use GCC on Linux. MSVC is an
alternative if you cannot use WSL, but you may encounter
compatibility differences.

</details>

---

## Verify completion

Once `gcc`, `g++`, `clang`, and `clang++` all respond to `--version`,
run the activity script. Open your WSL terminal (or any terminal on
macOS/Linux), navigate to this activity's folder, and run:

```bash
python3 launch.py
```

<details>
<summary>What is launch.py and how do I navigate to it?</summary>

`launch.py` is a verification script included with this activity.
`python3` is the Python interpreter -- the program that reads and runs
Python source files. The script checks that both compiler families are
installed and working, then prints a passphrase when everything passes.

To get to the right folder, use `cd` (change directory). For example:

```bash
cd ~/Downloads/env-setup-compiler
python3 launch.py
```

`~` is shorthand for your home directory. If you are not sure where
the activity files are, drag the folder into the terminal to paste
its path.

</details>

Follow the prompts. When the script succeeds it prints a passphrase --
submit that to record completion.

---

## TROUBLESHOOTING

### "gcc: command not found" after installation

Check that the install directory is in PATH:

```bash
which gcc
echo $PATH
```

On Ubuntu/WSL, gcc goes to `/usr/bin/gcc` which is always in PATH.
On macOS with Homebrew on Apple Silicon, Homebrew installs to
`/opt/homebrew/bin` -- add it to PATH as shown in the shell activity.

### "g++: No such file or directory" on Ubuntu

You may have installed `gcc` alone. Run:

```bash
sudo apt install g++
```

or reinstall the whole `build-essential` package.

### "clangd: command not found" after installation

```bash
sudo apt install clangd
```

On some Ubuntu versions the package is `clang-14` and the binary is
`clangd-14`. Create a symlink:

```bash
sudo ln -sf /usr/bin/clangd-14 /usr/local/bin/clangd
```

### macOS: "xcrun: error: invalid active developer path"

```bash
sudo xcode-select --reset
xcode-select --install
```

### MSYS2: "gcc: command not found" in UCRT64 terminal

Make sure you opened "MSYS2 UCRT64" (not "MSYS2 MSYS"). Also verify
`C:\msys64\ucrt64\bin` is in your Windows PATH and that you opened a
new terminal after adding it.
