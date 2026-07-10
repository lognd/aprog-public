# Curriculum Map

Course topics in teaching order. Each topic lists its activities and
assignments with a one-line description.

Status legend:
- done -- committed and verified end-to-end
- untested -- built but not yet verified end-to-end
- wip -- some artifacts built, others still planned
- planned -- designed but not built
- covered -- taught in lecture, no artifact needed

## 1. Ethics (untested)

Activities: none.

Assignments:
- `ai-vector-i` -- "vibe-code" a fix for a broken AI-generated VectorI class using an AI assistant; the point is experiencing (and reflecting on) shipping code you do not understand

## 2. Environment Setup (done)

Activities:
- `env-setup-shell` -- get a Linux/Unix shell and verify it by running a binary that prints a passphrase
- `env-setup-python` -- install Python 3 and the course's Python tooling (uv, ruff, ty, pytest)
- `env-setup-compiler` -- install both GCC/G++ and Clang/Clang++ compiler toolchains
- `env-setup-build-tools` -- install CMake and Make, the course's build system tools
- `env-setup-ide` -- install and configure an IDE (CLion, PyCharm, or VS Code)
- `env-setup-discord` -- join the class Discord server and set a real-name nickname
- `env-setup-git` -- install and configure git, GitHub, and the gh CLI

Assignments: none.

## 3. What is a computer? (covered)

No artifact.

## 4. Command-Line & Compilation (done)

Activities:
- `terminal-archeology` -- explore an unfamiliar broken C++ project tree using only shell commands, then fix it
- `git-heist` -- clean credentials and a large binary out of git history and reconcile a diverged branch

Assignments:
- `shell-build-pipeline` -- write a shell script that replicates make's incremental preprocess/compile/assemble/link pipeline

## 5. Variables & Type (done)

Activities:
- `bit-manipulation-re` -- trace five mystery bitwise functions by hand and predict their output, no compiling
- `implicit-conversion-minefield` -- predict the output of twelve snippets showing silent C++ type conversions
- `sizeof-bingo` -- predict the results of sixteen sizeof expressions across primitive types and data models

Assignments:
- `collatz-conjecture` -- implement the Collatz sequence using bitwise shifts instead of multiplication/division

## 6. Control & Functions (untested)

Activities:
- `complexity-clock` -- benchmark seven equivalent functions and diagnose why one is asymptotically slower
- `scope-safari` -- fix scope bugs (shadowing, static locals, loop-body scope) until program output matches
- `control-gauntlet` -- fix three buggy programs involving short-circuit evaluation, break/continue, and De Morgan's law

Assignments:
- `number-toolkit` -- implement five number-theory functions (is_prime, gcd, digit_sum, count_divisors, nth_fibonacci) under complexity constraints

## 7. Standard Library Types (done)

Activities:
- `array-foray` -- see why std::array size is fixed at compile time versus std::vector's heap growth
- `vector-inspector-corrector` -- diagnose and fix excessive std::vector reallocations using reserve
- `string-methods` -- fix two bugs in a word-wrap function and decode a passcode from the corrected output

Assignments:
- `csv-parser` -- parse CSV text with quoting/escaping into a nested vector of strings

## 8. Makefile & CMake (done)

Activities:
- `stale-build` -- diagnose and fix a Makefile that produces stale output on incremental builds
- `cmake-heist` -- write a CMakeLists.txt from an outline for a multi-module static-library project

Assignments:
- `dual-build` -- write both a Makefile and a CMakeLists.txt for the same small library

## 9. C++ Standards, Project Organization, README (done)

Activities:
- `cpp-standards-hunt` -- identify which C++ standard version a project's features require and set CMAKE_CXX_STANDARD to the minimum
- `project-docs` -- write README, LICENSE, CHANGELOG, CONTRIBUTORS, CODE_OF_CONDUCT, and SECURITY files with required headers
- `project-layout` -- read a locked CMakeLists.txt and move flat source files into the directory structure it expects

Assignments:
- `stats-library` -- implement an 8-function statistics library organized as a multi-target CMake project with its own test suite

## 10. Memory Model (heap vs. stack, call stack, recursion) (untested)

Activities:
- `stack-heap-bingo` -- classify 25 real C++ variable declarations by storage location and lifetime
- `recursion-unwind` -- answer questions about call counts and stack depth for naive, memoized, and iterative Fibonacci
- `call-stack-autopsy` -- read an AddressSanitizer stack-overflow trace and diagnose the missing recursion base case
- `stack-heap-safari` -- predict the output of six snippets illustrating call frames, unwinding, and heap lifetime

Assignments:
- `peano-math` -- build addition, multiplication, and exponentiation from a single recursive successor primitive

## 11. Pointers (pass modes, arrays as pointers, arithmetic) (untested)

Activities:
- `pass-mode-minefield` -- read function signatures and predict behavior for pass-by-value, by-reference, and by-pointer

Assignments:
- `pointer-matrix` -- implement a 2D matrix over a flat array using only pointer arithmetic, no subscript operator
- `pointer-toolkit` -- implement eight array/string utilities (reverse, find, strlen, strcpy, strcmp, ...) using only pointer arithmetic

## 12. C-Style Strings & Arrays (untested)

Activities:
- `cstring-predictor` -- trace C-style strings byte by byte to predict strlen/strcpy/strcat output
- `char-by-char` -- predict output of six programs that walk C strings character by character with pointers
- `cstring-whodunit` -- diagnose seven classic C-string bugs (overflow, pointer comparison, literal writes, sizeof vs strlen)
- `cstring-vs-stdstring` -- compare six side-by-side C-string vs std::string operations to see why std::string exists

Assignments:
- `sentence-tools` -- implement a word-level C-string library (word_count, word extraction, capitalize, trim) with no std::string

## 13. Const (untested)

Activities:
- `const-maze` -- distinguish const, constexpr, consteval, and constinit and their compile-time/runtime rules
- `const-contract` -- fix five programs that each violate a distinct const rule, reading compiler errors to locate the break
- `const-refactor` -- propagate const qualifiers through a call chain in a 2D character grid library using a lint script

Assignments:
- `const-qualifier-toolkit` -- implement a flat 2D char grid library with correct const/non-const pointer signatures throughout

## 14. Command Line Arguments (untested)

Activities:
- `argv-explorer` -- build a precise mental model of argc/argv layout and guarantees
- `cli-contract` -- reverse-engineer a compiled binary's CLI interface (flags, positional args, usage conventions) as a black box

Assignments:
- `connect-four` -- implement Connect Four's board logic (piece drop, four-in-a-row detection, computer opponent) over a flat char grid

## 15. Basic OS Theory (untested)

Activities:
- `posix-file-tour` -- walk the file I/O stack from program down to the kernel fd table, layer by layer
- `file-io-contracts` -- answer ten questions on the precise contracts of open/read/write/close, errno, and partial I/O
- `write-your-first-syscalls` -- fill in three blanks to print a file's contents using only open/read/write/close

Assignments:
- `hex-dump` -- implement a hexdump utility using only open/read/write/close/exit, no printf or formatting library

## 16. Streams & Files (done)

Activities:
- `iostream-interceptor` -- predict output of seven snippets covering stream whitespace rules, state flags, and operator chaining
- `sstream-formatter` -- predict exact formatted output of seven programs using iomanip manipulators and ostringstream
- `text-stream-surgery` -- diagnose and fix three classic ifstream bugs (eof() as loop condition, missing is_open, mixed >>/getline)
- `binary-stream-explorer` -- fill in three blanks in a binary file reader using ifstream, seekg, and sizeof to compute offsets

Assignments:
- `log-analyzer` -- parse a structured log file with ifstream/istringstream and print an aligned summary table with iomanip

## 17. Testing Tools (Catch2, gtest, gdb) (untested)

Activities:
- `catch2-tour` -- answer seven questions on wiring Catch2 into CMake, TEST_CASE/SECTION, and REQUIRE vs CHECK
- `gtest-tour` -- answer seven questions on wiring GTest into CMake, TEST/TEST_F, ASSERT vs EXPECT, and gtest_filter
- `catch2-first-contact` -- fill in four CMakeLists.txt blanks to fetch Catch2 and write a test suite for a stats library
- `gtest-cmake-lab` -- fix three deliberate CMake/GTest bugs and add two new TEST cases to an existing suite
- `gdb-time-machine` -- use gdb (run, bt, frame, print) to diagnose a null pointer dereference and a missing null terminator

Assignments:
- `html-parser` -- implement a minimal HTML tag-stripping/counting parser and write your own Catch2 test suite for it

## 18. Programming Paradigms (done)

Activities:
- `paradigm-lineup` -- identify which programming paradigm each of nine code snippets exemplifies
- `paradigm-refactor-detector` -- compare the same problem solved two ways and answer what each paradigm choice costs or buys

Assignments: none.

## 19. Structs (DOD & OOP intro) (untested)

Activities:
- `enum-field-day` -- predict the output of ten programs illustrating unscoped vs scoped enum rules
- `union-dissector` -- explore union memory sharing, use cases, and the C vs C++ type-punning distinction
- `struct-layout-bingo` -- measure struct field padding/alignment and see how a packing pragma removes it
- `dod-hot-cold` -- compare two particle-simulation benchmarks to observe the cost of the memory wall and perform a hot/cold split

Assignments:
- `tga-processor` -- build a CLI TGA image processor (blending, color ops, geometric transforms) over a packed binary struct

## 20. OOP Vocab & Theory (5 Pillars) (done)

Activities:
- `pillar-identification` -- name the OOP pillar each of eleven concrete software scenarios illustrates
- `is-a-has-a` -- decide is-a vs has-a vs neither for classic class-relationship scenarios, including the Square/Rectangle trap

Assignments: none.

## 21. OOP Implementation in C++ (wip)

Activities: none yet.

Assignments:
- `fraction-arithmetic` -- implement a Fraction class that maintains a lowest-terms invariant across every constructor and operation
- `raii-file-guard` -- (wip) implement FileGuard, whose constructor opens a POSIX fd and destructor closes it, to learn RAII

## 22. Inheritance (ABC, drawbacks, composition) (wip)

Activities: none yet.

Assignments:
- `media-library` -- design an abstract MediaItem base class and derived Book/Film/Album types cataloged by a Library class

## 23. Polymorphism (Interfaces, Templating) (wip)

Activities: none yet.

Assignments:
- `text-filters` -- implement four text filters twice: once via a virtual TextFilter interface, once via duck-typed templates

## 24. Design Patterns (wip)

Activities: none yet.

Assignments:
- `pattern-toolkit` -- implement Strategy, Observer, and Template Method patterns using non-owning base pointers, no dynamic memory

## 25. Dynamic Memory (Big 5, move semantics) (planned)

Nothing built yet.

## 26. Memory & Profiling Tools (valgrind, asan, perf, gprof) (planned)

Nothing built yet.

## 27. Smart Pointers (std + build your own) (wip)

Activities: none yet.

Assignments:
- `unique-ptr-from-scratch` -- (wip) implement a unique_ptr-like RAII owning-pointer class covering move semantics, release, and reset

## 28. Complexity Theory (planned)

Nothing built yet.

## 29. List ADT & Supporting DS (planned)

Nothing built yet.

## 30. Linked List (operations, build your own) (planned)

Nothing built yet.

## 31. Stack, Queue, Deque (ADT) (planned)

Nothing built yet.

## 32. Standard Containers p1 (planned)

Nothing built yet.

## 33. Map & Set ADT (planned)

Nothing built yet.

## 34. Standard Containers p2 (planned)

Nothing built yet.

## 35. Iterators (traversals) (planned)

Nothing built yet.

## 36. Proofs & Invariance (planned)

Nothing built yet.

## 37. Searching (planned)

Nothing built yet.

## 38. Sorting (planned)

Nothing built yet.

## 39. Function Pointers, Functors, Lambdas (planned)

Nothing built yet.

## 40. Libraries (static vs. dynamic) (planned)

Nothing built yet.

## 41. SFML (planned)

Nothing built yet.

## 42. auto & Type Deduction (planned)

Nothing built yet.

## 43. Modern C++ (C++11-C++17 features) (planned)

Nothing built yet.

## 44. Exception Handling (planned)

Nothing built yet.

## 45. Intro to Python (planned)

Nothing built yet.

## 46. Python Syntax (including OOP) (planned)

Nothing built yet.

## 47. Python Data Types (planned)

Nothing built yet.

## 48. Python Data Structures (planned)

Nothing built yet.

## 49. Python Decorators (planned)

Nothing built yet.

## 50. Python Classes (instance, class, static) (planned)

Nothing built yet.

## 51. Python Inner-Workings (__dict__, __mro__, etc.) (planned)

Nothing built yet.

## 52. Python Types & Comprehensions (planned)

Nothing built yet.

## 53. Python Generics & Typing (planned)

Nothing built yet.

## 54. Python Generators (planned)

Nothing built yet.

## 55. Python Async, Threads, Multiprocessing (planned)

Nothing built yet.

## 56. Python Contexts & Error Handling (planned)

Nothing built yet.

## 57. Python Scientific Computing (planned)

Nothing built yet.

## 58. Python Web Servers (planned)

Nothing built yet.

## 59. APIs (planned)

Nothing built yet.

## 60. Concepts from Other Languages (planned)

Nothing built yet.

## 61. Large Projects (planned)

Nothing built yet.

## 62. What's Next (planned)

Nothing built yet.
