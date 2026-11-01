"""
A* (A-Star) Search Algorithm
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the A* (A-Star) Informed Search Algorithm.
    A* uses both actual path cost g(n) and heuristic estimate h(n)
    to find the optimal path from Start to Goal:
        f(n) = g(n) + h(n)
        
    Topics covered:
    1. Graph Search: Finding the shortest route on a weighted graph with heuristics
       (Classic Romania Map problem: Arad to Bucharest).
    2. 2D Grid Pathfinding: Finding the shortest path around obstacles on a grid.
"""

import heapq
from typing import Dict, List, Tuple, Optional


# =====================================================================
# 1. A* Search on a Weighted Graph
# =====================================================================

class WeightedGraph:
    """
    Weighted graph representation for A* route-finding.
    """

    def __init__(self):
        # adj[u] = [(v, cost), ...]
        self.adj: Dict[str, List[Tuple[str, int]]] = {}
        # heuristics[node] = estimated cost to goal
        self.heuristics: Dict[str, int] = {}

    def add_edge(self, u: str, v: str, cost: int):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, cost))
        self.adj[v].append((u, cost))

    def set_heuristics(self, heuristics: Dict[str, int]):
        self.heuristics = heuristics

    def a_star_search(self, start: str, goal: str) -> Tuple[Optional[List[str]], int, int]:
        """
        Runs A* search from start node to goal node.
        Returns:
            - optimal_path: List of nodes from start to goal
            - total_cost: Actual g(goal) path cost
            - nodes_expanded: Number of nodes expanded during search
        """
        # Priority Queue stores: (f_score, g_score, current_node, path)
        open_set: List[Tuple[int, int, str, List[str]]] = []
        
        # Best known g_score for each node
        g_scores: Dict[str, int] = {start: 0}
        
        initial_f = self.heuristics.get(start, 0)
        heapq.heappush(open_set, (initial_f, 0, start, [start]))
        
        visited: Dict[str, int] = {}
        nodes_expanded = 0

        while open_set:
            f, g, current, path = heapq.heappop(open_set)

            # Skip if we already reached this node with an equal or lower g cost
            if current in visited and visited[current] <= g:
                continue
            visited[current] = g
            nodes_expanded += 1

            # Check goal reached
            if current == goal:
                return path, g, nodes_expanded

            # Expand neighbors
            for neighbor, edge_cost in self.adj.get(current, []):
                tentative_g = g + edge_cost

                if tentative_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = tentative_g
                    h = self.heuristics.get(neighbor, 0)
                    f_score = tentative_g + h
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor, path + [neighbor]))

        return None, -1, nodes_expanded


# =====================================================================
# 2. A* Search on a 2D Grid with Obstacles
# =====================================================================

def grid_a_star(
    grid: List[str],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """
    Finds the shortest path on a 2D grid from start to goal avoiding obstacles ('#').
    Uses Manhattan distance as heuristic: h((r1, c1), (r2, c2)) = |r1 - r2| + |c1 - c2|
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    # Priority Queue stores: (f_score, g_score, (r, c), path)
    open_queue: List[Tuple[int, int, Tuple[int, int], List[Tuple[int, int]]]] = []
    start_h = heuristic(start, goal)
    heapq.heappush(open_queue, (start_h, 0, start, [start]))

    g_values: Dict[Tuple[int, int], int] = {start: 0}
    closed_set = set()

    # 4 directional movements: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_queue:
        f, g, current, path = heapq.heappop(open_queue)

        if current in closed_set:
            continue
        closed_set.add(current)

        if current == goal:
            return path, g

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # Bounds & obstacle check
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                tentative_g = g + 1
                if tentative_g < g_values.get(neighbor, float('inf')):
                    g_values[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_queue, (f_score, tentative_g, neighbor, path + [neighbor]))

    return None, -1


def print_grid_path(grid: List[str], path: List[Tuple[int, int]], start: Tuple[int, int], goal: Tuple[int, int]):
    """Visualizes the grid with the calculated path marked as '*'."""
    path_set = set(path)
    print("\n2D Grid Path Visualization:")
    for r in range(len(grid)):
        row_str = ""
        for c in range(len(grid[0])):
            pos = (r, c)
            if pos == start:
                row_str += "S "
            elif pos == goal:
                row_str += "G "
            elif pos in path_set:
                row_str += "* "
            else:
                row_str += f"{grid[r][c]} "
        print("  " + row_str)


# =====================================================================
# Main Driver & Demonstrations
# =====================================================================

def main():
    print("=" * 65)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   A* (A-Star) Informed Search Algorithm")
    print("=" * 65)

    # -------------------------------------------------------------
    # Demonstration 1: Classic Romania Route Finding (Arad -> Bucharest)
    # -------------------------------------------------------------
    print("\n--- DEMONSTRATION 1: GRAPH ROUTE PLANNING (Arad -> Bucharest) ---")
    romania = WeightedGraph()

    # Straight-line distance heuristics to Bucharest (Admissible heuristic)
    romania_heuristics = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Drobeta': 242,
        'Craiova': 160,
        'Rimnicu Vilcea': 193,
        'Fagaras': 176,
        'Pitesti': 100,
        'Bucharest': 0,
        'Giurgiu': 77,
        'Urziceni': 80
    }
    romania.set_heuristics(romania_heuristics)

    # Graph edges and actual road step costs
    edges = [
        ('Arad', 'Zerind', 75),
        ('Arad', 'Sibiu', 140),
        ('Arad', 'Timisoara', 118),
        ('Zerind', 'Oradea', 71),
        ('Oradea', 'Sibiu', 151),
        ('Timisoara', 'Lugoj', 111),
        ('Lugoj', 'Mehadia', 70),
        ('Mehadia', 'Drobeta', 75),
        ('Drobeta', 'Craiova', 120),
        ('Sibiu', 'Fagaras', 99),
        ('Sibiu', 'Rimnicu Vilcea', 80),
        ('Rimnicu Vilcea', 'Craiova', 146),
        ('Rimnicu Vilcea', 'Pitesti', 97),
        ('Craiova', 'Pitesti', 138),
        ('Fagaras', 'Bucharest', 211),
        ('Pitesti', 'Bucharest', 101),
        ('Bucharest', 'Giurgiu', 90),
        ('Bucharest', 'Urziceni', 85)
    ]
    for u, v, w in edges:
        romania.add_edge(u, v, w)

    start_city = 'Arad'
    goal_city = 'Bucharest'

    path, cost, nodes_expanded = romania.a_star_search(start_city, goal_city)

    print(f"Start City      : {start_city}")
    print(f"Goal City       : {goal_city}")
    print(f"Optimal Path    : {' -> '.join(path) if path else 'None'}")
    print(f"Total Road Cost : {cost} km")
    print(f"Nodes Expanded  : {nodes_expanded}")

    # -------------------------------------------------------------
    # Demonstration 2: 2D Grid Pathfinding around Obstacles
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print("--- DEMONSTRATION 2: 2D GRID PATHFINDING WITH OBSTACLES ---")

    # '.' = Open, '#' = Obstacle, 'S' = Start, 'G' = Goal
    maze = [
        ". . . . . . .".split(),
        ". # # # # . .".split(),
        ". . . . # . .".split(),
        ". # # . # . .".split(),
        ". . . . # . .".split(),
    ]
    grid_rows = len(maze)
    grid_cols = len(maze[0])
    start_pos = (0, 0)
    goal_pos = (4, 6)

    grid_path, step_count = grid_a_star(maze, start_pos, goal_pos)

    print(f"Grid Dimensions : {grid_rows} x {grid_cols}")
    print(f"Start Position  : {start_pos} ('S')")
    print(f"Goal Position   : {goal_pos} ('G')")
    print(f"Shortest Steps  : {step_count}")

    if grid_path:
        print_grid_path(maze, grid_path, start_pos, goal_pos)

    # -------------------------------------------------------------
    # Characteristics of A*
    # -------------------------------------------------------------
    print("=" * 65)
    print("A* Algorithm Characteristics:")
    print("  - Evaluation Function : f(n) = g(n) + h(n)")
    print("  - Heuristic Condition : Must be Admissible (h(n) <= h*(n)) for Optimality")
    print("  - Time Complexity     : O(b^d) where b = branching factor, d = solution depth")
    print("  - Space Complexity    : O(b^d) (stores all visited and frontier nodes in memory)")
    print("  - Completeness        : Yes (on finite graphs with positive step costs)")
    print("  - Optimality          : Guaranteed optimal if h(n) is admissible and consistent")
    print("=" * 65)


if __name__ == "__main__":
    main()
