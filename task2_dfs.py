"""
Task 2: Depth First Search (DFS)
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of Depth First Search (DFS) algorithm for:
    1. Graph Traversal (visiting all reachable nodes)
    2. Path Finding (searching for a path from a Start state to a Goal state)
    
    DFS explores as deep as possible along each branch before backtracking,
    using a Last-In-First-Out (LIFO) stack mechanism (or recursion).
"""

from typing import Dict, List, Set, Optional, Tuple


class Graph:
    """
    Represents an unweighted or directed/undirected graph using an adjacency list.
    """

    def __init__(self, directed: bool = False):
        self.adj_list: Dict[str, List[str]] = {}
        self.directed = directed

    def add_edge(self, u: str, v: str):
        """
        Add an edge between vertex u and vertex v.
        """
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []

        self.adj_list[u].append(v)
        if not self.directed:
            self.adj_list[v].append(u)

    def display_graph(self):
        """
        Print the adjacency list representation of the graph.
        """
        print("\nGraph Adjacency List:")
        for node, neighbors in self.adj_list.items():
            print(f"  {node} -> {', '.join(neighbors) if neighbors else 'None'}")


def dfs_traversal_recursive(graph: Dict[str, List[str]], start_node: str) -> List[str]:
    """
    Perform DFS traversal starting from `start_node` using recursion.
    Returns the order of visited nodes.
    """
    visited: Set[str] = set()
    traversal_order: List[str] = []

    def _dfs(node: str):
        visited.add(node)
        traversal_order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)

    if start_node in graph:
        _dfs(start_node)

    return traversal_order


def dfs_traversal_iterative(graph: Dict[str, List[str]], start_node: str) -> List[str]:
    """
    Perform DFS traversal using an explicit LIFO Stack (Iterative approach).
    """
    if start_node not in graph:
        return []

    visited: Set[str] = set()
    traversal_order: List[str] = []
    stack: List[str] = [start_node]

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.add(current)
            traversal_order.append(current)

            # Push neighbors in reverse order so left-most neighbor is visited first
            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal_order


def dfs_find_path(graph: Dict[str, List[str]], start: str, goal: str) -> Optional[List[str]]:
    """
    Find a path from `start` node to `goal` node using Depth First Search.
    Returns the path as a list of nodes, or None if no path exists.
    """
    # Stack stores tuples of (current_node, path_taken_so_far)
    stack: List[Tuple[str, List[str]]] = [(start, [start])]
    visited: Set[str] = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)

            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None


def main():
    print("=" * 60)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Task 2: Depth First Search (DFS) Algorithm")
    print("=" * 60)

    # 1. Create a sample AI state-space / graph
    # Example tree/graph:
    #         A
    #        / \
    #       B   C
    #      / \   \
    #     D   E   F
    #        /
    #       G
    g = Graph(directed=False)
    edges = [
        ('A', 'B'),
        ('A', 'C'),
        ('B', 'D'),
        ('B', 'E'),
        ('C', 'F'),
        ('E', 'G'),
    ]

    for u, v in edges:
        g.add_edge(u, v)

    g.display_graph()

    start_node = 'A'
    goal_node = 'G'

    # 2. Run DFS Traversal (Recursive)
    rec_order = dfs_traversal_recursive(g.adj_list, start_node)
    print(f"\n1. DFS Traversal (Recursive) from '{start_node}':")
    print("   " + " -> ".join(rec_order))

    # 3. Run DFS Traversal (Iterative with Stack)
    iter_order = dfs_traversal_iterative(g.adj_list, start_node)
    print(f"\n2. DFS Traversal (Iterative with Stack) from '{start_node}':")
    print("   " + " -> ".join(iter_order))

    # 4. Run DFS Goal Search (Path Finding)
    path = dfs_find_path(g.adj_list, start_node, goal_node)
    print(f"\n3. DFS Path Finding (From '{start_node}' to Goal '{goal_node}'):")
    if path:
        print(f"   Path found : {' -> '.join(path)}")
        print(f"   Path length: {len(path) - 1} steps")
    else:
        print(f"   No path exists between '{start_node}' and '{goal_node}'.")

    print("\n" + "=" * 60)
    print("DFS Characteristics:")
    print("  - Strategy        : LIFO (Stack) / Deepest node first")
    print("  - Time Complexity : O(V + E) where V = Vertices, E = Edges")
    print("  - Space Complexity: O(V) for visited set and call stack")
    print("  - Completeness    : Yes, for finite state spaces (with cycle detection)")
    print("  - Optimality      : No, does not guarantee shortest path")
    print("=" * 60)


if __name__ == "__main__":
    main()
