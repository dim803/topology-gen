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

## A real theorem, checked computationally

**Every finite $T_1$ space is discrete** (and consequently $T_1 \iff T_2$ for finite spaces,
even though $T_1$ does not imply $T_2$ in general topology — the standard counterexample, the
cofinite topology, requires an infinite set). This isn't assumed; it's checked directly:

```
$ python examples/finite_t1_implies_discrete_demo.py
Generated 2000 random finite topologies.
  399 of them were T1.
  Of those, 399 were discrete (ALL of them).
  Of those, 399 were also T2 (ALL of them).
```

`tests/test_topology_gen.py` asserts this as an explicit property across 500 randomly
generated subbases on sets of size 1–6, not just a couple of hand-picked examples — the same
"generate broadly, check a real theorem" approach used for Wedderburn's theorem in the
`ring-field-checker` project and the exhaustive cross-validation in `polyring-fp`.

### Extended: $T_1 \iff T_2 \iff T_3 \iff T_4 \iff$ discrete

Since Munkres bakes $T_1$ into the definitions of $T_3$ and $T_4$, and finite $T_1$ spaces
are already discrete (hence trivially regular and normal), **all five properties coincide
exactly** on any finite topological space:

```
checked 500 random topologies, 92 were T1, 0 mismatches
```

`tests/test_extensions.py::test_t1_t2_t3_t4_and_discrete_all_coincide_on_finite_spaces`
checks this directly — for every one of 500 random subbases, `is_T1 == is_T2 == is_T3 ==
is_T4 == is_discrete`, always.

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

## An interesting finite-space curiosity

Two classic constructions from point-set topology — the **order topology** and the
**lower-limit topology** (finite analogue of the Sorgenfrey line) — both collapse to the
**discrete topology** on any finite linearly ordered set:

```python
from topology_gen import generate_topology_from_subbasis, order_topology_subbasis, is_discrete

X = [0, 1, 2, 3]
t = generate_topology_from_subbasis(X, order_topology_subbasis(X))
is_discrete(X, t)   # True
```

This makes sense once seen: in a finite linear order, any interior point $x$ can be isolated
as $\{x\} = \{y : y < x+1\} \cap \{y : y > x-1\}$ (an intersection of two subbasis rays), and
the endpoints are isolated by a single ray each. This is a genuine difference from the
infinite/continuum case, where neither topology is discrete and the lower-limit topology is
strictly finer than the order topology. `initial_segment_basis` deliberately reproduces what's
lost by omitting the unbounded-above ray from the lower-limit construction: the result is a
valid but non-$T_1$ topology, since the maximum element can then only be reached by $X$ itself.

## Other constructions

- **`sierpinski_topology()`** — the two-point space $\{0,1\}$ with $\mathcal{T} =
  \{\emptyset, \{0\}, \{0,1\}\}$: the smallest possible $T_0$-not-$T_1$ example.
- **`particular_point_subbasis(X, p)`** / **`excluded_point_subbasis(X, p)`** — generate the
  particular-point and excluded-point topologies (open sets are, respectively, everything
  containing $p$, or everything not containing $p$) — both classic $T_0$-not-$T_1$ families.

## `compare_topologies`

```python
from topology_gen import compare_topologies

compare_topologies(t1, t2)   # "finer" | "coarser" | "equal" | "incomparable"
```

The discrete topology is finer than every topology on the same set; the indiscrete topology
is coarser than every topology.

## Project layout

```
topology-gen/
├── pyproject.toml
├── conftest.py
├── src/topology_gen/
│   ├── __init__.py
│   ├── generator.py        (subbasis -> basis -> topology, via fixed-point closure)
│   ├── validate.py         (is_topology, with counterexamples)
│   ├── separation.py       (T0-T4, regular/normal, closed_sets, compare_topologies)
│   ├── connectedness.py    (connected_components, is_connected, clopen_sets)
│   ├── compactness.py      (is_compact, has_finite_subcover)
│   ├── continuity.py       (is_continuous, is_homeomorphism)
│   └── constructions.py    (discrete, order, lower-limit, Sierpinski, particular/excluded point)
├── examples/
│   ├── generate_and_classify_demo.py
│   ├── finite_t1_implies_discrete_demo.py
│   └── extensions_demo.py
└── tests/
```

## Known limitations

- Both the basis and topology generation steps are, in the worst case, exponential in the
  size of the subbasis/basis (the discrete topology on $n$ points genuinely has $2^n$ open
  sets — there's no way around that, it's the correct answer, not an inefficiency). Fine for
  the small $|X|$ this project targets; would need a smarter representation (e.g. minimal
  basis tracking, or working with a fixed basis rather than materializing the full topology)
  for much larger finite spaces.
- Everything here is about *finite* topological spaces. The interesting distinction between
  the order topology and the lower-limit topology only shows up on infinite sets (e.g. the
  real line); this project can illustrate what's lost in the finite case, but can't
  reconstruct the genuinely infinite phenomenon. Compactness is a good example of this
  limitation in action: it's automatic and not very illuminating here precisely *because*
  every finite space is compact — the interesting compactness questions (e.g. is $[0,1]$
  compact under the standard topology) require infinite sets this project doesn't model.
- `compare_topologies` only handles two topologies on the *same* underlying set $X$.
- `is_continuous` and `is_homeomorphism` take $f$ as an explicit dict (a fully specified
  function on a finite set), not a symbolic/parametric map — fine for finite $X, Y$, but
  there's no way to express "check continuity of $f(x)=x^2$" symbolically the way one would
  for a map between infinite spaces.
- $T_3$ and $T_4$ follow Munkres's convention (which bakes $T_1$ into both definitions); a
  different textbook's convention (regular/normal without $T_1$) would need
  `is_regular_space`/`is_normal_space` directly rather than `check_T3`/`check_T4`.

## Possible extensions

- Vector space / module axiom checking, given a ring and an abelian group with a scalar
  action (unrelated to topology, but a natural next step in the same spirit as
  `ring-field-checker`)
- Quotient topologies: given an equivalence relation on $X$, generate the quotient space and
  its topology
- Product topologies for two finite spaces, and a check of whether compactness/connectedness
  is preserved under products (trivially yes here, but worth stating why explicitly)
