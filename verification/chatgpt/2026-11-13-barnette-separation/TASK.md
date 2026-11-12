# Independent count: Barnette graphs without a Hamiltonian cycle that separates two face colour classes (up to 52 vertices)

Write your own programs from the definitions below, run them in your container, and report. This archive contains only
this brief and the source of plantri 5.5 (Brinkmann and McKay; `plantri55.tar.gz`, SHA-256
911cdf5bcca7294eb80f8f79fefc148183f7ba81da15b3aa4d6d2401a3bc7ded), the standard generator for these graphs.

## Definitions
- A Barnette graph is a 3-connected cubic bipartite planar graph. `plantri -dbc3 F` writes all of them with F faces
  (2F - 4 vertices), one per isomorphism class, with their (unique up to reflection) plane embedding, in planar code.
  Use `plantri -dbc3 F res/mod` to split a run into `mod` disjoint parts.
- The faces of a Barnette graph can be properly coloured with 3 colours (adjacent faces differ); the colouring is unique up
  to permuting the colours. At every vertex the three faces have three different colours.
- Property S2: there is a Hamiltonian cycle C and two different colours x, y such that every face of colour x lies inside C
  and every face of colour y lies outside C (the third colour is unrestricted).
- Property S1 (weaker): there is a Hamiltonian cycle C and a colour x such that every face of colour x lies on the same side of C.
- A graph with no Hamiltonian cycle has neither property.

## What to compute
For every vertex count 2k = 8, 12, 14, ..., 52 (F = k + 2 faces; there are no Barnette graphs with 10 vertices):
the number of Barnette graphs, the number WITHOUT property S2, and the number WITHOUT property S1.
Expected graph counts (OEIS A007083): 1, 1, 1, 2, 2, 8, 8, 32, 57, 185, 466, 1543, 4583, 15374, 50116, 171168, 582603,
2024119, 7057472, 24873248, 88111772, 314301078 for 8, 12, 14, ..., 52 vertices.
Any correct exact method is fine; explain it and why it is exact. For each order with a nonzero count, also write the graphs
without S2 to a file (planar code or plantri ascii, `plantri -a` style), if the total is under 20 MB.

## How to run and report
1. Report `nproc`, memory, compiler versions.
2. Long runs: split with res/mod, use all cores, write progress and results per part to files so a run can resume from
   finished parts. Processes do not survive the end of your reply, so in each reply compute as much as fits, then report
   which parts are done; I will ask you to continue.
3. When everything is done (or when I ask), push through your GitHub connector to a new branch
   `chatgpt/2026-11-13-barnette-separation` of the repository `iwasborninbali/oeis-A______-barnette-graphs-colour-separation-defect`
   (never to main), into `verification/chatgpt/2026-11-13-barnette-separation/result/`: your sources, a REPORT.md (method,
   exact commands, results table, run times, container resources), all logs and per-part result files, the files of graphs
   without S2, and MANIFEST.sha256 for every file. Read every pushed file back and compare hashes (we have seen '?' turn into
   NUL bytes in transit). Then open a draft pull request into main.

Answer in English. Be exact; say plainly what is not finished or not checked.
