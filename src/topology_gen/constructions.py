"""
constructions.py
-----------------
Concrete subbases/topologies to run through the generator:

  discrete_subbasis(X)          -- singletons; generates the discrete topology
  order_topology_subbasis(X)    -- rays {x : x < a}, {x : x > a} on a
                                    linearly ordered finite X (Munkres 13)
  lower_limit_basis(X)          -- half-open intervals [a, b) (already a
                                    basis; the finite analogue of the
                                    Sorgenfrey line)
  sierpinski_topology()         -- the two-point space {0,1} with
                                    topology {empty, {0}, {0,1}}: the
                                    smallest T0-not-T1 example
  particular_point_subbasis(X,p) -- generates {A : p in A} u {empty}
  excluded_point_subbasis(X,p)   -- generates {A : p not in A} u {X}
"""

from __future__ import annotations


def discrete_subbasis(X):
    return [frozenset({x}) for x in X]


def order_topology_subbasis(X_sorted):
    """
    Rays {y : y < a} and {y : y > a} for each a in a linearly ordered
    (already-sorted) finite list X_sorted. Generates the order topology.
    """
    X = list(X_sorted)
    subbasis = []
    for a in X:
        less = frozenset(y for y in X if y < a)
        greater = frozenset(y for y in X if y > a)
        subbasis.append(less)
        subbasis.append(greater)
    return subbasis


def lower_limit_basis(X_sorted):
    """
    Half-open intervals [a, b) for a < b in a sorted finite list X_sorted,
    together with the unbounded-above rays [a, +inf) = {x : x >= a} -- the
    correct finite analogue of a basis for the Sorgenfrey line. Represented
    as contiguous runs X[i:j] for 0 <= i < j <= len(X); j == len(X) is the
    unbounded-above case.

    Perhaps surprisingly, this topology is discrete: see
    `initial_segment_basis` below and the README for why omitting the
    unbounded-above ray changes this.
    """
    X = list(X_sorted)
    n = len(X)
    return [frozenset(X[i:j]) for i in range(n) for j in range(i + 1, n + 1)]


def initial_segment_basis(X_sorted):
    """
    Half-open intervals [a, b) for a < b in X_sorted, WITHOUT the
    unbounded-above ray -- i.e. every basis element other than X itself is
    a proper initial segment relative to some upper bound that is itself an
    element of X. X is included explicitly so the result is a genuine
    topology (X must be open); without it, max(X) would not appear in any
    basis element at all, and the union closure could never produce X.

    Unlike lower_limit_basis, this does not isolate the maximum element:
    the only open set containing max(X) is X itself, so this topology is
    not even T1 (max(X) can't be separated from anything). A deliberate
    example of what's lost by omitting the unbounded ray.
    """
    X = list(X_sorted)
    n = len(X)
    basis = [frozenset(X[i:j]) for i in range(n) for j in range(i + 1, n)]
    basis.append(frozenset(X))
    return basis


def sierpinski_topology():
    """The two-point Sierpinski space: X={0,1}, topology={{},{0},{0,1}}."""
    X = frozenset({0, 1})
    topology = {frozenset(), frozenset({0}), X}
    return X, topology


def particular_point_subbasis(X, p):
    """Generates the particular point topology: open sets are the empty set
    and every set containing p."""
    X = list(X)
    return [frozenset({p, x}) for x in X if x != p] + [frozenset(X)]


def excluded_point_subbasis(X, p):
    """Generates the excluded point topology: open sets are X and every set
    not containing p."""
    X = list(X)
    others = [x for x in X if x != p]
    subbasis = [frozenset({x}) for x in others]
    subbasis.append(frozenset(X))
    return subbasis
