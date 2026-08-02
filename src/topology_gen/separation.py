"""
separation.py
--------------
Separation axioms for a finite topological space (X, topology), each
returning (bool, counterexample or None):

  T0 (Kolmogorov): for distinct x,y, some open set contains exactly one of
                    them (not both, not neither).
  T1 (Frechet):     for distinct x,y, some open set contains x but not y,
                    AND some open set contains y but not x (both directions).
                    Equivalent to: every singleton {x} is closed.
  T2 (Hausdorff):   for distinct x,y, some disjoint open sets separate them.

Also: closed_sets, is_discrete, and compare_topologies (finer/coarser).
"""

from __future__ import annotations
from itertools import combinations


def check_T0(X, topology):
    X = list(X)
    topology = [frozenset(t) for t in topology]
    for x, y in combinations(X, 2):
        if any((x in U) != (y in U) for U in topology):
            continue
        return False, (x, y)
    return True, None


def check_T1(X, topology):
    X = list(X)
    topology = [frozenset(t) for t in topology]
    for x, y in combinations(X, 2):
        has_x_not_y = any(x in U and y not in U for U in topology)
        has_y_not_x = any(y in U and x not in U for U in topology)
        if not (has_x_not_y and has_y_not_x):
            return False, (x, y)
    return True, None


def check_T2(X, topology):
    X = list(X)
    topology = [frozenset(t) for t in topology]
    for x, y in combinations(X, 2):
        separated = any(
            x in U and y in V and not (U & V)
            for U in topology for V in topology
        )
        if not separated:
            return False, (x, y)
    return True, None


def is_regular_space(X, topology):
    """
    Regular (without assuming T1): for every closed set C and point x not in
    C, some disjoint open sets separate {x} and C. Returns (bool, (x, C) or
    None). This is the "regular" property alone; check_T3 below adds T1, per
    Munkres's convention (T3 = regular + T1).
    """
    X = list(X)
    topology = [frozenset(t) for t in topology]
    closed = closed_sets(X, topology)
    for x in X:
        for C in closed:
            if x in C:
                continue
            separated = any(
                x in U and C <= V and not (U & V)
                for U in topology for V in topology
            )
            if not separated:
                return False, (x, C)
    return True, None


def is_normal_space(X, topology):
    """
    Normal (without assuming T1): every pair of disjoint closed sets is
    separated by disjoint open sets. Returns (bool, (C, D) or None).
    check_T4 below adds T1, per Munkres's convention (T4 = normal + T1).
    """
    topology = [frozenset(t) for t in topology]
    closed = list(closed_sets(X, topology))
    for i, C in enumerate(closed):
        for D in closed[i + 1:]:
            if C & D:
                continue  # not disjoint; the axiom says nothing about this pair
            separated = any(
                C <= U and D <= V and not (U & V)
                for U in topology for V in topology
            )
            if not separated:
                return False, (C, D)
    return True, None


def check_T3(X, topology):
    """Regular (Munkres): T1 and is_regular_space. Returns (bool, reason)."""
    t1, ce = check_T1(X, topology)
    if not t1:
        return False, ("T1 fails", ce)
    regular, ce = is_regular_space(X, topology)
    if not regular:
        return False, ("regularity fails", ce)
    return True, None


def check_T4(X, topology):
    """Normal (Munkres): T1 and is_normal_space. Returns (bool, reason)."""
    t1, ce = check_T1(X, topology)
    if not t1:
        return False, ("T1 fails", ce)
    normal, ce = is_normal_space(X, topology)
    if not normal:
        return False, ("normality fails", ce)
    return True, None


def closed_sets(X, topology):
    """The closed sets of (X, topology): complements of the open sets."""
    X = frozenset(X)
    return {X - frozenset(U) for U in topology}


def check_T1_via_closed_singletons(X, topology):
    """
    Cross-check for T1: a space is T1 iff every singleton is closed. Returns
    (bool, offending_point or None). Used to validate check_T1 against an
    independent characterization, not just trust one implementation.
    """
    closed = closed_sets(X, topology)
    for x in X:
        if frozenset({x}) not in closed:
            return False, x
    return True, None


def is_discrete(X, topology):
    """True iff every subset of X is open (the topology is the full power set)."""
    X = frozenset(X)
    topology = {frozenset(t) for t in topology}
    return len(topology) == 2 ** len(X)


def is_indiscrete(X, topology):
    """True iff the only open sets are the empty set and X."""
    X = frozenset(X)
    topology = {frozenset(t) for t in topology}
    return topology == {frozenset(), X}


def compare_topologies(topology1, topology2) -> str:
    """
    Compares two topologies on the same set X by inclusion:
      'finer'        if topology1 properly contains topology2
      'coarser'      if topology1 is properly contained in topology2
      'equal'        if they're the same collection
      'incomparable' otherwise
    ("finer" = more open sets = higher-resolution; the discrete topology is
    the finest possible, the indiscrete topology the coarsest.)
    """
    t1 = {frozenset(t) for t in topology1}
    t2 = {frozenset(t) for t in topology2}
    if t1 == t2:
        return "equal"
    if t2 <= t1:
        return "finer"
    if t1 <= t2:
        return "coarser"
    return "incomparable"
