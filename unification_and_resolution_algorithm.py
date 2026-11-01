"""
Task: Unification and Resolution Algorithm
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the Unification and Resolution algorithm in First-Order Logic (FOL).
    - Unification: Finds a substitution theta that makes two logical predicates identical.
    - Resolution: Infers whether a query goal can be resolved from a given Knowledge Base (KB).
"""

import re


# Function to check if two predicates can be unified
def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if x == y:
        return theta
    elif isinstance(x, str) and x.islower():  # x is a variable (lowercase)
        return unify_var(x, y, theta)
    elif isinstance(y, str) and y.islower():  # y is a variable (lowercase)
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        t = unify(x[0], y[0], theta)
        if t is None:
            return None
        return unify(x[1:], y[1:], t)
    else:
        return None


# Function to unify a variable with a term
def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta


# Apply variable substitutions (theta) to a clause
def apply_theta(clause, theta):
    if isinstance(clause, str):
        return theta.get(clause, clause)
    elif isinstance(clause, list):
        return [apply_theta(item, theta) for item in clause]
    return clause


# Function to apply resolution rule
def resolution(kb, query):
    for clause in kb:
        theta = unify(clause[0], query, {})
        if theta is not None:
            new_kb = [apply_theta(c, theta) for c in clause[1:]]
            if not new_kb:  # If empty, means query is resolved
                return True
            else:
                return resolution(kb, new_kb[0])
    return False


# Knowledge base (Implications in Horn Clause form: [Head/Conclusion, Body/Premise...])
# Rule: Mortal(x) :- Human(x)  [All humans are mortal: Human(x) -> Mortal(x)]
# Fact: Human(John)            [John is human]
fact = ["Human", "John"]

knowledge_base = [
    [["Mortal", "x"], ["Human", "x"]],  # Human(x) → Mortal(x)
    [fact]                               # Fact: Human(John)
]

# Query: Mortal(John)? [Is John mortal?]
query = ["Mortal", "John"]

# Main Execution
def main():
    print("=" * 60)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Unification and Resolution Algorithm")
    print("=" * 60)
    print(f"Knowledge Base : {knowledge_base}")
    print(f"Fact           : {fact}")
    print(f"Query Goal     : {query}")
    print("-" * 60)

    # Apply resolution
    if resolution(knowledge_base, query):
        print("Query is resolved: John is Mortal")
    else:
        print("Query could not be resolved")
    print("=" * 60)


if __name__ == "__main__":
    main()
