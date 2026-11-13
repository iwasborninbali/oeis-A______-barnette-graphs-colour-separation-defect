# verify-barnette-separation — Continue computation report

## user · 2026-11-13T06:29:27
Please perform the task described in verification/chatgpt/2026-11-13-barnette-separation/TASK.md inside the attached archive (unpack it in your container; plantri55.tar.gz is in the archive root). Compute as much as fits in this reply and report what is done.
(files: barnette-separation-task.zip)

## assistant · 2026-11-13T06:53:53
Сначала распакую архив и прочитаю `TASK.md`, затем проверю доступные инструменты и выполню вычисления с воспроизводимыми результатами. В конце отмечу, что доказано или проверено, а что осталось открытым.

Analyzed face partitions and tested connectivity conditions

Implemented algorithm

Prepared implementation and finalized checker

## Barnette graph verification — interim results

The archive was unpacked successfully, and plantri 5.5 was compiled. I implemented an independent C checker for properties S2 and S1, using the supplied definitions.

**Complete enumeration through 38 vertices:** All 72,379 graphs examined have both S2 and S1. The generated graph counts match the supplied OEIS A007083 values at every order checked.

At 40 vertices, the complete enumeration of 171,168 graphs found **2 graphs without S2**, both of which satisfy S1. These are the first S2 failures found in the computation.

The checker preserves non-S2 graphs in planar-code format, and the work is being organized into resumable parts.

Checked orientation

Verified and optimized parallel Barnette graph separation enumeration

## user · 2026-11-13T06:54:09
Your last reply ended without a report. Please continue from your finished parts: compute as much as fits in this reply (42 vertices and beyond, both S2 and S1), and end the reply with a table of what is done: vertices, graphs, without S2, without S1, run time, and which parts remain. Answer in English.

## assistant · 2026-11-13T09:24:09
## Continued computation: 42–52 vertices

I recovered the saved checker, per-part results, logs, and counterexample files. The completed runs now establish the following additional counts beyond 40 vertices:

| Vertices | Graphs | Without S2 | Without S1 | Checker CPU time |
| --- | --- | --- | --- | --- |
| 42 | 582,603 | 0 | 0 | 5.09 s |
| 44 | 2,024,119 | 8 | 0 | 20.03 s |
| 46 | 7,057,472 | 88 | 0 | 83.17 s |
| 48 | 24,873,248 | 75 | 0 | 330.52 s |
| 50 | 88,111,772 | 1,032 | 0 | 1,323.15 s |

All five orders are completely enumerated. The graph totals match the expected counts in `TASK.md`. **None of the graphs without S2 at these orders fails S1.**

The 52-vertex run is already partitioned into 512 resumable parts. I am continuing that run rather than repeating finished computations.

## Final 52-vertex result

Complete enumeration — 512/512 partitions

## 314,301,078

Graphs checked

## 3,817

Without S2

## 0

Without S1

The graph total matches the expected value exactly. All 512 partitions finished successfully, and the primary audit confirms that their generator logs, checker counts, and saved counterexample-file sizes agree.

**The complete computational result through 52 vertices is that every enumerated Barnette graph satisfies S1**, although 3,817 of the 52-vertex graphs fail S2.

## Verification and deliverables

The independent Python checker has now verified **all 689 completed partitions from 40 through 52 vertices**, including every saved graph without S2. Its results agree with the C checker. All 140 additional S2-positive sample checks also passed.

The deliverables include the C source, Python verification scripts, per-part logs and counts, combined planar-code counterexample files, `REPORT.md`, `PARTS.csv`, and `MANIFEST.sha256`. Every manifest checksum passed, and ZIP integrity was confirmed.

**[Download complete results ZIP](#file-2)** (2.1 MB)

[Download REPORT.md](#file-3) · [Download PARTS.csv](#file-4)

The container had `nproc=5`, a four-core CPU quota, a 4 GiB memory limit, and GCC 14.2.0.

**Outstanding publication step:** The GitHub branch upload, read-back hash verification, and draft pull request have not been performed. The local computation and its integrity checks are complete.

## Final computation table

Run time below is the sum of per-part checker elapsed times, not the overall parallel wall time. Generator CPU times are recorded separately in the report. The 10-vertex order is omitted because no Barnette graphs exist at that order.

| Vertices | Graphs | Without S2 | Without S1 | Checker time | Parts remaining |
| --- | --- | --- | --- | --- | --- |
| 8 | 1 | 0 | 0 | 0.00 s | 0/1 |
| 12 | 1 | 0 | 0 | 0.00 s | 0/1 |
| 14 | 1 | 0 | 0 | 0.01 s | 0/1 |
| 16 | 2 | 0 | 0 | 0.00 s | 0/1 |
| 18 | 2 | 0 | 0 | 0.00 s | 0/1 |
| 20 | 8 | 0 | 0 | 0.00 s | 0/1 |
| 22 | 8 | 0 | 0 | 0.00 s | 0/1 |
| 24 | 32 | 0 | 0 | 0.00 s | 0/1 |
| 26 | 57 | 0 | 0 | 0.00 s | 0/1 |
| 28 | 185 | 0 | 0 | 0.00 s | 0/1 |
| 30 | 466 | 0 | 0 | 0.00 s | 0/1 |
| 32 | 1,543 | 0 | 0 | 0.00 s | 0/1 |
| 34 | 4,583 | 0 | 0 | 0.02 s | 0/1 |
| 36 | 15,374 | 0 | 0 | 0.07 s | 0/1 |
| 38 | 50,116 | 0 | 0 | 0.25 s | 0/1 |
| 40 | 171,168 | 2 | 0 | 0.92 s | 0/1 |
| 42 | 582,603 | 0 | 0 | 5.09 s | 0/4 |
| 44 | 2,024,119 | 8 | 0 | 20.03 s | 0/4 |
| 46 | 7,057,472 | 88 | 0 | 83.17 s | 0/8 |
| 48 | 24,873,248 | 75 | 0 | 330.52 s | 0/32 |
| 50 | 88,111,772 | 1,032 | 0 | 1,323.15 s | 0/128 |
| **52** | **314,301,078** | **3,817** | **0** | **6,882.58 s** | **0/512** |

**All requested vertex orders and computational partitions are complete.**
(files: barnette-separation-REPORT.md, barnette-separation-PARTS.csv, Download complete results ZIP, REPORT.md, PARTS.csv)

## user · 2026-11-13T09:25:42
Thank you, that is complete and agrees with my own separate count at every order, including 3817 at 52 vertices. Please now do the GitHub delivery from TASK.md step 3: push the unpacked result files (sources, REPORT.md, PARTS.csv, per-part logs and counts, the counterexample files if under 20 MB in total, MANIFEST.sha256) to a new branch chatgpt/2026-11-13-barnette-separation of iwasborninbali/oeis-A______-barnette-graphs-colour-separation-defect under verification/chatgpt/2026-11-13-barnette-separation/result/, read every pushed file back and compare hashes, and open a draft pull request into main. Answer in English with the branch, PR URL and the read-back result.
