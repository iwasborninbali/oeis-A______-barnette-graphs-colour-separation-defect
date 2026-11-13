# Independent Barnette face-colour separation enumeration

## Method and exactness

- Generator: plantri 5.5, archive `plantri55.tar.gz` SHA-256 `911cdf5bcca7294eb80f8f79fefc148183f7ba81da15b3aa4d6d2401a3bc7ded`, invoked `plantri -dbc3 F res/mod`. This enumerates each 3-connected cubic bipartite plane graph once up to isomorphism/reflection.
- C program `src/check_barnette.c` reads the binary planar_code stream, traverses the directed darts to obtain face boundaries, and propagates the unique 3-face-colouring from the incident faces of vertex 0.
- Every Hamiltonian cycle is the boundary between two face regions. At any cubic vertex exactly one of its three incident faces lies on one side and two on the other, because a Hamiltonian cycle passes through the vertex using two of its three edges.
- **S2:** choose ordered colour classes x inside and y outside, with third colour z. Assign each z-face to inside or outside, exploring all `2^(number of z-faces)` assignments. As x and y differ at every vertex, the boundary is a spanning 2-regular subgraph. Follow its cycle from vertex 0; it is Hamiltonian iff it visits all vertices. Repeat for the three possible unordered choices of x,y. Exhaustive and exact.
- **S1:** choose x inside, and assign the other two face colours freely. At every vertex at least one of the non-x faces must be outside; equivalently the set of non-x faces assigned inside is an *independent set in the dual graph induced by those two face colours*. Enumerate all such independent sets with depth-first search and pruning, derive the boundary, and test whether it is one Hamiltonian cycle. Repeat for each x. Test S1 only on graphs failing S2, since S2 implies S1. Exhaustive and exact.
- Independent secondary verification: Python `src/verify_independent.py` checks planar-code outputs by building the dual graph and testing connectivity of **both** face regions for each allowed assignment rather than walking a primal cycle. Verification logs include `logs/F22to26_verify_independent.log`, `logs/F27_verify_independent.log` and the various `logs/F28_verify_independent_*.log` files. Run `python src/audit_verification.py` to confirm per-part verification coverage and agreement. (A verification log applies only to its recorded inputs.)
- Additional positive cross-check: `src/verify_positive_samples.py` independently checks 20 fresh generator graphs at each order from 40 through 52 vertices, all S2-positive; see `logs/S2_positive_samples.log`.
- A part is committed atomically only when generator and checker both exit successfully. Every complete per-part summary is audited against its generator-reported graph count, and the number of saved counterexamples against its planar-code file size. The expected total graph counts are checked for each complete order.

## Reproduction

```sh
tar -xzf plantri55.tar.gz
cd plantri55 && make plantri && cd ..
gcc -O3 -std=c11 -o result/src/check_barnette result/src/check_barnette.c
# Example 50 vertices = 27 faces; split into 128 independent parts:
cd result
python src/run_parts.py 27 128 0 128 5
python src/audit_and_package.py --package
```

`run_parts.py` skips parts with a complete marker and a saved code file; it writes one file per `F_resOfMod` partition under `parts/`, a generator log and checker log under `logs/`, and a planar-code stream of graphs without S2 under `graphs/`. Combined streams are under `combined/`. All times are seconds. `Checker` is the **sum of per-part monotonic elapsed times**, so concurrent parts overlap in actual elapsed wall-clock time. `Generator` is the sum of CPU times printed by plantri and is additional to checker time; these are not a single wall time.

## Results

| Vertices | Graphs enumerated | Without S2 | Without S1 | Checker sum (s) | Generator CPU (s) | Status; parts remaining |
|---:|---:|---:|---:|---:|---:|---|
| 8 | 1 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 12 | 1 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 14 | 1 | 0 | 0 | 0.01 | 0.00 | complete; 0/1 remain |
| 16 | 2 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 18 | 2 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 20 | 8 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 22 | 8 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 24 | 32 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 26 | 57 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 28 | 185 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 30 | 466 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 32 | 1,543 | 0 | 0 | 0.00 | 0.00 | complete; 0/1 remain |
| 34 | 4,583 | 0 | 0 | 0.02 | 0.01 | complete; 0/1 remain |
| 36 | 15,374 | 0 | 0 | 0.07 | 0.02 | complete; 0/1 remain |
| 38 | 50,116 | 0 | 0 | 0.25 | 0.09 | complete; 0/1 remain |
| 40 | 171,168 | 2 | 0 | 0.92 | 0.26 | complete; 0/1 remain |
| 42 | 582,603 | 0 | 0 | 5.09 | 1.42 | complete; 0/4 remain |
| 44 | 2,024,119 | 8 | 0 | 20.03 | 4.86 | complete; 0/4 remain |
| 46 | 7,057,472 | 88 | 0 | 83.17 | 22.68 | complete; 0/8 remain |
| 48 | 24,873,248 | 75 | 0 | 330.52 | 91.78 | complete; 0/32 remain |
| 50 | 88,111,772 | 1,032 | 0 | 1323.15 | 346.00 | complete; 0/128 remain |
| 52 | 314,301,078 | 3,817 | 0 | 6882.58 | 1289.44 | complete; 0/512 remain |

## Incomplete partitions

None; all requested partitions are complete.

## Container

- Linux container with `nproc=5`, **4 effective CPU cores** (`/sys/fs/cgroup/cpu.max = 400000 100000`), **4 GiB cgroup memory limit** (`/sys/fs/cgroup/memory.max = 4294967296`), 5.8 GiB reported by `free -h`, GCC 14.2.0 and Clang 17.0.0 (compiler used: GCC).
- Complete results through F=27 (50 vertices) were recovered from previous saved parts. The F=28 (52-vertex) partitioned run was continued and its completed parts retained.
- "Without S1" counts refer to graphs lacking S1 among those without S2; every graph with S2 also has S1 by definition.
