# Activity: Install SFML

> **Activity 5 of 8**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
> - [2. Python](../env-setup-python/)
> - [3. Compiler](../env-setup-compiler/)
> - [4. Build Tools](../env-setup-build-tools/)
>
> Next: [6. IDE](../env-setup-ide/)

SFML (Simple and Fast Multimedia Library) is a C++ library for 2D
graphics, windows, audio, and input. The course project uses it, so
you need it installed and linkable before that assignment starts.

<details>
<summary>What is a media library?</summary>

A media library is a collection of pre-written code that handles
things your operating system can do but that C++'s standard library
does not cover on its own: opening a window, drawing shapes and
images to the screen, reading keyboard and mouse input, and playing
sound. Writing this from scratch means talking directly to the
operating system's graphics and audio APIs, which differ by platform.
SFML wraps all of that behind one consistent C++ interface that works
the same way on Linux, macOS, and Windows.

</details>

---

## Linux (Ubuntu / Debian -- including WSL)

```bash
sudo apt update
sudo apt install -y libsfml-dev
```

Verify the headers are present:
```bash
ls /usr/include/SFML
```

You should see directories like `Graphics`, `Window`, `Audio`, and
`System`.

---

## Linux (Fedora / RHEL / Rocky)

```bash
sudo dnf install SFML-devel
```

---

## Linux (Arch / Manjaro)

```bash
sudo pacman -S sfml
```

---

## macOS

```bash
brew install sfml
```

Homebrew installs SFML's headers under `/opt/homebrew/include` (Apple
Silicon) or `/usr/local/include` (Intel). Both are already on the
compiler's default search path once Homebrew is set up correctly (see
the shell activity).

---

## Windows -- use WSL (recommended)

Inside your WSL terminal:

```bash
sudo apt install -y libsfml-dev
```

This is the simplest and recommended approach for this course. Any
graphical window SFML opens from WSL requires WSLg (bundled with
recent Windows 11 WSL installs) or an X server; if you only need to
run this activity's verification script, no display is required.

---

## Windows -- native

1. Go to https://www.sfml-dev.org/download.php and download the SDK
   that matches your compiler **and its exact version**. SFML ships
   separate downloads per compiler (MinGW, Visual Studio) and per
   compiler version.
2. Extract the archive somewhere permanent, e.g. `C:\SFML`.
3. Configure your IDE or build system to add `C:\SFML\include` to the
   include path and `C:\SFML\lib` to the library path.

<details>
<summary>Why does the compiler version have to match?</summary>

SFML on Windows ships as prebuilt binary libraries, not source code you
compile yourself. Different compilers (MinGW vs. MSVC) and even
different versions of the same compiler lay out function calls and
data in memory in incompatible ways under the hood. A library built
for one compiler version usually will not link correctly against a
different one -- you will get confusing linker errors. This is the
classic pitfall on native Windows: always download the SFML build that
names your exact compiler and version. This is one of the reasons this
course recommends WSL, where a single `apt install` guarantees a
matching toolchain.

</details>

---

## Verify completion

Once SFML is installed, run the activity script. Open your terminal,
navigate to this activity's folder, and run:

```bash
python3 launch.py
```

The script checks two things:

1. That the SFML headers (`SFML/Graphics.hpp`) are present in a
   standard include path.
2. That a small real C++ program using SFML actually compiles, links,
   and runs: it creates a 2x2 red `sf::Image` and prints its size.

<details>
<summary>What does "compile, link, and run" mean here, and why check
all three?</summary>

Compiling turns your `.cpp` file into machine code, but that step only
needs the *headers* -- the declarations of SFML's classes and
functions. Linking is the separate step that stitches your compiled
code together with SFML's actual compiled implementation, supplied as
library files, using `-lsfml-graphics -lsfml-system` on the compiler
command line (each `-l<name>` flag tells the linker "find and include
the library named `<name>`"). Headers can be present while the
library files are missing, which compiles fine but fails to link. This
activity's script does both steps, then runs the resulting program, so
a pass means SFML is genuinely usable, not just partially installed.
(Whether that library file is linked directly into your program or
loaded separately at startup is the static-vs-dynamic linking
distinction -- covered later, in the Libraries topic.)

</details>

If `g++` is not found, complete the [compiler activity](../env-setup-compiler/)
first.

Follow the prompts. When the script succeeds it prints a passphrase --
submit that to record completion.

---

## TROUBLESHOOTING

### "undefined reference to `sf::Image::create...`" (or similar)

This is a linker error, not a compiler error -- the headers were found,
but the linker could not find SFML's compiled code. You are missing
one or more `-l` flags on the compile command, or the SFML library
files themselves are not installed. Make sure you installed the `-dev`
/ `-devel` package (which includes both headers and library files),
not just a runtime package.

### "cannot find -lsfml-graphics"

The SFML library files are not installed, or are not on the linker's
search path. Re-run the install command for your platform above. On
Linux, confirm the package installed with:
```bash
dpkg -L libsfml-dev | grep libsfml-graphics
```

### "SFML/Graphics.hpp: No such file or directory"

This is a compiler error -- the include path does not contain SFML's
headers. Confirm the package installed and that you are not pointing
your build at a different, older SFML you installed previously.

### g++ not found

Complete the [compiler activity](../env-setup-compiler/) before this
one; the verification script needs `g++` to compile the test program.
