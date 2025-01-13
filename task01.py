from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.graph = [[0] * vertices for _ in range(vertices)]

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v, capacity in enumerate(self.graph[u]):
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True

        return False

    def edmonds_karp(self, source, sink):
        parent = [-1] * self.V
        max_flow = 0
        flows = [[0] * self.V for _ in range(self.V)]

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                flows[u][v] += path_flow
                v = parent[v]

        return max_flow, flows

if __name__ == "__main__":
    vertices = 22  # 20 nodes + source (0) + sink (21)
    source = 0
    sink = vertices - 1

    graph = Graph(vertices)

    # Adding edges from source to terminals
    terminal_edges = [(1, 25), (2, 20), (3, 15), (4, 15), (5, 30)]
    for u, cap in terminal_edges:
        graph.add_edge(source, u, cap)

    # Adding edges between terminals and stores
    terminal_to_store_edges = [
        (1, 6, 15), (1, 7, 10), (1, 8, 20),
        (2, 9, 15), (2, 10, 10), (2, 11, 25),
        (3, 12, 20), (3, 13, 15), (3, 14, 10),
        (4, 15, 20), (4, 16, 10), (4, 17, 15), (4, 18, 5), (4, 19, 10)
    ]
    for u, v, cap in terminal_to_store_edges:
        graph.add_edge(u, v, cap)

    # Adding edges from stores to sink
    for store in range(6, 20):
        graph.add_edge(store, sink, float('inf'))

    max_flow, flows = graph.edmonds_karp(source, sink)
    print(f"Maximum flow: {max_flow}")

    # Flow Table
    print("\nFlow Table:")
    print("Terminal\tStore\tActual Flow")
    terminal_map = {1: "Terminal 1", 2: "Terminal 1", 3: "Terminal 1", 4: "Terminal 2", 5: "Terminal 2"}

    for u in range(vertices):
        for v in range(vertices):
            if flows[u][v] > 0 and u in terminal_map and 6 <= v <= 19:
                terminal = terminal_map[u]
                store = f"Store {v - 5}"
                print(f"{terminal}\t{store}\t{flows[u][v]}")
