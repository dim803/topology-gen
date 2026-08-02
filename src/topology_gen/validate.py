"""
validate.py
-----------
Checks whether a given collection of subsets of a finite X is actually a
topology: contains X and the empty set, and is closed under (finite, hence
here equivalently arbitrary, since X is finite) union and intersection.
Since X is finite, checking closure under *pairwise* union and intersection
of the collection's own members is exactly equivalent to full closure under
arbitrary unions/intersections -- there are only finitely many members to
combine in the first place.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TopologyValidationReport:
    is_topology: bool
    contains_empty_set: bool
    contains_whole_set: bool
    closed_under_union: bool
    union_counterexample: tuple | None
    closed_under_intersection: bool
    intersection_counterexample: tuple | None

    def summary(self) -> str:
        lines = [f"Is a topology: {self.is_topology}"]
        lines.append(f"  contains empty set: {self.contains_empty_set}")
        lines.append(f"  contains whole set: {self.contains_whole_set}")
        lines.append(f"  closed under union: {self.closed_under_union}" +
                      ("" if self.closed_under_union else f"  (fails at {self.union_counterexample})"))
        lines.append(f"  closed under intersection: {self.closed_under_intersection}" +
                      ("" if self.closed_under_intersection else f"  (fails at {self.intersection_counterexample})"))
        return "\n".join(lines)


def is_topology(X, collection) -> TopologyValidationReport:
    X = frozenset(X)
    collection = {frozenset(c) for c in collection}

    contains_empty = frozenset() in collection
    contains_whole = X in collection

    closed_under_union = True
    union_ce = None
    closed_under_intersection = True
    intersection_ce = None

    members = list(collection)
    for i, a in enumerate(members):
        for b in members[i:]:
            if closed_under_union and (a | b) not in collection:
                closed_under_union = False
                union_ce = (a, b)
            if closed_under_intersection and (a & b) not in collection:
                closed_under_intersection = False
                intersection_ce = (a, b)
        if not closed_under_union and not closed_under_intersection:
            break

    valid = contains_empty and contains_whole and closed_under_union and closed_under_intersection

    return TopologyValidationReport(
        is_topology=valid,
        contains_empty_set=contains_empty,
        contains_whole_set=contains_whole,
        closed_under_union=closed_under_union,
        union_counterexample=union_ce,
        closed_under_intersection=closed_under_intersection,
        intersection_counterexample=intersection_ce,
    )
