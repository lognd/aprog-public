# Activity: Install CMake and Make

> **Activity 4 of 6**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
> - [2. Python](../env-setup-python/)
>
> Next: [5. IDE](../env-setup-ide/)

CMake and Make are the build system tools used throughout this course.
CMake generates build files from a high-level description of your
project; Make reads those files and runs the compiler to produce your
program. You need both.

---

## What these tools do

### Make

Make reads a `Makefile` and runs commands to build targets. When you
run `make`, it checks which source files have changed since the last
build and recompiles only what is necessary.

```makefile
# Minimal Makefile example
hello: hello.cpp
    g++ hello.cpp -o hello
```

```bash
make        # builds the 'hello' target
make clean  # if you define a 'clean' target
```

Make has been around since 1976. It is simple but can become complex
for large projects, which is why CMake exists.

### CMake

CMake is a build system generator. You write a `CMakeLists.txt` that
describes your project at a high level, and CMake generates the actual
build files for your platform (Makefiles on Linux/macOS, Visual Studio
projects on Windows, Ninja build files, etc.).

```cmake
# Minimal CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(Hello)
add_executable(hello hello.cpp)
```

You will be using this to build many of your more complicated projects.

---

## Linux (Ubuntu / Debian -- including WSL)

```bash
sudo apt update
sudo apt install -y cmake make
```

Verify:
```bash
cmake --version
make --version
```

Ubuntu 22.04 ships CMake 3.22. Ubuntu 24.04 ships CMake 3.28. The
course requires CMake 3.14 or later.

---

## Linux (Fedora / RHEL / Rocky)

```bash
sudo dnf install cmake make
```

---

## Linux (Arch / Manjaro)

```bash
sudo pacman -S cmake make
```

---

## macOS

### Option 1: Homebrew (recommended)

```bash
brew install cmake make
```

Homebrew's `make` is installed as `gmake` to avoid shadowing the system
`make`. Add an alias if you prefer the `make` name:

```bash
echo 'alias make=gmake' >> ~/.zprofile
```

<details>
<summary>What is an alias?</summary>

An alias is a shell shortcut: when you type the alias name, the shell
substitutes the command you mapped it to before running anything.
`alias make=gmake` makes typing `make` behave exactly as if you had
typed `gmake`. Aliases defined in `.zprofile` or `.bashrc` are
available in every new terminal you open. They are local to your shell
-- no other program sees them, and they do not create actual files on
disk.

</details>

### Option 2: CMake official installer

Download the macOS `.dmg` from https://cmake.org/download/ and install.
The installer offers to add cmake to PATH -- select that option.

---

## Windows -- use WSL (recommended)

Inside your WSL terminal:

```bash
sudo apt install -y cmake make
```

This is the simplest and recommended approach for this course.

---

## Windows -- native (MSYS2)

If you set up MinGW-w64 via MSYS2 in the compiler activity, open the
MSYS2 UCRT64 terminal and run:

```
pacman -S cmake make
```

If you installed cmake separately, add `C:\msys64\ucrt64\bin` to your
Windows PATH (see the compiler activity for PATH instructions).

---

## Windows -- native CMake installer

1. Download the `.msi` installer from https://cmake.org/download/
2. Run it. On the "Install Options" page, select
   **"Add CMake to the system PATH for all users"** (or current user).
3. Open a new Command Prompt and run `cmake --version` to verify.

`make` is not natively available on Windows. Use `cmake --build` instead
of `make` when building CMake projects on Windows:

```
cmake -B build -G "NMake Makefiles"
cmake --build build
```

<details>
<summary>What does the -G flag do?</summary>

`-G` selects the build system generator -- the format of files CMake
produces. By default on Linux CMake writes Makefiles; on Windows it
writes Visual Studio project files. `-G "NMake Makefiles"` tells CMake
to produce NMake-compatible Makefiles instead, which work with
Microsoft's `nmake.exe` build tool. `-G Ninja` produces Ninja build
files. The generated files are an implementation detail you rarely
look at directly; `cmake --build` runs them for you regardless of
which generator was used.

</details>

---

## Verify completion

Once `cmake --version` and `make --version` both print output, run
the activity script. Open your WSL terminal (or any terminal on
macOS/Linux), navigate to this activity's folder, and run:

```bash
python3 launch.py
```

<details>
<summary>What is launch.py and how do I navigate to it?</summary>

`launch.py` is a verification script included with this activity.
`python3` is the Python interpreter -- the program that reads and runs
Python source files. The script checks that CMake and Make are
installed and working, then prints a passphrase when everything passes.

To get to the right folder, use `cd` (change directory). For example:

```bash
cd ~/Downloads/env-setup-build-tools
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

### "cmake: command not found" after installation

Check your PATH:
```bash
which cmake
echo $PATH
```

On macOS with Homebrew on Apple Silicon, cmake is in `/opt/homebrew/bin`.
That directory must be on your PATH. See the shell activity for how to
add it.

### "CMake Error: your CXX compiler ... is not able to compile"

CMake cannot find g++. Make sure you completed the compiler activity
first and that `g++ --version` works.

### "make: *** No rule to make target"

You are trying to run `make` in the wrong directory, or the Makefile
has not been generated yet. Run `cmake -B build` first, then run make
inside the build directory:

```bash
cmake -B build
cmake --build build
# or equivalently:
cmake -B build
cd build && make
```

### "CMake 3.XX or higher is required"

Your CMake is too old. Check your version:
```bash
cmake --version
```

Install a newer version:
- Ubuntu/WSL: add the Kitware APT repository:
  ```bash
  wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc \
    | sudo apt-key add -
  sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ focal main'
  sudo apt update
  sudo apt install cmake
  ```
- macOS: `brew upgrade cmake`

### "CMake Error: The source directory ... does not exist"

Run cmake from the correct parent directory. If your project is at
`~/cs-101/hw1/`, run:
```bash
cd ~/cs-101/hw1
cmake -B build
```

### Windows: "cl is not recognized as an internal or external command"

You need to open a "Developer Command Prompt for VS" rather than a
regular Command Prompt. Search "Developer Command Prompt" in the
Start menu.

### MSYS2: cmake opens the wrong generator

In the MSYS2 UCRT64 terminal, explicitly specify the MinGW Makefiles
generator:
```bash
cmake -B build -G "MinGW Makefiles"
cmake --build build
```
