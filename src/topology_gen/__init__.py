"""
topology_gen
------------
Generates the topology induced by a subbasis on a finite set, validates
topology axioms, and checks separation axioms (T0 through T4), continuity,
connectedness, and compactness -- with counterexamples wherever an axiom
fails.
"""

from .generator import (
    generate_basis_from_subbasis,
    generate_topology_from_basis,
    generate_topology_from_subbasis,
)
from .validate import is_topology, TopologyValidationReport
from .separation import (
    check_T0,
    check_T1,
    check_T2,
    check_T3,
    check_T4,
    is_regular_space,
    is_normal_space,
    check_T1_via_closed_singletons,
    closed_sets,
    is_discrete,
    is_indiscrete,
    compare_topologies,
)
from .connectedness import connected_components, is_connected, clopen_sets
from .compactness import is_compact, has_finite_subcover
from .continuity import is_continuous, is_homeomorphism, preimage
from .constructions import (
    discrete_subbasis,
    order_topology_subbasis,
    lower_limit_basis,
    initial_segment_basis,
    sierpinski_topology,
    particular_point_subbasis,
    excluded_point_subbasis,
)

__all__ = [
    "generate_basis_from_subbasis",
    "generate_topology_from_basis",
    "generate_topology_from_subbasis",
    "is_topology",
    "TopologyValidationReport",
    "check_T0",
    "check_T1",
    "check_T2",
    "check_T3",
    "check_T4",
    "is_regular_space",
    "is_normal_space",
    "check_T1_via_closed_singletons",
    "closed_sets",
    "is_discrete",
    "is_indiscrete",
    "compare_topologies",
    "connected_components",
    "is_connected",
    "clopen_sets",
    "is_compact",
    "has_finite_subcover",
    "is_continuous",
    "is_homeomorphism",
    "preimage",
    "discrete_subbasis",
    "order_topology_subbasis",
    "lower_limit_basis",
    "initial_segment_basis",
    "sierpinski_topology",
    "particular_point_subbasis",
    "excluded_point_subbasis",
]
