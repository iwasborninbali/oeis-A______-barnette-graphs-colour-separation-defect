# Verification certificate

## Claim

- For k=4..23 the counts of graphs with positive defect are the values in `data/terms.txt`.
- Each supplied witness has defect 1; none of its Hamiltonian cycles separates two face colours.

## Evidence

| What | Program | Author / date | Coverage | Result |
|---|---|---|---|---|
| Producer | `programs/hc2.c` | lab agent vtora, 2026-08-31 per source ledger | source census even n=8..46 | reported defect histogram |
| Producer replay | `programs/hc2.c` and plantri | vtora; replay OpenAI Codex, 2026-11-13 | even n=8..40 | matches source histograms; recorded in companion repository and copied to logs here |
| Independent witness check | `verification/verify_B.py`, `verification/checks.py` | lab agent vtora, 2026-08-30/31 per source | n=40: 2 graphs; n=44: 8 graphs; n=46: first graph | all have proper colouring, no separating cycle and defect 1 |
| Accelerated witness check | `verification/fast_replay.py` with `verification/verify_B.py` | OpenAI Codex, 2026-11-13 for path enumeration; vtora for face and defect checks | all stored n=44 and 46 graphs | each passes defect-1 assertion; 44 counts agree with direct checker |
| Independent graph-class check | `verification/class_check.py` | OpenAI Codex, 2026-11-13 | all 98 supplied graphs | simple cubic, bipartite, 3-connected and spherical rotation systems |
| Cut check | `verification/cyc4.py` | lab agent vtora, 2026-08-30/31 per source | stored graphs, see logs | cyclic 3-edge-cut counts |

The source-derived Python checker shares neither C producer code nor its enumeration strategy, but shares the supplied embedding and the same mathematical definition. The accelerated replay uses the same `verify_B.py` face/defect functions as the direct checker, and a separately written degree-pruned path enumerator with caching; its necessary condition overlaps the producer's pruning principle, but it does not share code. The accelerated and direct checks are not two independent checks of the face calculations. The separate class checker verifies the supplied rotation systems are spherical by Euler characteristic, bipartiteness and connectivity after deletion of any one or two vertices. None independently generates the full graph class or checks the inputs for isomorphism.

## Replayed for this repository

2026-11-13, Darwin arm64, Python 3. Commands and complete output are in `verification/logs/`. The producer was replayed earlier in the companion minima repository at the same source commit, using plantri 5.5 and `cc -O3` for `hc2.c`; its 8–38 and 40 logs are copied here. The command there is `python3 programs/census.py N /tmp/barnette-c4/plantri /tmp/barnette-c4/hc2` for each even N from 8 through 40; the result at 40 is `graphs=171168 ... def0=171166 def1=2 ...`.

```sh
python3 verification/verify_B.py data/n40_B_counterexamples.txt
python3 verification/verify_B.py data/defect1_n44.txt
head -n 1 data/defect1_n46.txt > /tmp/barnette-c4/witness46.txt
python3 verification/verify_B.py /tmp/barnette-c4/witness46.txt
python3 verification/fast_replay.py data/defect1_n44.txt
python3 verification/compare.py
python3 verification/fast_replay.py data/defect1_n46.txt
python3 verification/cyc4.py data/n40_B_counterexamples.txt
python3 verification/cyc4.py data/defect1_n44.txt
python3 verification/cyc4.py data/defect1_n46.txt
python3 verification/class_check.py data/n40_B_counterexamples.txt data/defect1_n44.txt data/defect1_n46.txt
```

The source checker reports cycles 260 and 280 for the two n=40 witnesses, each with defect 1. The direct and accelerated cycle counts on the eight n=44 witnesses match: 392, 344, 344, 344, 324, 384, 384, 344. All 88 n=46 witnesses pass the accelerated check; the first also passes the direct checker with 480 cycles, agreeing with the accelerated count. Detailed outputs are in the logs; the checker output has been translated into English and its dependency reduced to the three used routines; their algorithms were not intentionally changed. The C source has its non-English comments removed.

## Not covered

Counts 0, 8 and 88 at n=42,44,46 and all source zeros before 40 are not independently certified as whole-class counts. The C census was replayed through 40, but relies on plantri for completeness and shares the producer's algorithm. Independent witness checks establish properties only of the supplied embeddings, not their pairwise nonisomorphism or the absence of further examples. Their graph-class membership was separately checked. The English-adapted source `verify_B.py` was run directly only on the first of the 88 n=46 graphs; its functions were run on them via the accelerated enumerator. The graph-class checker tests the supplied embeddings, not the completeness of the census. The extension to non-Hamiltonian graphs uses +infinity by convention and is not tested here. Existing literature and OEIS searches do not establish novelty or suitability for OEIS.

## Guide's independent check

13 November 2026. Two separately written programs, neither sharing code with the producer (`programs/hc2.c`, which
enumerates all Hamiltonian cycles) or with each other, both reading the graphs from plantri 5.5 (`plantri -dbc3 F`,
F = number of faces, split into parts with `res/mod` for 48-52 vertices):

1. The guide's `verification/guide/bsep.c`: a separating Hamiltonian cycle exists iff, for some colour z and some choice of
   sides for the z-faces, the resulting 2-factor (all {x,y}-edges plus one edge class of every z-face) is a single cycle
   (correctness argument in the file header). Logs: `verification/logs/guide-bsep-8-46.log` (Mac) and
   `verification/logs/guide-bsep-48-52-vm.log` (lab VM).
2. A ChatGPT agent's program written from the task's definitions only (task, conversation and results in
   `verification/chatgpt/2026-11-13-barnette-separation/`; per-part counts in `result/PARTS.csv`, manifest checked).

Both give 0 for 8..38 vertices and 2, 0, 8, 88, 75, 1032, 3817 for 40..52 vertices
(`verification/chatgpt/2026-11-13-barnette-separation/guide-comparison.log`); the graph counts equal A007083 at every
order. The completeness of plantri's generation is the standard assumption; A007083 is an independent published census
of the same class sizes.

## Verdict

complete — every term from 8 to 52 vertices is confirmed by two independent programs; the graph counts match A007083.
