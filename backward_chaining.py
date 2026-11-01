"""
Task: Backward Chaining Algorithm
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the Backward Chaining inference engine.
    Backward Chaining is a goal-driven reasoning technique that starts
    with a goal (query) and works backwards through Horn-clause rules 
    to determine if the goal can be proven from the known facts.
"""

from typing import Dict, List, Set, Tuple, Optional


class BackwardChainingEngine:
    """
    Inference Engine using Backward Chaining for Horn Clauses.
    Rules are represented as: Premise -> Conclusion (e.g. ['A', 'B'] -> 'C')
    """

    def __init__(self):
        # List of rules: (premises: List[str], conclusion: str)
        self.rules: List[Tuple[List[str], str]] = []
        # Set of known facts
        self.facts: Set[str] = set()

    def add_fact(self, fact: str):
        """Add a known atomic fact to the knowledge base."""
        self.facts.add(fact)

    def add_rule(self, premises: List[str], conclusion: str):
        """
        Add an implication rule: IF premises THEN conclusion.
        """
        self.rules.append((premises, conclusion))

    def prove(self, goal: str, visited: Optional[Set[str]] = None, indent: int = 0) -> bool:
        """
        Backward chaining algorithm to prove a goal.
        Returns True if the goal is entails by the KB, False otherwise.
        """
        if visited is None:
            visited = set()

        prefix = "  " * indent
        print(f"{prefix}--> Evaluating Goal: '{goal}'")

        # 1. Base Case: If goal is already a known fact
        if goal in self.facts:
            print(f"{prefix}    [MATCH] '{goal}' is a known fact.")
            return True

        # 2. Cycle Detection: Avoid infinite loops in recursive rules
        if goal in visited:
            print(f"{prefix}    [CYCLE DETECTED] Already exploring '{goal}', backtracking.")
            return False

        visited.add(goal)

        # 3. Find rules that conclude this goal
        applicable_rules = [rule for rule in self.rules if rule[1] == goal]
        if not applicable_rules:
            print(f"{prefix}    [NO RULE] No rule concludes '{goal}'.")
            visited.remove(goal)
            return False

        for i, (premises, conclusion) in enumerate(applicable_rules, 1):
            print(f"{prefix}    Trying Rule {i}: {' AND '.join(premises)} => {conclusion}")
            
            # Check if ALL premises of this rule can be proved (conjunction)
            all_premises_satisfied = True
            for premise in premises:
                if not self.prove(premise, visited.copy(), indent + 2):
                    all_premises_satisfied = False
                    break

            if all_premises_satisfied:
                print(f"{prefix}    [SUCCESS] Rule {i} succeeded! '{goal}' is PROVEN.")
                # Cache proven goal as a new fact
                self.facts.add(goal)
                return True

        print(f"{prefix}    [FAILED] All rules for '{goal}' failed.")
        return False


def main():
    print("=" * 60)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Backward Chaining Inference Engine (Goal-Driven)")
    print("=" * 60)

    kb = BackwardChainingEngine()

    # Define known facts
    initial_facts = ['B', 'D', 'F']
    for fact in initial_facts:
        kb.add_fact(fact)

    # Define rules:
    # Rule 1: A AND B => C
    # Rule 2: C AND D => E
    # Rule 3: F => A
    kb.add_rule(['A', 'B'], 'C')
    kb.add_rule(['C', 'D'], 'E')
    kb.add_rule(['F'], 'A')

    print("\nKnowledge Base:")
    print(f"  Facts : {list(kb.facts)}")
    print("  Rules :")
    for premises, conclusion in kb.rules:
        print(f"    {' ^ '.join(premises)} => {conclusion}")

    query_goal = 'E'
    print(f"\nQuery Goal to Prove: '{query_goal}'")
    print("-" * 60)
    print("Inference Trace:")

    # Execute backward chaining
    result = kb.prove(query_goal)

    print("-" * 60)
    print(f"Result : Goal '{query_goal}' {'is PROVEN' if result else 'CANNOT be proven'} from the KB.")
    print(f"Updated Facts Base: {sorted(list(kb.facts))}")
    print("=" * 60)


if __name__ == "__main__":
    main()
