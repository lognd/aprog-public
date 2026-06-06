// Reference solution for Graph Search (BFS).
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

int main() {
    int n, m;
    std::cin >> n >> m;

    std::vector<std::vector<int>> adj(n);
    for (int i = 0; i < m; ++i) {
        int u, v;
        std::cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (auto &nbrs : adj) std::sort(nbrs.begin(), nbrs.end());

    int src;
    std::cin >> src;

    std::vector<bool> visited(n, false);
    std::queue<int> q;
    visited[src] = true;
    q.push(src);

    bool first = true;
    while (!q.empty()) {
        int node = q.front();
        q.pop();
        if (!first) std::cout << " ";
        std::cout << node;
        first = false;
        for (int nb : adj[node]) {
            if (!visited[nb]) {
                visited[nb] = true;
                q.push(nb);
            }
        }
    }
    std::cout << "\n";
    return 0;
}
