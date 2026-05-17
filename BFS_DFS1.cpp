#include <iostream>
#include <vector>
#include <queue>
#include <omp.h>

using namespace std;

class Graph {
    int V;
    vector<vector<int> > adj;

public:
    Graph(int V) : V(V), adj(V) {}

    void addEdge(int v, int w) {
        adj[v].push_back(w);
    }

    void parallelDFS(int startVertex) {
        vector<bool> visited(V, false);
        parallelDFSUtil(startVertex, visited);
    }

    void parallelDFSUtil(int v, vector<bool>& visited) {

        // CRITICAL: print one node at a time (no merged digits)
        #pragma omp critical(print)
        {
            cout << v << " ";
        }

        #pragma omp parallel for schedule(dynamic)
        for (int i = 0; i < (int)adj[v].size(); ++i) {
            int n = adj[v][i];

            bool shouldVisit = false;

            // CRITICAL: check-and-set visited atomically
            // Without this, two threads can BOTH see !visited[n]
            // as true and both recurse — visiting the same node twice
            // here the iteration across multiple cpu threads 
            #pragma omp critical(visited_check)
            {
                if (!visited[n]) {
                    visited[n] = true;   // mark BEFORE recursing
                    shouldVisit = true;
                }
            }

            if (shouldVisit) {
                parallelDFSUtil(n, visited);
            }
        }
    }

    // ---------------------------------------------
    //  PARALLEL BFS  –  fixes applied
    //  Problem 1: q.push(n) called from multiple threads
    //             simultaneously ? std::queue is NOT
    //             thread-safe ? undefined behaviour / crash
    //  Problem 2: visited[n] check + set was not atomic
    //             ? same node pushed to queue multiple times
    //  Problem 3: cout from multiple threads ? garbled output
    //  Fix: wrap visited-check+set+push inside omp critical
    //       so the queue is only accessed by one thread at a time
    // ---------------------------------------------
    void parallelBFS(int startVertex) {
        vector<bool> visited(V, false);
        queue<int> q;

        visited[startVertex] = true;
        q.push(startVertex);

        while (!q.empty()) {
            int v = q.front();
            q.pop();

            // CRITICAL: safe single-threaded print
            #pragma omp critical(print)
            {
                cout << v << " ";
            }

            #pragma omp parallel for schedule(dynamic)
            for (int i = 0; i < (int)adj[v].size(); ++i) {
                int n = adj[v][i];

                // CRITICAL: check-and-set visited + push are one
                // atomic unit — no other thread can interleave here
                // Without this, two threads could both see !visited[n]
                // and push n twice, causing duplicate BFS visits
                #pragma omp critical(bfs_queue)
                {
                    if (!visited[n]) {
                        visited[n] = true;
                        q.push(n);
                    }
                }
            }
        }
    }
};

int main() {
    Graph g(7);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 4);
    g.addEdge(2, 5);
    g.addEdge(2, 6);

    /*
        Graph structure:
              0
             / \
            1   2
           / \ / \
          3  4 5  6
    */

    cout << "Depth-First Search (DFS): ";
    g.parallelDFS(0);
    cout << endl;

    cout << "Breadth-First Search (BFS): ";
    g.parallelBFS(0);
    cout << endl;

    return 0;
}

/*
  COMPILE & RUN:
    g++ -fopenmp -o bfs_dfs BFS_DFS_fixed.cpp
    ./bfs_dfs

  EXPECTED OUTPUT:
    Depth-First Search (DFS):  0 1 3 4 2 5 6   (depth order, no duplicates)
    Breadth-First Search (BFS): 0 1 2 3 4 5 6  (level order, no duplicates
*/
