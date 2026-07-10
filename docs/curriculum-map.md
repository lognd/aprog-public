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
- `env-setup-sfml` -- install SFML and verify a real sf::Image compile-link-run test
- `env-setup-ide` -- install and configure an IDE (CLion, PyCharm, or VS Code)
- `env-setup-git` -- install and configure git, GitHub, and the gh CLI
- `env-setup-discord` -- join the class Discord server and set a real-name nickname

Assignments: none.

## 3. What is a computer? (covered)

No artifact.

## 4. Command-Line & Compilation (done)

Activities:
- `terminal-archeology` -- explore an unfamiliar broken C++ project tree using only shell commands, then fix it
- `git-mental-models` -- conceptual model of git: commits as snapshots, branches as pointers, merge vs. rebase, and what problem the system solves
- `git-heist` -- clean credentials and a large binary out of git history and reconcile a diverged branch
- `cpp-syntax-boot-camp` -- predict-then-compile twelve first-contact C++ programs: variables, if/else, loops, functions, strings

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
- `complexity-clock` -- benchmark seven equivalent functions and diagnose why one is dramatically slower as input grows
- `scope-safari` -- fix scope bugs (shadowing, static locals, loop-body scope) until program output matches
- `control-gauntlet` -- fix three buggy programs involving short-circuit evaluation, break/continue, and De Morgan's law

Assignments:
- `number-toolkit` -- implement five number-theory functions (is_prime, gcd, digit_sum, count_divisors, nth_fibonacci) under complexity constraints

## 7. Standard Library Types (done)

Activities:
- `array-foray` -- see why std::array size is fixed at compile time versus std::vector's heap growth
- `vector-inspector-corrector` -- diagnose and fix excessive std::vector reallocations using reserve
- `string-methods` -- fix two bugs in a word-wrap function and decode a passcode from the corrected output
- `capacity-chronicles` -- predict size/capacity output of seven vector programs with reserve-pinned, standard-guaranteed values

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
- `os-mental-models` -- eleven no-code questions building the conceptual model of what an OS is, kernel vs distribution, user/kernel mode, syscalls, and the three problems (sharing, isolation, abstraction) an OS solves
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

## 21. OOP Implementation in C++ (untested)

Activities:
- `ctor-dtor-tracer` -- predict the exact construction/destruction output of eight programs to learn object lifetime rules
- `encapsulation-audit` -- diagnose what (if anything) is wrong with ten small class designs: public data, missing const, leaky getters
- `operator-overload-workshop` -- predict output of nine programs covering operator==/+/<</[]/++/bool overloading and the member-vs-free decision rule

Assignments:
- `fraction-arithmetic` -- implement a Fraction class that maintains a lowest-terms invariant across every constructor and operation
- `raii-file-guard` -- implement FileGuard, whose constructor opens a POSIX fd and destructor closes it, to learn RAII

## 22. Inheritance (ABC, drawbacks, composition) (untested)

Activities:
- `hiding-hunt` -- predict output of six programs distinguishing virtual overriding from name hiding, including the virtual-in-constructor classic
- `slice-of-life` -- predict output of six programs where object slicing silently cuts derived objects down to their base class

Assignments:
- `media-library` -- design an abstract MediaItem base class and derived Book/Film/Album types cataloged by a Library class

## 23. Polymorphism (Interfaces, Templating) (untested)

Activities:
- `dispatch-detective` -- predict output of seven programs to learn when C++ binds a call at compile time vs run time
- `duck-or-vtable` -- compare interface-based and template-based versions of the same code and answer what each can and cannot do

Assignments:
- `text-filters` -- implement four text filters twice: once via a virtual TextFilter interface, once via duck-typed templates

## 24. Design Patterns (untested)

Activities:
- `smell-hunt` -- name the code smell in nine working-but-rotting snippets and learn which refactor fixes each
- `pattern-matcher` -- match requirement scenarios to the right design pattern, including two where no pattern is needed
- `space-between-the-lines` -- misuse-resistant API design: why a partially formed object must never be reachable, and how type design (not comments) prevents it

Assignments:
- `pattern-toolkit` -- implement Strategy, Observer, and Template Method patterns using non-owning base pointers, no dynamic memory

## 25. Dynamic Memory (Big 5, move semantics) (untested)

Activities:
- `big5-tracer` -- predict which special member functions run in nine instrumented programs (copies, moves, elision, std::move)
- `rule-of-five-whodunit` -- diagnose what goes wrong in seven resource-managing classes with missing or broken special members
- `value-category-taxonomy` -- classify lvalue/xvalue/prvalue expressions and learn how value category drives which special member overload resolution picks
- `who-frees-this` -- ownership as a concept in the raw-pointer world: leak/double-free/dangling-use, transfer vs. borrow, real API ownership contracts, and the fix ladder that ends at smart pointers

Assignments: none yet.

## 26. Memory & Profiling Tools (valgrind, asan, perf, gprof) (untested)

Activities:
- `asan-autopsy` -- read six real AddressSanitizer reports and name the heap/stack error class each one describes
- `valgrind-leak-lab` -- fix three distinct leaks in a real program; the launcher re-runs valgrind and demands zero definitely-lost bytes

Assignments: none.

## 27. Smart Pointers (std + build your own) (untested)

Activities:
- `ownership-court` -- rule on ten ownership scenarios: unique_ptr, shared_ptr, weak_ptr, or plain raw pointer/reference
- `shared-ptr-tracer` -- predict use_count and destruction output of seven programs, including the reference-cycle leak weak_ptr fixes

Assignments:
- `unique-ptr-from-scratch` -- implement a unique_ptr-like RAII owning-pointer class covering move semantics, release, and reset

## 28. Complexity Theory (untested)

Activities:
- `big-o-lineup` -- classify ten functions into O(1) through O(n^2), including triangular loops, binary search, and amortized push_back
- `growth-witness` -- estimate runtimes and growth crossovers numerically from a measured data point and a complexity class

Assignments: none.

## 29. List ADT & Supporting DS (untested)

Activities:
- `list-tradeoff-tribunal` -- pick the right backing structure (dynamic array vs linked list) for nine workload scenarios
- `index-vs-node` -- count element shifts vs pointer hops for the same operations on an array list and a linked list

Assignments: none.

## 30. Linked List (operations, build your own) (untested)

Activities:
- `link-tracer` -- predict traversal output of six programs that splice, reverse, and break raw linked-list nodes by hand

Assignments:
- `linked-list-from-scratch` -- implement a templated singly linked list with the full Big 5, O(1) push_back and size, graded under ASan and Valgrind

## 31. Stack, Queue, Deque (ADT) (untested)

Activities:
- `ring-buffer-rehearsal` -- trace head/tail indices of a circular buffer through wrapped push/pop sequences with modulo arithmetic

Assignments:
- `deque-two-ways` -- implement a Deque twice (circular-buffer array with O(1) pop_front enforced by a performance test, and doubly linked list) plus Stack/Queue adapters

## 32. Standard Containers p1 (untested)

Activities:
- `container-casting-call` -- pick vector, deque, list, forward_list, or array for eight workloads, weighted toward list/forward_list's splice and iterator-stability strengths (vector/array covered at row 7 are mentioned, not centered)
- `splice-circus` -- predict output of seven programs on std::list splice/sort/remove/unique and std::forward_list's before_begin/insert_after/no-size() API

Assignments: none.

## 33. Map & Set ADT (untested)

Activities:
- `associative-adjudicator` -- choose map, unordered_map, set, or unordered_set per scenario; hash table vs balanced tree from scratch
- `bracket-trap` -- predict output of six map/unordered_map programs centered on the operator[] insert-on-read trap

Assignments:
- `word-ledger` -- implement six word-analysis functions over tokenized text using map, unordered_map, and set operations

## 34. Standard Containers p2 (untested)

Activities:
- `adaptor-roundup` -- choose stack, queue, priority_queue, or plain vector per scenario, including the adaptors-cannot-iterate trap
- `multi-court` -- predict output of seven programs on multiset/multimap duplicate keys and priority_queue pop order

Assignments: none.

## 35. Iterators (traversals) (untested)

Activities:
- `iterator-walk` -- predict output of eight programs walking containers with iterators: fence-post end(), reverse, map ->first/->second, safe erase
- `invalidation-minefield` -- rule valid or undefined for eight held-iterator scenarios across vector, map, and deque

Assignments:
- `linked-list-iterators` -- add Iterator/ConstIterator, begin/end, insert_after, and erase_after to a provided linked list so range-for works

## 36. Proofs & Invariance (untested)

Activities:
- `invariant-inspector` -- pick the true loop invariant for nine loops and chain it with the exit condition to the postcondition
- `termination-tribunal` -- rule whether seven loops always terminate, using the decreasing-measure argument (Collatz included, honestly)

Assignments: none.

## 37. Searching (untested)

Activities:
- `search-stepper` -- trace binary search mid/lo/hi values and comparison counts numerically on concrete arrays
- `binary-search-autopsy` -- diagnose six subtly broken binary searches: infinite loop, skipped answer, out-of-bounds, overflow mid

Assignments:
- `binary-bounds` -- implement binary search plus first/last-occurrence bounds and an O(log n) count_of enforced by a performance test

## 38. Sorting (untested)

Activities:
- `sort-pass-tracer` -- trace single passes and swap/comparison counts of bubble, selection, insertion, and merge steps on concrete arrays
- `sorting-court` -- stability, algorithm choice, quadratic-vs-nlogn scale, and what std::sort actually is (introsort)

Assignments:
- `sort-suite` -- implement selection, insertion, and merge sorts plus a stability-required pair sort, oracle-checked and performance-gated

## 39. Function Pointers, Functors, Lambdas (untested)

Activities:
- `callable-lineup` -- predict output of eight programs using function pointers, stateful functors, and lambdas with each capture mode
- `capture-court` -- rule on capture semantics: value vs reference divergence, capture defaults, init-capture, and the dangling-capture UB trap

Assignments:
- `sort-with-anything` -- generalize merge sort with a Compare template parameter and prove it works with all three callable species

## 40. Libraries (static vs. dynamic) (untested)

Activities:
- `library-forge` -- build libmathx.a and libmathx.so by hand, hit the LD_LIBRARY_PATH loader error, and fix it; checker verifies both link modes
- `link-order-lab` -- diagnose compile vs link vs load errors, -L/-l mechanics, and why library order on the link line matters

Assignments: none.

## 41. SFML (untested)

Activities:
- `sfml-anatomy` -- the game-loop mental model: event-queue draining, clear/draw/display, top-left coordinates, dt-scaled movement, draw order

Assignments:
- `sfml-canvas` -- implement five sf::Image pixel routines (gradient, checkerboard, disk, blend, outline) graded per-pixel against reference PNGs, headless by construction

## 42. auto & Type Deduction (untested)

Activities:
- `deduction-detective` -- name the type auto deduces in ten cases: dropped references, stripped const, const char*, the map pair trap
- `auto-consequences` -- predict output of seven programs where auto-by-copy and auto& visibly diverge

Assignments: none.

## 43. Modern C++ (C++11-C++17 features) (untested)

Activities:
- `modernization-bureau` -- match ten pre-C++11 snippets to the modern feature that replaces them, with the rewrite shown each time
- `seventeen-tracer` -- predict output of six programs using structured bindings, if-with-initializer, optional, and string_view

Assignments: none.

## 44. Exception Handling (untested)

Activities:
- `unwind-tracer` -- predict output of seven throw/catch programs where instrumented destructors print during stack unwinding
- `throw-or-not-court` -- judge nine scenarios: throw, return a sentinel, assert, or never throw (destructors), with honest tradeoffs

Assignments:
- `parse-with-grace` -- build an exceptions-first parsing library with exact exception types/messages, propagation transparency, and RAII balance under throws

## 45. Intro to Python (untested)

Activities:
- `python-syntax-boot-camp` -- predict output of twelve first-contact Python programs with a C++ to Python construct mapping table
- `python-culture-shock` -- predict output of nine Python snippets that surprise C++ programmers: names not owners, no overflow, slice copies
- `indentation-court` -- rule on indentation structure, no-block-scope visibility, truthiness, and is None conventions

Assignments: none.

## 46. Python Syntax (including OOP) (untested)

Activities:
- `dunder-decoder` -- predict output of eight class snippets mapping C++ OOP onto __init__, self, __str__/__repr__, __eq__, and super()
- `pythonic-or-not` -- pick the idiomatic version: enumerate over range(len), join over loop concat, attributes over getters

Assignments:
- `cpp-to-python-phrasebook` -- port six course-familiar string functions to stdlib-only Python, graded by pytest with a ty cleanliness bonus

## 47. Python Data Types (untested)

Activities:
- `mutability-tribunal` -- predict output of nine snippets on str/tuple immutability, += rebind vs mutate, and unhashable keys
- `numeric-nuances` -- floats vs exact ints: banker's rounding, floor division on negatives, and why 0.1 + 0.2 != 0.3

Assignments: none.

## 48. Python Data Structures (untested)

Activities:
- `slice-sorcery` -- predict output of eight slicing snippets: copies vs aliases, slice assignment, sort() returning None, shared-row traps
- `structure-selector` -- choose list, tuple, dict, or set per scenario, including hashability and duplicate/order behavior

Assignments:
- `roster-wrangler` -- implement six typed roster-analysis functions over list[dict] records, pytest-graded with a ty cleanliness bonus

## 49. Python Decorators (untested)

Activities:
- `decorator-x-ray` -- predict output of nine snippets: closures, decoration-time vs call-time, stacking order, functools.wraps
- `wrap-court` -- rule on what @deco desugars to, when decorator bodies run, and the forgot-to-return-the-wrapper trap

Assignments: none.

## 50. Python Classes (instance, class, static) (untested)

Activities:
- `method-trinity` -- predict output of seven snippets contrasting instance, class, and static methods, properties, and attribute shadowing
- `self-cls-court` -- match method kinds to jobs and rule on self mechanics, missing-instance calls, and name mangling

Assignments:
- `temperature-lab` -- build a Temperature class with classmethod factories, a validated property, computed read-only properties, and tolerant equality

## 51. Python Inner-Workings (__dict__, __mro__, etc.) (untested)

Activities:
- `dunder-dungeon` -- watch __dict__ grow, shadowing reverse under del, diamond __mro__, bound methods, and __slots__ refuse attributes
- `lookup-court` -- rule where attributes resolve, what super() actually consults, and why monkey-patching hits existing instances
- `pyobject-autopsy` -- the real (simplified) PyObject/PyVarObject/PyListObject/PyLongObject structs from CPython's Include/object.h: refcounting as automated shared ownership, reference cycles, why a list stores pointers not values, `is` vs `==` at the struct level, string interning, big-int digit arrays, and the None/True/False singletons

Assignments: none.

## 52. Python Types & Comprehensions (untested)

Activities:
- `comprehension-decathlon` -- predict output of ten comprehension snippets: filter vs if/else position, nesting, laziness, scoping
- `type-inspector` -- type()/isinstance semantics, bool as int, and why annotations are promises the runtime never checks

Assignments: none.

## 53. Python Generics & Typing (untested)

Activities:
- `annotation-arsenal` -- pick correct annotations, read Callable types, TypeVar vs overload, and the mutable-default trap
- `typevar-tracer` -- observe that annotations and TypeVars vanish at runtime: no coercion, no enforcement, live mutable-default growth
- `make-the-linter-happy` -- fix seeded ruff/ty/pytest findings in a small typed project until all four quality gates run green
- `pytest-dojo` -- write real pytest tests: a parametrized table, pytest.raises, a tmp_path fixture, and a slow marker that -m deselects
- `ship-it-pipeline` -- CI/CD judgment calls: workflow anatomy, why the red X blocks merges, secrets and fork PRs, ssh deploys, .env practices

Assignments: none.

## 54. Python Generators (untested)

Activities:
- `yield-yard` -- predict output of nine generator snippets proving pause/resume, laziness, exhaustion, and pipeline chaining

Assignments:
- `lazy-pipeline` -- build a five-stage generator log pipeline where instrumented iterables prove each stage consumes only what it must

## 55. Python Async, Threads, Multiprocessing (untested)

Activities:
- `concurrency-court` -- choose asyncio, threads, multiprocessing, or plain sequential per workload; GIL and races taught from scratch
- `await-tracer` -- predict deterministic asyncio output: unawaited coroutines, gather ordering, sleep(0) interleaving
- `who-handles-the-wait` -- disambiguate event loop, threading, interrupts, and concurrency-vs-parallelism side by side

Assignments: none.

## 56. Python Contexts & Error Handling (untested)

Activities:
- `with-wizardry` -- predict output of nine context-manager snippets: the unwind guarantee, suppression, contextmanager, try/else/finally

Assignments:
- `context-keeper` -- implement journaling, selective-suppression, and copy-then-commit transaction context managers plus a failure-proof cleanup chain

## 57. Python Scientific Computing (untested)

Activities:
- `broadcast-bureau` -- numpy shapes, broadcasting legality, views vs copies, boolean masks, and axis semantics

Assignments:
- `grade-matrix` -- vectorize six grade-matrix operations with loops forbidden by a keyword gate; numpy is the only allowed import

## 58. Python Web Servers (untested)

Activities:
- `osi-elevator` -- very basic networking first: why layers, encapsulation as nesting envelopes, which layer HTTP/TCP/IP/Ethernet live at, IP/port/MAC, DNS, and TCP vs. "just send it"
- `http-anatomy` -- request anatomy, methods, status codes, idempotency, and statelessness from first principles

Assignments:
- `tiny-ledger-api` -- build a Flask CRUD API with an app factory, exact status codes and error bodies, graded via the test client
- `typed-ledger-api` -- the same ledger domain rebuilt on FastAPI: a pydantic model replaces hand-written validation, graded via TestClient for framework-generated 422s and response_model field-stripping

## 59. APIs (untested)

Activities:
- `client-court` -- status-code handling, key placement, rate limits, pagination, and why you always set a timeout

Assignments:
- `api-harvester` -- write API-client logic against an injected fetch callable; instrumented fakes grade exact retry counts and pagination

## 60. Concepts from Other Languages (untested)

Activities:
- `language-safari` -- map Rust ownership, Java GC, JS promises, Go channels, and TypeScript typing back onto course concepts

Assignments: none.

## 61. Large Projects (covered)

No artifact. Taught in lecture.

## 62. What's Next (covered)

No artifact. Taught in lecture.
