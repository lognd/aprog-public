# Activity: Install and Configure an IDE

> **Activity 5 of 7**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
> - [2. Python](../env-setup-python/)
> - [3. Compiler](../env-setup-compiler/)
> - [4. Build Tools](../env-setup-build-tools/)
>
> Next: [6. Discord](../env-setup-discord/)

An IDE (Integrated Development Environment) is the program you write
code in. It combines a code editor, real-time error checking, and a
debugger into one tool.

<details>
<summary>What makes an IDE different from a text editor?</summary>

A text editor shows you text. An IDE understands your code:

- **Inline errors**: red underlines appear on mistakes within seconds,
  without you having to run the compiler.
- **Autocompletion**: the IDE knows the methods on every class and
  suggests them as you type.
- **Go to definition**: Ctrl+click on a function to jump to where it
  is defined.
- **Integrated debugger**: pause your program at any line and inspect
  the values of every variable.

For C++, this works because the IDE runs `clangd` in the background --
the same Clang language server you installed in the compiler activity.
It continuously parses your code and answers the IDE's questions.

</details>

The supported options are:

| IDE | Language | Notes |
|---|---|---|
| **CLion** (recommended) | C/C++ | From JetBrains; free |
| **PyCharm** (recommended) | Python | From JetBrains; free; unified product |
| **VS Code** | Both | Lightweight; free; needs extensions |
| **Neovim** | Both | Terminal-only; steep learning curve |

**Install both CLion and PyCharm** if you want separate dedicated IDEs
for each language. Use VS Code if you prefer one window for everything.

---

## JetBrains IDEs: CLion and PyCharm

CLion is a dedicated C/C++ IDE. PyCharm is a dedicated Python IDE.
Both are made by JetBrains and are free. PyCharm is a unified product
-- one download, no license or student account required. CLion is free
for non-commercial use; if it asks for a license at startup, choose
"Start a free trial" or sign in with a free JetBrains account.

Install guides: [CLion](https://www.jetbrains.com/help/clion/installation-guide.html) --
[PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html)

FAQs: [CLion](https://www.jetbrains.com/clion/faq/) --
[PyCharm](https://www.jetbrains.com/pycharm/faq/)

### Install via JetBrains Toolbox

Toolbox is a small launcher app that installs and updates JetBrains
IDEs. Install it first; then use it to install the IDEs.

1. Download Toolbox from https://www.jetbrains.com/toolbox-app/
2. Run the installer for your platform.
   - **Windows**: run the `.exe`.
   - **macOS**: open the `.dmg` and drag Toolbox to Applications.
   - **Linux**: extract the `.tar.gz` and run `jetbrains-toolbox`
     inside it. It installs itself automatically.
3. Open Toolbox. It appears as a small icon in your system tray.
4. Find **CLion** in the list and click **Install**.
5. Find **PyCharm** and click **Install**.

---

## CLion setup

### Step 1: Configure the toolchain

A toolchain is the set of compiler and debugger binaries CLion uses
to build and debug your code. Before CLion can build anything, it
needs to know where those binaries are.

Open CLion. From the Welcome screen or inside a project, open:

**Settings** (Ctrl+Alt+S on Linux/Windows, Cmd+, on macOS)
**> Build, Execution, Deployment > Toolchains**

#### Linux or macOS

CLion usually detects the toolchain automatically. Check that each
field shows a green checkmark. Expected paths on Ubuntu/WSL:

| Field | Expected path |
|---|---|
| C Compiler | `/usr/bin/gcc` |
| C++ Compiler | `/usr/bin/g++` |
| Debugger | `/usr/bin/gdb` |

If any field shows red: click the folder icon next to it, navigate
to `/usr/bin/`, and select the correct binary.

#### Windows -- connect to WSL

Run the IDE on Windows but compile inside Linux:

1. In Toolchains, click **+** > **WSL**.
2. CLion detects your WSL distribution. Select it (usually Ubuntu).
3. Wait for CLion to connect and populate the fields automatically.
   If any field is not found, set the paths using the table above.
4. Drag the WSL entry to the **top** of the list.

<details>
<summary>How does CLion talk to WSL?</summary>

CLion connects to WSL over a local socket. Your source files live on
the Windows side; CLion sends build and debug commands to WSL, which
runs them and sends results back. The IDE window stays on Windows.
This gives you native Linux compilation without leaving your Windows
desktop.

</details>

### Step 2: Open a project

**File > Open** and select the folder that contains your
`CMakeLists.txt`. CLion reads that file (the project description
used by CMake, the course build system) and configures itself
automatically. After a moment the build targets appear in the toolbar.

### Step 3: Verify it works

Create `hello.cpp` in the project:

```cpp
#include <iostream>
int main() {
    std::cout << "hello\n";
}
```

1. Hover over `std::cout`. A tooltip with its type should appear
   within a second or two -- this confirms clangd is running.
2. Press **Shift+F10** (or the green run triangle). An output panel
   opens and shows `hello`.
3. Click in the left gutter (the line number by the source code) 
   next to the `std::cout` line. A red octagon (breakpoint) 
   appears. Press **Shift+F9**. The program pauses at
   that line and the Debug panel shows your variables.

---

## PyCharm setup

### Step 1: Configure the Python interpreter

The interpreter is the Python executable PyCharm uses to run your
code and power autocompletion. You have to point PyCharm at the
right one before it will work correctly.

<details>
<summary>Why does the interpreter need to be set explicitly?</summary>

Multiple Python installations can coexist on one machine (the system
Python, a Homebrew Python, virtual environments, the WSL Python, etc.),
each with its own set of installed packages. PyCharm needs to know
exactly which one your project uses. If the wrong one is selected,
imports look broken in the IDE even though they work in the terminal.

</details>

1. Open or create a project in PyCharm.
2. Open **Settings > Project: [name] > Python Interpreter**.
3. Click the dropdown or the gear icon to its right.
4. Click **Add New Interpreter > Add Local Interpreter...**
5. Choose **System Interpreter**, then click the `...` button to
   browse to the Python executable.
   - Linux/WSL: usually `/usr/bin/python3`
   - macOS: `/opt/homebrew/bin/python3` (if installed via Homebrew)

**Windows/WSL users**: instead of "Add Local Interpreter", choose
**On WSL...** PyCharm will detect your WSL distribution and list the
Python installations inside it. Select `/usr/bin/python3`.

<details>
<summary>How does PyCharm run code inside WSL?</summary>

PyCharm connects to WSL over a local socket and runs Python inside
Linux while keeping its GUI window on Windows. When you press run,
the code actually executes in WSL. This matches what happens when you
run the same code in your WSL terminal.

</details>

Click **OK**. PyCharm indexes the interpreter -- this takes about
10-30 seconds. When it finishes, you should see the five course tools
(black, ruff, mypy, pytest, isort) listed in the packages panel.

### Step 2: Verify it works

Create `hello.py`:

```python
def greet(name: str) -> str:
    return f"hello, {name}"

print(greet("world"))
```

1. Press **Shift+F10** (or the run triangle). The output panel shows
   `hello, world`.
2. Change `greet("world")` to `greet(42)`. PyCharm should underline
   the argument within a few seconds -- this confirms type checking
   is working.

---

## VS Code setup

VS Code is a lightweight, extensible code editor. It handles both C++
and Python in one window, using extensions to add language support.

Install guides and documentation:
- [C++ in VS Code](https://code.visualstudio.com/docs/languages/cpp)
- [Python in VS Code](https://code.visualstudio.com/docs/languages/python)
- [WSL development in VS Code](https://code.visualstudio.com/docs/remote/wsl)

### Step 1: Install VS Code

- **Windows**: download from https://code.visualstudio.com and run
  the installer. Check **"Add to PATH"** so you can type `code .`
  in a terminal to open a folder.
- **macOS**: download the `.dmg`, drag to Applications. Then open VS
  Code, press Cmd+Shift+P, and run
  "Shell Command: Install 'code' command in PATH".
- **Linux**: download the `.deb` and run:

```bash
sudo dpkg -i code_*.deb
```

<details>
<summary>What is dpkg -i?</summary>

`dpkg` is Debian/Ubuntu's package installer for `.deb` files.
`-i` means install. `sudo` is needed because installing writes to
system directories. The `*` in `code_*.deb` is a shell wildcard that
matches whatever the actual filename is (the version number changes).
If you get dependency errors, run `sudo apt install -f` afterward.

</details>

> **WSL users**: install VS Code on **Windows**, not inside WSL. The
> Remote-WSL extension (installed next) connects VS Code back to WSL
> automatically.

### Step 2: Install extensions

Extensions add the language support that makes VS Code useful. Open
the Extensions panel (Ctrl+Shift+X) and install these:

| Extension | What it does |
|---|---|
| **clangd** (LLVM) | C++ errors, autocompletion, and go-to-definition using the clangd language server |
| **CMake Tools** (Microsoft) | Run CMake configure and build steps from inside VS Code |
| **Remote - WSL** (Microsoft) | Connects VS Code on Windows to your WSL Linux environment |
| **Python** (Microsoft) | Python language support, test runner, debugger integration |
| **Ruff** (Astral) | Runs the Ruff linter and formatter you installed in the Python activity |
| **Pylance** (Microsoft) | Fast Python type checking and IntelliSense |

> When you install clangd, VS Code will ask you to disable the
> built-in C/C++ IntelliSense. Agree -- they conflict and clangd is
> more accurate.

To install all at once from the terminal:

```bash
code --install-extension llvm-vs-code-extensions.vscode-clangd
code --install-extension ms-vscode.cmake-tools
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-python.python
code --install-extension charliermarsh.ruff
code --install-extension ms-python.vscode-pylance
```

### Step 3: Set the Python interpreter

1. Open any `.py` file.
2. Click the Python version shown in the bottom status bar, or press
   Ctrl+Shift+P and run **"Python: Select Interpreter"**.
3. Pick the correct Python from the list. WSL users using Remote-WSL
   will see the WSL Python automatically.

### Step 4: Verify it works

1. Open a `.cpp` file. Hover over `std::cout` -- a tooltip should
   appear within a couple of seconds.
2. Open a `.py` file. Type `def f(x: int) -> str: return x` --
   Pylance should underline the return value as a type error.
3. In the CMake Tools panel (CMake icon in the left sidebar), click
   **Configure**, then **Build**.

---

## Neovim setup

Neovim is a terminal-based modal text editor. It takes more setup
than the GUI options but runs entirely in the terminal and works well
on remote machines.

### Step 1: Install Neovim

**Linux / WSL**:

```bash
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage
chmod +x nvim-linux-x86_64.appimage
sudo mv nvim-linux-x86_64.appimage /usr/local/bin/nvim
```

<details>
<summary>What do these commands do?</summary>

`curl -LO` downloads a file from a URL. `-L` follows redirects
(GitHub download links redirect to the real file); `-O` saves it
using the filename from the URL.

The file is an AppImage -- a self-contained Linux application bundled
into a single executable. It runs on any Linux distribution without
installation. `chmod +x` sets the execute permission on it. Moving it
to `/usr/local/bin/` (the standard directory for manually installed
programs) makes `nvim` available as a command from any directory.

</details>

**macOS**:

```bash
brew install neovim
```

### Step 2: Configure with LazyVim

LazyVim (https://www.lazyvim.org) is a complete Neovim configuration
that sets up plugins, keybindings, and language servers automatically.

```bash
mv ~/.config/nvim ~/.config/nvim.bak 2>/dev/null || true
git clone https://github.com/LazyVim/starter ~/.config/nvim
rm -rf ~/.config/nvim/.git
```

<details>
<summary>What do these commands do?</summary>

`mv ~/.config/nvim ~/.config/nvim.bak 2>/dev/null || true` renames
any existing Neovim config to `.bak` as a backup, suppressing any
error if there was nothing to move.

`git clone URL PATH` downloads a git repository to a local directory.
Git tracks the full history of changes to a set of files. Here it
downloads the LazyVim starter configuration into `~/.config/nvim/`,
where Neovim looks for its config.

`rm -rf ~/.config/nvim/.git` removes the git history from the clone
so the config becomes a standalone directory you own rather than a
tracked copy of the LazyVim starter.

</details>

Open Neovim. Plugins install automatically on the first launch:

```bash
nvim
```

Enable C++ and Python language servers inside Neovim:
- Press `:`, type `LazyExtras`, and press Enter.
- Find `lang.clangd`, press `x` to enable it.
- Find `lang.python`, press `x` to enable it.
- Press `q`, then restart Neovim. Language servers install
  automatically.

### Step 3: Verify it works

```bash
nvim hello.cpp
```

In normal mode, move the cursor over a symbol and press `K`. A
documentation popup should appear. Press `gd` on any symbol to jump
to its definition.

---

## Verify completion

Once you have an IDE set up and the verify steps above pass, run the
activity script. Open your terminal (WSL terminal on Windows),
navigate to this activity's folder, and run:

```bash
python3 launch.py
```

<details>
<summary>What is launch.py and how do I navigate to it?</summary>

`launch.py` is the verification script included with this activity.
`python3` is the Python interpreter -- the program that reads and
runs Python source files. Running this command executes the script,
which checks your setup and prints a passphrase when everything
passes.

To navigate to the right folder, use `cd` (change directory). For
example, if you downloaded the activity files to your Downloads
folder:

```bash
cd ~/Downloads/env-setup-ide
python3 launch.py
```

`~` is shorthand for your home directory. If you are not sure where
the files are, you can drag the folder into the terminal window to
paste its path.

</details>

Follow any prompts the script shows. When it succeeds it prints a
passphrase -- submit that to record completion.

---

## TROUBLESHOOTING

### CLion: toolchain fields show red or "Not found"

**Settings > Build, Execution, Deployment > Toolchains > Auto-detect**.
If that does not help, click the folder icon next to each red field
and set the path manually. On Ubuntu/WSL: gcc is at `/usr/bin/gcc`,
g++ at `/usr/bin/g++`, gdb at `/usr/bin/gdb`.

### CLion: WSL toolchain shows "Cannot connect"

WSL must already be running when CLion tries to connect. Open a WSL
terminal window first, wait for the prompt to appear, then return to
CLion and click **Test Connection**.

### CLion: code analysis shows errors but the code compiles fine

Try in order:
1. **Tools > CMake > Reset Cache and Reload Project**
2. **File > Invalidate Caches > Invalidate and Restart**

### PyCharm: "No Python interpreter configured"

Open **Settings > Project > Python Interpreter** and add one. Follow
the interpreter setup steps above.

### PyCharm: pip packages are installed but PyCharm cannot find them

The packages were probably installed into a different Python than the
one PyCharm is using. In the terminal, run `which python3` and
`which pip3` -- they should point to the same path. Check that
PyCharm's interpreter matches that path.

### VS Code: clangd shows errors on standard headers

```bash
sudo apt install libstdc++-dev build-essential
```

You may also need to generate `compile_commands.json` -- see the
Learn More section below.

### VS Code: clangd is stuck showing stale errors

Ctrl+Shift+P > **"clangd: Restart Language Server"**

### VS Code: "code: command not found" inside WSL

In VS Code on Windows, press Ctrl+Shift+P and run
"Shell Command: Install 'code' command in PATH". Then open a new
terminal.

### Neovim: AppImage fails with "AppImages require FUSE"

```bash
sudo apt install libfuse2
```

---

## Learn more

> These are things you will encounter as the course progresses. There
> is no need to read this now -- come back when a specific situation
> sends you here.

### CMake in CLion: refreshing after changes to CMakeLists.txt

**Soft reload** -- picks up most changes without deleting anything:
right-click `CMakeLists.txt` in the Project panel and choose
**Reload CMake Project**, or click the refresh icon in the CMake
panel at the bottom of the screen.

**Hard reset** -- deletes the build directory and starts over. Use
this when soft reload does not fix a broken build or when you switch
compilers: **Tools > CMake > Reset Cache and Reload Project**.

### compile_commands.json (VS Code / clangd)

clangd needs to know exactly how your project is compiled -- which
include paths and flags are in use -- to give accurate errors and
completions. CMake can produce a file called `compile_commands.json`
that records this. Generate it:

```bash
cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
ln -sf build/compile_commands.json compile_commands.json
```

`ln -sf` creates a symbolic link: a file that points to another file.
The result is that `compile_commands.json` at the project root always
points to the up-to-date copy CMake regenerates in `build/`. clangd
finds it automatically. CLion handles this on its own -- no manual
step needed there.

Regenerate it any time you change `CMakeLists.txt`.

### CLion: switching compilers or build configurations

**Settings > Build, Execution, Deployment > Toolchains**: drag a
toolchain to the top to make it the default.

For separate build profiles (for example, a Debug build with GCC
and a Release build with Clang): **Settings > CMake > +** to add a
profile, assign its Toolchain, and name it. The target dropdown in
the toolbar lets you switch between them.

### PyCharm: changing the interpreter later

**Settings > Project > Python Interpreter** > click the dropdown or
gear icon. Use **Add New Interpreter** to add a new one, or select
from the dropdown to switch.

### PyCharm: run configurations

A run configuration tells PyCharm which script to run, which
interpreter to use, what arguments to pass, and what environment
variables to set. Create one at **Run > Edit Configurations > + >
Python**, set the script path, and click OK. Configurations are saved
in `.idea/runConfigurations/` and can be committed to git.

### Where JetBrains stores settings

| Location | Contents |
|---|---|
| `.idea/` in project root | Per-project settings: run configs, build profiles, open files |
| `~/.config/JetBrains/<IDE>/` | Global IDE preferences, keymaps, plugins |
| `~/.cache/JetBrains/<IDE>/` | Indexes and caches; safe to delete; rebuilt on next open |

`.idea/` is created when you open any project in a JetBrains IDE. If
it becomes corrupted, delete it and reopen the project. Personal state
(your window layout, scroll positions) is in `.idea/.gitignore` by
default and should not be committed.

### Finding a binary's location

```bash
which gcc
which python3
which clangd
```

`which` tells you the full path to the executable that runs when you
type a command. Useful when an IDE cannot auto-detect something and
asks you to browse for a binary path.
