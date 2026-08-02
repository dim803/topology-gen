import random

from topology_gen import (
    generate_topology_from_subbasis,
    generate_topology_from_basis,
    discrete_subbasis,
    order_topology_subbasis,
    initial_segment_basis,
    sierpinski_topology,
    particular_point_subbasis,
    is_connected,
    connected_components,
    clopen_sets,
    is_compact,
    has_finite_subcover,
    is_continuous,
    is_homeomorphism,
    check_T1,
    check_T2,
    check_T3,
    check_T4,
    is_regular_space,
    is_normal_space,
    is_discrete,
)


# ---------------------------------------------------------------------- #
# Connectedness
# ---------------------------------------------------------------------- #

def test_discrete_topology_is_totally_disconnected():
    X = [0, 1, 2, 3]
    t = generate_topology_from_subbasis(X, discrete_subbasis(X))
    assert not is_connected(X, t)
    components = connected_components(X, t)
    assert len(components) == len(X)
    assert all(len(c) == 1 for c in components)


def test_indiscrete_topology_is_connected():
    X = [0, 1, 2, 3]
    t = generate_topology_from_subbasis(X, [])
    assert is_connected(X, t)
    assert connected_components(X, t) == [frozenset(X)]


def test_sierpinski_space_is_connected():
    # only clopen sets are {} and X, since {0} is open but its complement
    # {1} is not open (not in the topology), so {0} is not closed
    X, t = sierpinski_topology()
    assert is_connected(X, t)
    assert clopen_sets(X, t) == {frozenset(), frozenset(X)}


def test_components_partition_x():
    X = [0, 1, 2, 3, 4]
    t = generate_topology_from_basis(X, initial_segment_basis(X))
    components = connected_components(X, t)
    union = frozenset().union(*components)
    assert union == frozenset(X)
    # disjoint
    for i, c1 in enumerate(components):
        for c2 in components[i + 1:]:
            assert not (c1 & c2)


# ---------------------------------------------------------------------- #
# Compactness -- trivial for finite spaces, but genuinely checked
# ---------------------------------------------------------------------- #

def test_compactness_holds_for_every_finite_topology():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(1, 6)
        X = list(range(n))
        k = rng.randint(0, 5)
        subbasis = [frozenset(rng.sample(X, rng.randint(0, n))) for _ in range(k)]
        t = generate_topology_from_subbasis(X, subbasis)
        assert is_compact(X, t)


def test_has_finite_subcover_actually_covers_x():
    X = [0, 1, 2, 3]
    t = generate_topology_from_subbasis(X, discrete_subbasis(X))
    all_opens = [frozenset(s) for s in t if len(frozenset(s)) > 0]
    subcover = has_finite_subcover(X, all_opens)
    assert frozenset().union(*subcover) == frozenset(X)


def test_has_finite_subcover_rejects_a_cover_that_misses_a_point():
    X = [0, 1, 2]
    bad_cover = [frozenset({0}), frozenset({1})]  # doesn't cover 2
    try:
        has_finite_subcover(X, bad_cover)
        assert False, "should have raised"
    except ValueError:
        pass


# ---------------------------------------------------------------------- #
# Continuity
# ---------------------------------------------------------------------- #

def test_identity_from_finer_to_coarser_is_continuous():
    X = [0, 1, 2]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    indiscrete = generate_topology_from_subbasis(X, [])
    f = {x: x for x in X}
    is_cont, ce = is_continuous(X, discrete, f, indiscrete)
    assert is_cont


def test_identity_from_coarser_to_finer_is_not_continuous_in_general():
    X = [0, 1, 2]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    indiscrete = generate_topology_from_subbasis(X, [])
    f = {x: x for x in X}
    is_cont, ce = is_continuous(X, indiscrete, f, discrete)
    assert not is_cont
    assert ce is not None


def test_constant_map_is_always_continuous():
    X = [0, 1, 2]
    Y = [0, 1, 2]
    discrete_X = generate_topology_from_subbasis(X, discrete_subbasis(X))
    discrete_Y = generate_topology_from_subbasis(Y, discrete_subbasis(Y))
    indiscrete_X = generate_topology_from_subbasis(X, [])

    f_const = {x: 0 for x in X}
    assert is_continuous(X, discrete_X, f_const, discrete_Y)[0]
    assert is_continuous(X, indiscrete_X, f_const, discrete_Y)[0]


def test_identity_is_a_homeomorphism():
    X = [0, 1, 2]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    f = {x: x for x in X}
    is_homeo, reason = is_homeomorphism(X, discrete, f, X, discrete, f)
    assert is_homeo


def test_discrete_and_indiscrete_are_not_homeomorphic():
    X = [0, 1, 2]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    indiscrete = generate_topology_from_subbasis(X, [])
    f = {x: x for x in X}
    is_homeo, reason = is_homeomorphism(X, discrete, f, X, indiscrete, f)
    assert not is_homeo


def test_homeomorphism_rejects_non_bijective_map():
    X = [0, 1, 2]
    discrete = generate_topology_from_subbasis(X, discrete_subbasis(X))
    f_not_bijective = {0: 0, 1: 0, 2: 2}  # not injective
    f_inv = {0: 0, 2: 2}
    is_homeo, reason = is_homeomorphism(X, discrete, f_not_bijective, X, discrete, f_inv)
    assert not is_homeo


# ---------------------------------------------------------------------- #
# T3 / T4
# ---------------------------------------------------------------------- #

def test_discrete_topology_is_t3_and_t4():
    X = [0, 1, 2, 3]
    t = generate_topology_from_subbasis(X, discrete_subbasis(X))
    assert check_T3(X, t)[0]
    assert check_T4(X, t)[0]


def test_non_t1_spaces_fail_t3_and_t4_immediately():
    X, t = sierpinski_topology()
    t3, reason = check_T3(X, t)
    t4, reason4 = check_T4(X, t)
    assert not t3 and reason[0] == "T1 fails"
    assert not t4 and reason4[0] == "T1 fails"

    Y = [0, 1, 2, 3]
    pp = generate_topology_from_subbasis(Y, particular_point_subbasis(Y, 0))
    assert not check_T3(Y, pp)[0]
    assert not check_T4(Y, pp)[0]


def test_t1_t2_t3_t4_and_discrete_all_coincide_on_finite_spaces():
    """
    Extends this project's central finding (finite T1 => discrete) to T3
    and T4: since Munkres's T3/T4 both require T1, and finite T1 already
    forces discreteness (hence trivially regular and normal), all five
    properties -- T1, T2, T3, T4, discrete -- coincide exactly on any
    finite topological space. Checked broadly, not just on hand-picked
    examples.
    """
    rng = random.Random(0)
    t1_count = 0
    for _ in range(500):
        n = rng.randint(1, 6)
        X = list(range(n))
        k = rng.randint(0, 5)
        subbasis = [frozenset(rng.sample(X, rng.randint(0, n))) for _ in range(k)]
        t = generate_topology_from_subbasis(X, subbasis)

        is_t1, _ = check_T1(X, t)
        is_t2, _ = check_T2(X, t)
        is_t3, _ = check_T3(X, t)
        is_t4, _ = check_T4(X, t)
        disc = is_discrete(X, t)

        if is_t1:
            t1_count += 1
        assert is_t1 == is_t2 == is_t3 == is_t4 == disc, f"mismatch for X={X}, subbasis={subbasis}"

    assert t1_count > 0  # sanity check the loop actually exercised T1 cases
