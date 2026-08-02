import random

from topology_gen import (
    generate_basis_from_subbasis,
    generate_topology_from_basis,
    generate_topology_from_subbasis,
    is_topology,
    check_T0,
    check_T1,
    check_T2,
    check_T1_via_closed_singletons,
    closed_sets,
    is_discrete,
    is_indiscrete,
    compare_topologies,
    discrete_subbasis,
    order_topology_subbasis,
    lower_limit_basis,
    initial_segment_basis,
    sierpinski_topology,
    particular_point_subbasis,
    excluded_point_subbasis,
)


# ---------------------------------------------------------------------- #
# Generator correctness
# ---------------------------------------------------------------------- #

def test_discrete_subbasis_generates_full_power_set():
    X = [0, 1, 2]
    t = generate_topology_from_subbasis(X, discrete_subbasis(X))
    assert len(t) == 2 ** len(X)
    assert is_discrete(X, t)


def test_empty_subbasis_generates_indiscrete_topology():
    X = [0, 1, 2]
    t = generate_topology_from_subbasis(X, [])
    assert t == {frozenset(), frozenset(X)}
    assert is_indiscrete(X, t)


def test_generated_topology_is_always_a_valid_topology():
    # generator output should satisfy is_topology across many random subbases
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 6)
        X = list(range(n))
        k = rng.randint(0, 4)
        subbasis = [frozenset(rng.sample(X, rng.randint(0, n))) for _ in range(k)]
        t = generate_topology_from_subbasis(X, subbasis)
        report = is_topology(X, t)
        assert report.is_topology, f"generator produced an invalid topology for X={X}, subbasis={subbasis}"


def test_basis_from_subbasis_contains_x_and_is_closed_under_intersection():
    X = [0, 1, 2, 3]
    subbasis = [frozenset({0, 1}), frozenset({1, 2}), frozenset({2, 3})]
    basis = generate_basis_from_subbasis(X, subbasis)
    assert frozenset(X) in basis
    members = list(basis)
    for a in members:
        for b in members:
            assert (a & b) in basis


# ---------------------------------------------------------------------- #
# Order topology and lower-limit basis on finite sets
# ---------------------------------------------------------------------- #

def test_order_topology_on_finite_set_is_discrete():
    # every point in a finite linearly ordered set can be isolated via two rays
    for n in [1, 2, 3, 5]:
        X = list(range(n))
        t = generate_topology_from_subbasis(X, order_topology_subbasis(X))
        assert is_discrete(X, t), f"order topology on {n} points should be discrete"


def test_correct_lower_limit_basis_on_finite_set_is_discrete():
    # with the unbounded-above ray included, this is also discrete on any finite X
    for n in [1, 2, 3, 5]:
        X = list(range(n))
        t = generate_topology_from_basis(X, lower_limit_basis(X))
        assert is_discrete(X, t)


def test_initial_segment_basis_is_not_t1():
    X = [0, 1, 2, 3]
    t = generate_topology_from_basis(X, initial_segment_basis(X))
    assert is_topology(X, t).is_topology
    t0, _ = check_T0(X, t)
    t1, ce = check_T1(X, t)
    assert t0
    assert not t1
    assert ce is not None
    # the max element should be the one that can't be separated
    assert max(X) in ce


# ---------------------------------------------------------------------- #
# Separation axioms on known examples
# ---------------------------------------------------------------------- #

def test_sierpinski_space_is_t0_not_t1_not_t2():
    X, t = sierpinski_topology()
    assert check_T0(X, t)[0]
    assert not check_T1(X, t)[0]
    assert not check_T2(X, t)[0]


def test_particular_point_topology_is_t0_not_t1():
    X = [0, 1, 2, 3]
    t = generate_topology_from_subbasis(X, particular_point_subbasis(X, 0))
    assert check_T0(X, t)[0]
    assert not check_T1(X, t)[0]


def test_excluded_point_topology_is_t0_not_t1():
    X = [0, 1, 2, 3]
    t = generate_topology_from_subbasis(X, excluded_point_subbasis(X, 0))
    assert check_T0(X, t)[0]
    assert not check_T1(X, t)[0]


def test_t1_check_matches_closed_singletons_characterization():
    # cross-validate check_T1 against the independent "singletons are closed" characterization
    examples = []
    X1, t1 = sierpinski_topology()
    examples.append((X1, t1))
    X2 = [0, 1, 2, 3]
    examples.append((X2, generate_topology_from_subbasis(X2, discrete_subbasis(X2))))
    examples.append((X2, generate_topology_from_subbasis(X2, particular_point_subbasis(X2, 0))))
    examples.append((X2, generate_topology_from_basis(X2, initial_segment_basis(X2))))

    for X, t in examples:
        direct, _ = check_T1(X, t)
        via_closed, _ = check_T1_via_closed_singletons(X, t)
        assert direct == via_closed


# ---------------------------------------------------------------------- #
# The central theorem: finite T1 spaces are discrete (hence T1 <=> T2 <=> discrete)
# ---------------------------------------------------------------------- #

def test_finite_t1_implies_discrete_and_hausdorff():
    """
    Classical fact: every finite T1 topological space is discrete (for any
    x, {x} is the intersection of the finitely many open sets containing x
    but excluding each other point -- a finite intersection of opens is
    open). Consequently T1 => T2 for finite spaces, even though T1 does not
    imply T2 in general topology. Checked here across many randomly
    generated finite topologies, not just the hand-picked examples above.
    """
    rng = random.Random(42)
    checked_t1_examples = 0
    for _ in range(500):
        n = rng.randint(1, 6)
        X = list(range(n))
        k = rng.randint(0, 5)
        subbasis = [frozenset(rng.sample(X, rng.randint(0, n))) for _ in range(k)]
        t = generate_topology_from_subbasis(X, subbasis)

        is_t1, _ = check_T1(X, t)
        if is_t1:
            checked_t1_examples += 1
            assert is_discrete(X, t), f"found a finite T1 space that is NOT discrete: X={X}"
            is_t2, _ = check_T2(X, t)
            assert is_t2, f"found a finite T1 space that is NOT T2: X={X}"

    assert checked_t1_examples > 0  # sanity check the loop actually exercised some T1 cases


def test_t2_implies_t1_implies_t0_on_random_examples():
    """The general implication chain T2 => T1 => T0 always holds, checked broadly."""
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 6)
        X = list(range(n))
        k = rng.randint(0, 5)
        subbasis = [frozenset(rng.sample(X, rng.randint(0, n))) for _ in range(k)]
        t = generate_topology_from_subbasis(X, subbasis)

        is_t0, _ = check_T0(X, t)
        is_t1, _ = check_T1(X, t)
        is_t2, _ = check_T2(X, t)

        if is_t2:
            assert is_t1
        if is_t1:
            assert is_t0


# ---------------------------------------------------------------------- #
# Closed sets and comparing topologies
# ---------------------------------------------------------------------- #

def test_closed_sets_are_complements_of_open_sets():
    X = [0, 1, 2]
    t = generate_topology_from_subbasis(X, discrete_subbasis(X))
    closed = closed_sets(X, t)
    X_fs = frozenset(X)
    for U in t:
        assert (X_fs - U) in closed


def test_compare_topologies_discrete_is_finer_than_everything():
    X = [0, 1, 2]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    indiscrete = generate_topology_from_subbasis(X, [])
    order_t = generate_topology_from_subbasis(X, order_topology_subbasis(X))

    assert compare_topologies(discrete, indiscrete) == "finer"
    assert compare_topologies(indiscrete, discrete) == "coarser"
    assert compare_topologies(discrete, discrete) == "equal"
    assert compare_topologies(discrete, order_t) in ("finer", "equal")  # order_t is discrete here too


def test_compare_topologies_incomparable_case():
    X = [0, 1, 2]
    t1 = {frozenset(), frozenset({0}), frozenset(X)}
    t2 = {frozenset(), frozenset({1}), frozenset(X)}
    assert compare_topologies(t1, t2) == "incomparable"
