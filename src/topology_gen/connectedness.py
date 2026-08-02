"""
connectedness.py
-----------------
A space is connected iff its only clopen (simultaneously open and closed)
subsets are the empty set and X itself -- equivalently, iff it cannot be
partitioned into two nonempty disjoint open sets.

For a FINITE space, the clopen sets form a finite Boolean algebra under
intersection/union, and its atoms (minimal nonempty clopen sets) are
exactly the connected components: component(x) is the intersection of
every clopen set containing x, which is itself clopen (a finite
intersection of clopen sets), nonempty (it contains x), and minimal by
construction.
"""

from __future__ import annotations

from .separation import closed_sets


def clopen_sets(X, topology):
    """Every subset that is both open (in `topology`) and closed."""
    topology_fs = {frozenset(t) for t in topology}
    closed = closed_sets(X, topology)
    return topology_fs & closed


def connected_components(X, topology):
    """
    The connected components of (X, topology), as a list of disjoint
    frozensets whose union is X.
    """
    X = list(X)
    clopen = list(clopen_sets(X, topology))

    components = []
    seen = set()
    for x in X:
        if x in seen:
            continue
        component = frozenset(X)
        for C in clopen:
            if x in C:
                component &= C
        components.append(component)
        seen |= component
    return components


def is_connected(X, topology):
    """True iff (X, topology) has exactly one connected component."""
    return len(connected_components(X, topology)) == 1
