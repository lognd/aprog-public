# Activity: C++ Standards Hunt

The C++ standard has evolved over decades. Features added in one version are
not available in earlier versions. When a project fails to compile, one
possible cause is that the build system is targeting a standard that predates
the features the code uses.

## Background

Your job in this activity is not to understand what the code does. You only
need to identify the language features it uses, look each one up on
cppreference (a community-maintained reference site documenting the C++
language and standard library, including which standard version introduced
each feature) to find which standard version introduced it, and set
`CMAKE_CXX_STANDARD` -- the CMake variable that tells the compiler which
version of the C++ language spec to compile against -- in `CMakeLists.txt`
to the minimum version that covers all of them.

You must find the minimum. Using a higher standard than necessary will not
unlock the passphrase.

A useful starting point: https://en.cppreference.com/w/cpp/compiler_support

## Concepts covered

- How C++ standard versions (C++11, C++14, C++17, C++20) gate language features
- Reading compiler errors as clues to which standard version is required
- Using cppreference.com to look up when a feature was introduced
- Setting `CMAKE_CXX_STANDARD` to target a specific standard version

## How it works

You are dropped into a shell with a small C++ project. The `CMakeLists.txt`
sets the standard too low, so the project will not compile. Look at the
compiler errors, open cppreference, and figure out what version is needed.
Then set `CMAKE_CXX_STANDARD` to the minimum correct value.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project, containing `main.cpp`,
`CMakeLists.txt`, and a `Makefile`.

### Step 1 -- read main.cpp

Open `main.cpp` and read through it. Each line that uses a feature worth
looking up is marked with a `// check out:` or `// look up:` comment
naming the feature.

### Step 2 -- try to build it

```bash
make
```

`CMakeLists.txt` currently sets `CMAKE_CXX_STANDARD` to 11, which is too
low, so the build will fail with one or more compiler errors. Read the
errors -- they name the symbol that could not be compiled.

### Step 3 -- look up each feature

For every failing symbol (and every commented feature in `main.cpp`), search
cppreference for it and find the version marker on the page, written like
`(since C++11)`. That marker is the standard version that introduced the
feature. The largest marker across all the features used is the minimum
standard the project needs.

### Step 4 -- edit CMakeLists.txt

Open `CMakeLists.txt` and change the number in `set(CMAKE_CXX_STANDARD 11)`
to the minimum version you found.

### Step 5 -- rebuild and run

```bash
make
make run
```

Repeat steps 2-4 if the build still fails or you are not confident you
found every feature.

### Step 6 -- exit

    exit

The validator checks your work automatically.

## You will know you are done when...

The validator accepts your `CMakeLists.txt` and prints the passphrase.

## Going further

- Find a feature introduced in C++20 (e.g., concepts, ranges, `std::span`)
  and try using it in a project targeting C++17. Read the error message.
- Look up the compiler support table on cppreference for a feature that is
  partially implemented -- one where GCC and Clang diverge. What does that mean?
- Try compiling with `-std=c++23` on your machine. Which C++23 features
  are already available in your version of GCC or Clang?
