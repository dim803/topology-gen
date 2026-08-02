"""
generate_and_classify_demo.py
--------------------------------
Generates several topologies from subbases and reports their separation
axioms, including the two finite-space curiosities this project turned up:
the order topology and lower-limit topology both collapse to the discrete
topology on any finite linearly ordered set (unlike their infinite/continuum
counterparts, where they're genuinely different).
"""

from topology_gen import (
    generate_topology_from_subbasis,
    generate_topology_from_basis,
    is_topology,
    check_T0,
    check_T1,
    check_T2,
    is_discrete,
    discrete_subbasis,
    order_topology_subbasis,
    lower_limit_basis,
    initial_segment_basis,
    sierpinski_topology,
    particular_point_subbasis,
    excluded_point_subbasis,
)


def report(title, X, topology):
    print(f"\n{title}")
    print(f"  |X|={len(list(X))}, |topology|={len(topology)}, discrete={is_discrete(X, topology)}")
    valid = is_topology(X, topology)
    print(f"  valid topology: {valid.is_topology}")
    t0, _ = check_T0(X, topology)
    t1, t1_ce = check_T1(X, topology)
    t2, t2_ce = check_T2(X, topology)
    print(f"  T0={t0}  T1={t1}" + (f" (fails at {t1_ce})" if not t1 else "") +
          f"  T2={t2}" + (f" (fails at {t2_ce})" if not t2 else ""))


if __name__ == "__main__":
    X = [0, 1, 2, 3]

    report("Discrete topology", X, generate_topology_from_subbasis(X, discrete_subbasis(X)))
    report("Indiscrete topology", X, generate_topology_from_subbasis(X, []))

    report("Order topology on {0,1,2,3}", X,
           generate_topology_from_subbasis(X, order_topology_subbasis(X)))
    print("  -> collapses to discrete: every point in a finite linear order")
    print("     can be isolated by intersecting two rays around it.")

    report("Lower-limit basis on {0,1,2,3} (with the unbounded-above ray)", X,
           generate_topology_from_basis(X, lower_limit_basis(X)))
    print("  -> also discrete: unlike the actual Sorgenfrey line, a FINITE")
    print("     lower-limit space has no room for infinitely shrinking")
    print("     intervals, so every point is isolated here too.")

    report("Initial-segment basis (deliberately missing the top ray)", X,
           generate_topology_from_basis(X, initial_segment_basis(X)))
    print("  -> NOT T1: the only open set containing max(X)=3 is X itself.")

    Xs, ts = sierpinski_topology()
    report("Sierpinski space {0,1}", Xs, ts)

    report("Particular point topology (p=0)", X, generate_topology_from_subbasis(X, particular_point_subbasis(X, 0)))
    report("Excluded point topology (p=0)", X, generate_topology_from_subbasis(X, excluded_point_subbasis(X, 0)))
