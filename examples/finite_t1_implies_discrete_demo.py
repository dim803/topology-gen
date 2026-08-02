"""
finite_t1_implies_discrete_demo.py
--------------------------------------
Classical theorem: every finite T1 topological space is discrete (and hence
T1 and T2 coincide for finite spaces, even though T1 does not imply T2 in
general topology). This script generates many random topologies on small
finite sets and confirms the theorem holds for every one that turns out to
be T1 -- the same "generate lots of cases and check a real theorem
computationally" approach used in the other repos in this series.
"""

import random

from topology_gen import (
    generate_topology_from_subbasis,
    check_T0,
    check_T1,
    check_T2,
    is_discrete,
)


def random_subbasis(rng, X, max_sets):
    k = rng.randint(0, max_sets)
    return [frozenset(rng.sample(X, rng.randint(0, len(X)))) for _ in range(k)]


if __name__ == "__main__":
    rng = random.Random(123)
    trials = 2000
    t1_count = 0
    t1_and_discrete_count = 0
    t1_and_t2_count = 0

    for _ in range(trials):
        n = rng.randint(1, 6)
        X = list(range(n))
        subbasis = random_subbasis(rng, X, max_sets=5)
        topology = generate_topology_from_subbasis(X, subbasis)

        is_t1, _ = check_T1(X, topology)
        if is_t1:
            t1_count += 1
            if is_discrete(X, topology):
                t1_and_discrete_count += 1
            is_t2, _ = check_T2(X, topology)
            if is_t2:
                t1_and_t2_count += 1

    print(f"Generated {trials} random finite topologies.")
    print(f"  {t1_count} of them were T1.")
    print(f"  Of those, {t1_and_discrete_count} were discrete "
          f"({'ALL of them' if t1_and_discrete_count == t1_count else 'NOT all!'}).")
    print(f"  Of those, {t1_and_t2_count} were also T2 "
          f"({'ALL of them' if t1_and_t2_count == t1_count else 'NOT all!'}).")
    print()
    if t1_count == t1_and_discrete_count == t1_and_t2_count:
        print("Confirms the theorem: every T1 example found was discrete, and every")
        print("T1 example found was also T2 -- consistent with 'finite T1 => discrete'.")
    else:
        print("Found a counterexample to the theorem -- this would indicate a bug.")
