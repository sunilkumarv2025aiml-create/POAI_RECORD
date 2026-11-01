"""
Task: Forward Chaining Algorithm
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the Forward Chaining inference engine.
    Forward Chaining is a data-driven reasoning technique that starts
    with known facts and iteratively applies Horn-clause inference rules
    to derive new conclusions until a goal is reached or no more facts can be inferred.
"""

from typing import List, Set, Tuple, Dict, Optional


class ForwardChainingEngine:
    """
    Inference Engine using Forward Chaining for Horn Clauses.
    Rules are represented as: Premise -> Conclusion (e.g. ['A', 'B'] -> 'C')
    """

    def __init__(self):
        # List of rules: (premises: List[str], conclusion: str)
        self.rules: List[Tuple[List[str], str]] = []
        # Set of known facts
        self.facts: Set[str] = set()

    def add_fact(self, fact: str):
        """Add an initial known atomic fact."""
        self.facts.add(fact)

    def add_rule(self, premises: List[str], conclusion: str):
        """
        Add an implication rule: IF premises THEN conclusion.
        """
        self.rules.append((premises, conclusion))

    def infer(self, goal: str) -> Tuple[bool, List[str], List[str]]:
        """
        Runs Forward Chaining to determine if `goal` can be inferred.
        Returns:
            - is_proven: True if goal reached, False otherwise
            - fired_rules: Log of rules that were triggered in order
            - derived_facts: List of all facts known at the end
        """
        # Count of unsatisfied premises for each rule
        count = [len(premises) for premises, _ in self.rules]

        # Agenda of facts to process (queue)
        agenda = list(self.facts)
        inferred = {fact: True for fact in self.facts}
        fired_rules: List[str] = []

        # If goal is already in the initial facts
        if goal in self.facts:
            return True, ["Goal already known initially"], list(self.facts)

        step = 1
        print(f"\nInitial Facts: {sorted(list(self.facts))}")
        print(f"Target Goal  : '{goal}'")
        print("-" * 60)
        print("Forward Inference Steps:")

        while agenda:
            p = agenda.pop(0)

            # Check all rules where 'p' is part of the premises
            for i, (premises, conclusion) in enumerate(self.rules):
                if p in premises:
                    count[i] -= 1

                    # When all premises for rule i are satisfied
                    if count[i] == 0:
                        if conclusion not in inferred:
                            inferred[conclusion] = True
                            self.facts.add(conclusion)
                            agenda.append(conclusion)
                            
                            rule_str = f"Step {step}: {' ^ '.join(premises)} => Derived '{conclusion}'"
                            print(f"  [FIRED] {rule_str}")
                            fired_rules.append(rule_str)
                            step += 1

                            # If target goal is derived, stop early
                            if conclusion == goal:
                                print(f"\n  [GOAL REACHED] Goal '{goal}' has been successfully inferred!")
                                return True, fired_rules, sorted(list(self.facts))

        is_proven = goal in self.facts
        return is_proven, fired_rules, sorted(list(self.facts))


def main():
    print("=" * 60)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Forward Chaining Inference Engine (Data-Driven)")
    print("=" * 60)

    engine = ForwardChainingEngine()

    # Define initial facts
    initial_facts = ['A', 'B']
    for f in initial_facts:
        engine.add_fact(f)

    # Define rule set (Horn clauses):
    # Rule 1: A AND B => C
    # Rule 2: C AND D => E
    # Rule 3: C => D
    # Rule 4: E => Z
    engine.add_rule(['A', 'B'], 'C')
    engine.add_rule(['C'], 'D')
    engine.add_rule(['C', 'D'], 'E')
    engine.add_rule(['E'], 'Z')

    print("\nKnowledge Base Rules:")
    for i, (premises, conclusion) in enumerate(engine.rules, 1):
        print(f"  Rule {i}: {' ^ '.join(premises)} => {conclusion}")

    query_goal = 'Z'
    success, fired_rules, all_facts = engine.infer(query_goal)

    print("-" * 60)
    print("Summary:")
    print(f"  Target Goal Proven? : {success}")
    print(f"  Total Facts Known   : {all_facts}")
    print(f"  Rules Fired Count   : {len(fired_rules)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
