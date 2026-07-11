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

This course targets the **SFML 3.x** API -- the current release. The
graded SFML assignment (sfml-canvas) is built and tested against SFML
3, so that is the version to install. SFML 3 renamed and changed
several functions relative to the older 2.x line (for example,
`sf::Image::create(w, h, color)` became `img.resize({w, h}, color)`,
and pixel access takes a coordinate pair: `img.setPixel({x, y},
color)` instead of `img.setPixel(x, y, color)`).

<details>
<summary>I already have SFML 2.x installed -- can I still use it?</summary>

For this activity, yes: the verification program below only uses API
that is identical on both versions, so it passes on either. For the
graded sfml-canvas assignment, no -- that assignment is compiled
against SFML 3, so its functions must use the SFML 3 API. If your
package manager only offers 2.x, the assignment's README lists the
handful of 2.x-vs-3.x call differences so you can develop locally on
2.x and adjust, but the version you submit against is 3.x. When in
doubt, install SFML 3.

</details>

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

Ubuntu/Debian's `apt` package `libsfml-dev` currently installs SFML
**2.5.1**, not the SFML 3 this course targets. There are two options.

**Option A -- build SFML 3 from source (recommended).** This is the
reliable way to get SFML 3 on any Linux distribution. Install the build
tools and SFML's own dependencies, then compile and install it under
`/usr/local`:

```bash
sudo apt update
sudo apt install -y build-essential cmake git \
    libx11-dev libxrandr-dev libxcursor-dev libxi-dev \
    libudev-dev libgl1-mesa-dev libfreetype-dev \
    libopenal-dev libflac-dev libvorbis-dev

git clone --branch 3.0.0 --depth 1 https://github.com/SFML/SFML.git
cd SFML
cmake -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON
cmake --build build -j"$(nproc)"
sudo cmake --install build
sudo ldconfig          # refresh the dynamic-linker cache for /usr/local/lib
```

This installs the headers under `/usr/local/include/SFML` and the
libraries under `/usr/local/lib`.

**Option B -- use the apt SFML 2.5.1.** If you would rather not build
from source, `sudo apt install -y libsfml-dev` gets you SFML 2.5.1.
This activity's check still passes on it, but remember the graded
sfml-canvas assignment is compiled against SFML 3 -- see that
assignment's README for the 2.x-vs-3.x call differences.

Verify the headers are present (source build):
```bash
ls /usr/local/include/SFML
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
   and runs: it constructs an empty `sf::Image` and prints its size
   (`0 0`). This program deliberately uses only calls that are spelled
   the same on SFML 2 and 3, so the install check itself does not
   depend on which version you have.

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

### "no member named 'resize' in 'sf::Image'" (or similar)

This is a compiler error that means SFML installed, but as the older
version 2.x instead of the 3.x this course targets. SFML 3 renamed
several functions; the 2.x `sf::Image::create(w, h, color)` became
`img.resize({w, h}, color)`, and `setPixel`/`getPixel` now take a
coordinate pair (`{x, y}`) instead of two separate arguments. Check
your installed version:

```bash
pkg-config --modversion sfml-graphics
# if that reports nothing for a source build, try:
PKG_CONFIG_PATH=/usr/local/lib/pkgconfig pkg-config --modversion sfml-graphics
```

If it reports `2.x`, install SFML 3 (on Linux, build from source per
Option A above; on macOS, current Homebrew installs SFML 3 directly).
You can develop against 2.x if you must -- the sfml-canvas README lists
the exact call differences -- but the graded build uses 3.x.

### g++ not found

Complete the [compiler activity](../env-setup-compiler/) before this
one; the verification script needs `g++` to compile the test program.
