# Graph Search

Implement breadth-first search (BFS) on an undirected graph.

## Problem Statement

Read an undirected graph from stdin and print the nodes visited by BFS
starting from a given source node. Nodes are numbered `0` through `N-1`.
When expanding a node, visit its neighbors in ascending numerical order.

## Input Format

```
N M
u_0 v_0
u_1 v_1
...
u_{M-1} v_{M-1}
source
```

- Line 1: `N` (number of nodes) and `M` (number of edges)
- Next `M` lines: each edge `u v` (undirected)
- Last line: the source node for BFS

## Output Format

Print the BFS visit order as space-separated integers on one line, followed
by a newline.

## Examples

### Example 1

**Input:**
```
5 5
0 1
0 2
1 3
2 3
3 4
0
```

**Output:**
```
0 1 2 3 4
```

### Example 2

**Input:**
```
4 2
0 1
2 3
0
```

**Output:**
```
0 1
```
(nodes 2 and 3 are unreachable from 0)

## Grading

| Component     | Points |
|---------------|--------|
| Files present | 0 (required) |
| Compilation   | 0 (required) |
| Correctness   | 80     |
| Memory safety | 20     |

## Submission

Submit all source files **and** a `CMakeLists.txt`. The CMake target must be
named `graph-search`.

## Local Build

```bash
cmake -B build .
cmake --build build
echo "5 5
0 1
0 2
1 3
2 3
3 4
0" | ./build/graph-search
```
