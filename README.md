# OEIS candidate (no A-number yet): Barnette graphs with positive face-colour-separation defect

<!-- oeis-status:begin -->
**OEIS status: not submitted; no A-number yet** (lab registry, 13 Nov 2026).

- A______, Barnette graphs on 2n vertices with no Hamiltonian cycle separating two face colour classes: **candidate** (2026-11-13: reconsidered with Alex: the two failed criteria (few terms, uncertified 42..46) are fixable by computing; guide recount 8..46 agrees). Certificate: complete.

Rules and the full registry: [athanor-oeis](https://github.com/iwasborninbali/athanor-oeis/blob/main/REGISTRY.md).
<!-- oeis-status:end -->

## Definition

For k >= 4, a(k) counts isomorphism classes of simple 3-connected cubic bipartite planar graphs on 2k vertices whose face-colour-separation defect is positive. Offset 4. An empty class contributes 0, including k=5.

Embed each graph on the sphere and properly colour its faces with three colours; the colouring is unique up to permutation. For a Hamiltonian cycle C, its two sides partition the faces. Given distinct colours x,y and a designation of the sides as inside and outside, count the x-coloured faces outside plus the y-coloured faces inside. The defect is the minimum of this integer over all Hamiltonian cycles, all ordered distinct pairs x,y and both designations of sides. If there is no Hamiltonian cycle, define the minimum as +infinity, which is positive. This convention makes the sequence defined without assuming Barnette's conjecture. A defect of zero means that some Hamiltonian cycle separates two entire colour classes. The complementary third colour is unrestricted.

## Terms / result

| k | a(k) | k | a(k) |
|---:|---:|---:|---:|
| 4–19 | 0 | 20 | 2 |
| 21 | 0 | 22 | 8 |
| 23 | 88 | | |

Thus there are 16 consecutive zero terms through 38 vertices, followed by 2, 0, 8, 88 for 40, 42, 44, 46 vertices. These totals are source census reports; see the certificate for what was actually checked.

## How it was obtained

The producer enumerates the graph class with plantri 5.5, counts Hamiltonian cycles, traces faces from the rotation system and minimizes the side-colour mismatch. A count is taken over one generated representative per isomorphism class. Original graph lists, in plantri's Latin-1 adjacency format, are in `data/` (2, 8 and 88 graphs). The verification program independently enumerates cycles, colours faces and checks the defect. Its companion enumerates 3-edge cuts.

## Verification

The producer census was replayed through 40 vertices; the separate Python checker was replayed on the witnesses identified in [CERTIFICATE.md](CERTIFICATE.md). A separate checker validates graph-class membership from each supplied rotation system. These checks do not independently certify enumeration completeness or graph nonisomorphism. The full order-by-order table has not been independently established.

## Prior art and credit

Alt, Payne, Schmidt and Wood established the qualitative phenomenon before the lab work. The source census is credited to lab agent vtora; plantri is by Brinkmann and McKay. See [PRIOR-ART.md](PRIOR-ART.md) for details and OEIS search limitations.

## Reproduce

```sh
sh programs/fetch-plantri.sh
cc -O3 programs/hc2.c -o hc2
./plantri -adbc3 15 | ./hc2
python3 verification/verify_B.py data/n40_B_counterexamples.txt
python3 verification/cyc4.py data/n40_B_counterexamples.txt
python3 verification/fast_replay.py data/defect1_n44.txt
python3 verification/fast_replay.py data/defect1_n46.txt
python3 verification/cyc4.py data/defect1_n44.txt
python3 verification/cyc4.py data/defect1_n46.txt
python3 verification/class_check.py data/n40_B_counterexamples.txt data/defect1_n44.txt data/defect1_n46.txt
```

The producer command gives `graphs=57 ... def0=57 def1=0 ...` for 26 vertices. The first checker reports 260 and 280 cycles, proper colouring, no separating cycle and defect 1 for each 40-vertex graph; the second reports one cyclic 3-edge cut in each. Individual checks take up to minutes on the recorded machine. The accelerated checker asserts defect 1 on each of 8 and 88 witnesses; it reuses the original face and defect routines and caches a separately written pruned path enumeration. The cut checker prints 1 cyclically 4-edge-connected graph at n=44 and 3 at n=46. See the certificate and logs for actual replays. Fetching needs a network.

## Provenance

Source: `projects/science/barnette` at commit `3a25ee0144cfb45a380cc74ec0b6570bfbfa4256`, paths `data/hc2_n8-46.log`, `data/n40_B_counterexamples.txt`, `data/defect1_n44.txt`, `data/defect1_n46.txt`, `data/defect1_c4ec.md`, `code/hc2.c`, `code/checks.py`, `code/verify_B.py`, `code/cyc4.py`, `ledger.jsonl`, `research/answers/01-barnette.md`. The census logs 8–40 were replayed in the companion minima repository in this workspace. `data/source-census.csv` extracts selected numeric columns from the source log. The copied programs have been adapted to English: C comments were removed; Python output text was translated and the checker dependency was reduced to the three used routines without changing their algorithms. No source archive DOI was identified.

## Author, licence

Aleksei Kudriashov (ORCID 0009-0006-8885-5338), Athanor lab, with AI assistance (OpenAI Codex cores; Claude Code as the lab's guide). Code: MIT; data and text: CC BY 4.0 (see LICENSE.md).
