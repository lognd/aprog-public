# project-layout

## What you will practice

- Reading a CMakeLists.txt to understand a project's expected structure
- Understanding how `add_library`, `add_executable`, and
  `target_include_directories` imply specific file paths
- Organizing source files into the correct directory tree
- Building a multi-target CMake project from scratch

## How it works

You are dropped into a shell with all source files in a single flat
directory. A CMakeLists.txt is already present and locked -- do not
modify it. The build will fail until you read the CMakeLists.txt and
move each file to the exact path it expects.

Your job is to:

1. Read `CMakeLists.txt` carefully.
2. Create the directories it expects.
3. Move each source file to its correct location.
4. Build the project and run the app to confirm it works.

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
