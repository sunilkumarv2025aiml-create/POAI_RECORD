"""
Task: Blocks World Program
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the Blocks World planning problem in AI.
    The goal is to transition from an initial block configuration
    to a designated goal state using a sequence of block moves.
"""


class BlocksWorld:
    def __init__(self):
        # Initial State: A is on B, B is on table, C is on table
        self.state = {
            "A": "B",       # A is on B
            "B": "table",   # B is on table
            "C": "table"    # C is on table
        }
        # Goal State: A is on B, B is on C, C is on table
        self.goal = {
            "A": "B",
            "B": "C",
            "C": "table"
        }

    def is_goal_state(self):
        return self.state == self.goal

    def move(self, block, destination):
        if block in self.state and self.state[block] != destination:
            print(f"Moving {block} from {self.state[block]} to {destination}")
            self.state[block] = destination

    def plan_moves(self):
        print("=" * 60)
        print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
        print("   Blocks World Planning Program")
        print("=" * 60)
        print("\nInitial State :", self.state)
        print("Goal State    :", self.goal)
        print("-" * 60)
        print("Execution Steps:")

        while not self.is_goal_state():
            for block, target in self.goal.items():
                if self.state[block] != target:
                    self.move(block, target)

        print("-" * 60)
        print("\nFinal Goal State Reached:", self.state)
        print("=" * 60)


if __name__ == "__main__":
    # Run the Blocks World Solver
    bw = BlocksWorld()
    bw.plan_moves()
