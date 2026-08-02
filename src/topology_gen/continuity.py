"""
continuity.py
--------------
f: X -> Y is continuous iff the preimage of every open set in Y is open in
X. f is given as a dict mapping each element of X to its image in Y.
"""

from __future__ import annotations


def preimage(f: dict, V) -> frozenset:
    V = frozenset(V)
    return frozenset(x for x, y in f.items() if y in V)


def is_continuous(X, topology_X, f: dict, topology_Y):
    """
    Returns (bool, V or None): V is an open set of Y whose preimage under f
    is NOT open in X, if continuity fails.
    """
    topology_X_fs = {frozenset(t) for t in topology_X}
    for V in topology_Y:
        if preimage(f, V) not in topology_X_fs:
            return False, frozenset(V)
    return True, None


def is_homeomorphism(X, topology_X, f: dict, Y, topology_Y, f_inv: dict):
    """
    Checks that f: X -> Y and f_inv: Y -> X are mutually inverse bijections
    and that both f and f_inv are continuous -- i.e. f is a homeomorphism.
    Returns (bool, reason or None).
    """
    X, Y = list(X), list(Y)

    if sorted(f.keys()) != sorted(X) or sorted(f.values()) != sorted(Y):
        return False, "f is not a bijection X -> Y"
    if sorted(f_inv.keys()) != sorted(Y) or sorted(f_inv.values()) != sorted(X):
        return False, "f_inv is not a bijection Y -> X"
    if any(f_inv[f[x]] != x for x in X):
        return False, "f_inv is not the inverse of f"

    cont_forward, ce = is_continuous(X, topology_X, f, topology_Y)
    if not cont_forward:
        return False, ("f is not continuous", ce)

    cont_backward, ce = is_continuous(Y, topology_Y, f_inv, topology_X)
    if not cont_backward:
        return False, ("f_inv is not continuous", ce)

    return True, None
