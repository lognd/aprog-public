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

A Makefile is provided. Inside the shell:

```bash
make
make run
```

Type `exit` when you are ready for the validator to check your work.

## You will know you are done when...

The validator accepts your `CMakeLists.txt` and prints the passphrase.

## Going further

- Find a feature introduced in C++20 (e.g., concepts, ranges, `std::span`)
  and try using it in a project targeting C++17. Read the error message.
- Look up the compiler support table on cppreference for a feature that is
  partially implemented -- one where GCC and Clang diverge. What does that mean?
- Try compiling with `-std=c++23` on your machine. Which C++23 features
  are already available in your version of GCC or Clang?
