"""
compactness.py
---------------
A space is compact iff every open cover has a finite subcover. For ANY
finite topological space this is automatic: the topology itself has at
most 2**|X| members, so any open cover -- being a sub-collection of the
topology -- is already a finite collection, and is trivially its own
finite subcover.

is_compact therefore always returns True on a finite space. It's
implemented as a genuine check (constructing an explicit finite subcover
via has_finite_subcover) rather than a hardcoded constant, so the "why" is
demonstrable rather than asserted -- the interesting content here is the
proof, not the computation.
"""

from __future__ import annotations


def has_finite_subcover(X, cover):
    """
    cover: a collection of open sets whose union is X. Returns a (finite,
    since `cover` itself is a finite collection when X is finite) sub-list
    covering X, found by greedy set cover -- not the unique minimal one,
    just a witness that one exists.
    """
    X = frozenset(X)
    cover = [frozenset(c) for c in cover]
    union = frozenset().union(*cover) if cover else frozenset()
    if union != X:
        raise ValueError("the given cover does not actually cover X")

    remaining = set(X)
    remaining_sets = list(cover)
    chosen = []
    while remaining:
        best = max(remaining_sets, key=lambda s: len(s & remaining))
        chosen.append(best)
        remaining -= best
        remaining_sets.remove(best)
    return chosen


def is_compact(X, topology):
    """
    Always True for a finite space -- see module docstring. Verified here
    by actually constructing a finite subcover of the full topology (the
    largest possible open cover of X), rather than asserted outright.
    """
    all_open_sets = [frozenset(t) for t in topology if len(frozenset(t)) > 0]
    has_finite_subcover(X, all_open_sets)  # raises if something is actually wrong
    return True
