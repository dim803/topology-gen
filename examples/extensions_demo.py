"""
extensions_demo.py
--------------------
Tours the four extensions: continuity/homeomorphisms, connectedness,
compactness, and T3/T4 -- including the extended central finding that all
of T1, T2, T3, T4, and "discrete" coincide on any finite space.
"""

from topology_gen import (
    generate_topology_from_subbasis,
    discrete_subbasis,
    sierpinski_topology,
    particular_point_subbasis,
    is_connected,
    connected_components,
    is_compact,
    is_continuous,
    is_homeomorphism,
    check_T3,
    check_T4,
)


if __name__ == "__main__":
    X = [0, 1, 2, 3]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    indiscrete = generate_topology_from_subbasis(X, [])

    print("=== Connectedness ===")
    print(f"discrete on {X}: connected = {is_connected(X, discrete)}, "
          f"components = {connected_components(X, discrete)}")
    print(f"indiscrete on {X}: connected = {is_connected(X, indiscrete)}, "
          f"components = {connected_components(X, indiscrete)}")

    Xs, ts = sierpinski_topology()
    print(f"Sierpinski space: connected = {is_connected(Xs, ts)} "
          f"(only clopen sets are the empty set and X itself)")

    print("\n=== Compactness ===")
    print("Every finite topological space is compact -- checked directly, not assumed:")
    print(f"  discrete: {is_compact(X, discrete)}")
    print(f"  indiscrete: {is_compact(X, indiscrete)}")

    print("\n=== Continuity ===")
    identity = {x: x for x in X}
    print(f"identity: discrete -> indiscrete continuous = "
          f"{is_continuous(X, discrete, identity, indiscrete)[0]}  (always true: "
          f"finer to coarser)")
    print(f"identity: indiscrete -> discrete continuous = "
          f"{is_continuous(X, indiscrete, identity, discrete)[0]}  (fails: "
          f"coarser to finer, in general)")
    print(f"identity: discrete -> discrete is a homeomorphism = "
          f"{is_homeomorphism(X, discrete, identity, X, discrete, identity)[0]}")

    print("\n=== T3 / T4 ===")
    print(f"discrete: T3 = {check_T3(X, discrete)[0]}, T4 = {check_T4(X, discrete)[0]}")
    print(f"Sierpinski (not T1): T3 = {check_T3(Xs, ts)[0]}, T4 = {check_T4(Xs, ts)[0]}")

    print("\n=== The extended theorem ===")
    print("On any finite space: T1 <=> T2 <=> T3 <=> T4 <=> discrete.")
    print("Munkres bakes T1 into the definitions of T3 (regular) and T4 (normal);")
    print("since finite T1 spaces are already discrete (and discrete spaces are")
    print("trivially regular and normal), all five properties collapse together.")
    print("Verified across 500 random finite topologies in tests/test_extensions.py.")
