# cpp-standards-hunt

## What you will practice

- Using cppreference.com to look up when C++ features were introduced
- Understanding how `CMAKE_CXX_STANDARD` controls what the compiler accepts
- Reading compiler errors as diagnostic clues, not obstacles

## The premise

The C++ standard has evolved over decades. Features added in one version are
not available in earlier versions. When a project fails to compile, one
possible cause is that the build system is targeting a standard that predates
the features the code uses.

Your job in this activity is not to understand what the code does. You only
need to identify the language features it uses, look each one up on
cppreference to find which standard version introduced it, and set
`CMAKE_CXX_STANDARD` in `CMakeLists.txt` to the minimum version that covers
all of them.

You must find the minimum. Using a higher standard than necessary will not
unlock the passphrase.

## How it works

You are dropped into a shell with a small C++ project. The CMakeLists.txt
sets the standard too low, so the project will not compile. Look at the
compiler errors, open cppreference, and figure out what version is needed.

A useful starting point: https://en.cppreference.com/w/cpp/compiler_support

## How to run

```
python3 launch.py
```

A Makefile is provided. Inside the shell:

```
make
make run
```

Type `exit` when you are ready for the validator to check your work.
