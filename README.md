# Topology Generator from a Subbasis

Given a finite set $X$ and a subbasis $\mathcal{S}$ (any collection of subsets of $X$),
algorithmically generates the topology $\mathcal{S}$ induces — closure under finite
intersections (basis), then closure under arbitrary unions (topology) — validates the
topology axioms directly, and checks separation axioms ($T_0$ through $T_4$), continuity,
connectedness, and compactness, with concrete counterexamples wherever an axiom fails.

## Installation

```bash
cd topology-gen
pip install -e .
pytest tests/        # 32 tests, including two separate 500-trial randomized theorem checks
```

## Generating a topology

For a subbasis $\mathcal{S}$, the **basis** it generates is all finite intersections of
members of $\mathcal{S}$ (together with $X$, the empty intersection). The **topology** the
basis generates is all unions of subsets of the basis (together with $\emptyset$, the empty
union). Both steps are computed here by closing under pairwise intersection/union to a fixed
point — any finite intersection or union can be built one set at a time, so this reaches
every element of the basis/topology. Since $X$ is finite, "arbitrary" unions and "finite"
unions coincide, so this is an exact computation, not an approximation.

```python
from topology_gen import generate_topology_from_subbasis, discrete_subbasis

X = [0, 1, 2]
topology = generate_topology_from_subbasis(X, discrete_subbasis(X))
len(topology)   # 8 = 2^3, the full power set
```

## Validating a topology

```python
from topology_gen import is_topology

report = is_topology(X, topology)
print(report.summary())
```

`is_topology` checks $\emptyset, X \in \mathcal{T}$ and closure under pairwise
union/intersection of $\mathcal{T}$'s own members — which, since $X$ is finite, is exactly
equivalent to full closure under arbitrary unions and finite intersections. Every failed
check reports a concrete counterexample pair, not just `False`.

## Separation axioms: $T_0$ through $T_4$

```python
from topology_gen import check_T0, check_T1, check_T2, check_T3, check_T4

check_T0(X, topology)   # (bool, counterexample pair or None)
check_T1(X, topology)
check_T2(X, topology)
check_T3(X, topology)   # regular: T1, and points/closed sets separated by disjoint opens
check_T4(X, topology)   # normal: T1, and disjoint closed sets separated by disjoint opens
```

$T_1$ is cross-validated against its independent characterization ("every singleton is
closed") via `check_T1_via_closed_singletons`, so the classifier doesn't just trust one
formulation of the axiom.

$T_3$ and $T_4$ follow Munkres's convention: **regular** and **normal** are the separation
properties alone (available independently as `is_regular_space` / `is_normal_space`), and
$T_3 = \text{regular} + T_1$, $T_4 = \text{normal} + T_1$. Both fail immediately, with an
explicit `"T1 fails"` reason, whenever the underlying space isn't $T_1$ — see the extended
theorem below for why that turns out to be the *only* way they can fail on a finite space.


## Connectedness

```python
from topology_gen import is_connected, connected_components

is_connected(X, topology)          # bool
connected_components(X, topology)  # list of disjoint frozensets, partitioning X
```

A space is connected iff its only **clopen** (simultaneously open and closed) subsets are
$\emptyset$ and $X$. For a finite space, the clopen sets form a finite Boolean algebra under
intersection, and its atoms are exactly the connected components: `component(x)` is computed
here as the intersection of every clopen set containing $x$ — itself clopen (a finite
intersection of clopen sets), nonempty, and minimal by construction.

Checked against three cases with known answers: the **discrete** topology is totally
disconnected ($n$ singleton components), the **indiscrete** topology is connected (its only
clopen sets are $\emptyset, X$ trivially), and the **Sierpiński space** is connected despite
not being $T_1$ — $\{0\}$ is open but not closed (its complement $\{1\}$ isn't open), so it
isn't clopen, and no nontrivial clopen set exists at all.

## Compactness

```python
from topology_gen import is_compact

is_compact(X, topology)   # always True for a finite space
```

Every finite topological space is compact, automatically: the topology itself has at most
$2^{|X|}$ members, so any open cover — being a sub-collection of the topology — is already a
finite collection, and is trivially its own finite subcover. `is_compact` is implemented as a
genuine check via `has_finite_subcover` (which actually constructs a witnessing finite
subcover by greedy set cover) rather than a hardcoded `True`, so the "why" is demonstrable,
not just asserted.

## Continuity and homeomorphisms

```python
from topology_gen import is_continuous, is_homeomorphism

f = {0: 0, 1: 1, 2: 2}   # a dict mapping each element of X to its image in Y
is_continuous(X, topology_X, f, topology_Y)   # (bool, an open set of Y whose preimage isn't open, or None)
is_homeomorphism(X, topology_X, f, Y, topology_Y, f_inv)  # bijective + continuous both ways
```

$f: X \to Y$ is continuous iff the preimage of every open set of $Y$ is open in $X$. This
gives clean, checkable facts: the identity map is always continuous from a **finer** topology
to a **coarser** one on the same set (confirmed: discrete → indiscrete succeeds), but not the
reverse in general (confirmed: indiscrete → discrete fails, with the failing open set
returned as a witness); a **constant** map is continuous regardless of the domain topology
(the preimage of any open set is $\emptyset$ or $X$, both always open). `is_homeomorphism`
additionally checks that $f$ and its claimed inverse are genuinely mutually inverse
bijections before checking continuity both ways.

