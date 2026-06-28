# Activity: Project Layout

A CMakeLists.txt describes a project's structure: which files build which
targets, and where headers live. This activity gives you a locked
CMakeLists.txt and a pile of source files all in one flat directory. Your
job is to read the build file and move each source file to exactly where
CMake expects it.

## Concepts covered

- Reading a `CMakeLists.txt` to infer the expected directory structure
- How `add_library`, `add_executable`, and `target_include_directories` imply specific file paths
- Creating directories and moving files from the command line (`mkdir -p`, `mv`)
- Building a multi-target CMake project after reorganizing source files

## How it works

You are dropped into a shell with all source files in a single flat
directory. A `CMakeLists.txt` is already present and locked -- do not
modify it. The build will fail until you read the `CMakeLists.txt` and
move each file to the exact path it expects.

## Getting started

```bash
python3 launch.py
```

A Makefile is provided. Inside the shell:

### Step 1 -- read CMakeLists.txt

Open `CMakeLists.txt` and trace every `add_library`, `add_executable`, and
`target_include_directories` call. Each one implies a specific directory
structure.

### Step 2 -- create the directories

Create whatever subdirectories the build file expects. Use `mkdir -p` to
create nested directories in one command.

### Step 3 -- move the source files

Move each source file to its correct location:

```bash
mv filename.cpp subdir/filename.cpp
```

### Step 4 -- build and verify

```bash
make
make run
```

Both must succeed before exiting.

### Step 5 -- exit

```
exit
```

The launcher checks your work automatically.

## You will know you are done when...

The build succeeds and the launcher prints the passphrase.

## Going further

- Add a fourth target to the locked CMakeLists.txt after the activity ends:
  a new library with its own include path and a test executable. Does the
  structure you learned here generalize cleanly?
- Look up `FetchContent` in the CMake docs. How would you use it to pull in
  a third-party library (e.g., Catch2) without committing it to the repo?
- Read the CMake documentation for `PRIVATE`, `PUBLIC`, and `INTERFACE`
  keyword in `target_include_directories`. Write three examples -- one of each.
