#!/usr/bin/env python3
"""Audit finished Barnette partitions, assemble counterexample streams, report, manifest, zip."""
import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict

ROOT=pathlib.Path(__file__).resolve().parents[1]
EXPECTED={6:1, 8:1, 9:1, 10:2, 11:2, 12:8, 13:8, 14:32, 15:57, 16:185, 17:466,18:1543, 19:4583, 20:15374, 21:50116, 22:171168,23:582603,24:2024119,25:7057472,26:24873248,27:88111772,28:314301078}
MOD={**{F:1 for F in range(6,23)},23:4,24:4,25:8,26:32,27:128,28:512}
RX=re.compile(r'^COMPLETE F=(\d+) n=(\d+) graphs=(\d+) noS2=(\d+) noS1=(\d+) attemptsS2=(\d+) attemptsS1=(\d+) seconds=([\d.]+)\s*$')
DATA={}
all_good=True
for F,expected in EXPECTED.items():
    entries=[]
    for res in range(MOD[F]):
        key=f'F{F}_{res}of{MOD[F]}'
        part=ROOT/'parts'/(key+'.txt')
        graph=ROOT/'graphs'/(key+'.pcode')
        log=ROOT/'logs'/(key+'.plantri.log')
        if not (part.is_file() and graph.is_file() and log.is_file()):continue
        match=RX.match(part.read_text())
        if not match:raise RuntimeError(f'Bad summary: {part}')
        cf,n,g,s2,s1,attempt2,attempt1,seconds=match.groups()
        cf,n,g,s2,s1,attempt2,attempt1=int(cf),int(n),int(g),int(s2),int(s1),int(attempt2),int(attempt1)
        seconds=float(seconds)
        if cf!=F or n!=2*F-4:raise RuntimeError(f'Bad F/n: {part}')
        # For cubic planar_code with n < 256: one n byte, three neighbours and 0 per vertex.
        content=graph.read_bytes()
        if not content.startswith(b'>>planar_code<<') or len(content)!=15+(4*n+1)*s2:raise RuntimeError(f'Bad pcode size: {graph}')
        log_data=log.read_text()
        m=re.search(r'\n(\d+) bipartite cubic graphs written to stdout; cpu=([\d.]+) sec',log_data)
        if not m or int(m[1])!=g:raise RuntimeError(f'Plantri discrepancy: {log}')
        entries.append(dict(res=res, graphs=g, noS2=s2, noS1=s1, tcheck=seconds, tgen=float(m[2]), pcode=graph))
    tot={k:sum(e[k] for e in entries) for k in ('graphs','noS2','noS1','tcheck','tgen')}
    complete=len(entries)==MOD[F]
    if complete and tot['graphs']!=expected:raise RuntimeError(f'Wrong OEIS count F={F}: {tot["graphs"]} != {expected}')
    DATA[F]=(entries,tot,complete)
    print(f'F={F:2} n={2*F-4:2} {len(entries):3}/{MOD[F]:3} graphs={tot["graphs"]:10} nonS2={tot["noS2"]:5} nonS1={tot["noS1"]:4} genCPU={tot["tgen"]:8.2f}s checkerSumElapsed={tot["tcheck"]:8.2f}s complete={complete}',flush=True)

if '--package' not in sys.argv:sys.exit(0)
# Only combine completely finished orders, ensure one header in concatenated stream.
combined=ROOT/'combined'
combined.mkdir(exist_ok=True)
for F,(entries,tot,complete) in DATA.items():
    if not complete or not tot['noS2']:continue
    out=combined/f'n{2*F-4}_without_S2.pcode'
    with open(out,'wb') as f:
        f.write(b'>>planar_code<<')
        for e in entries:
            f.write(e['pcode'].read_bytes()[15:])
    assert out.stat().st_size==15+(4*(2*F-4)+1)*tot['noS2']

import csv
with open(ROOT/'PARTS.csv','w',newline='') as csvout:
    writer=csv.writer(csvout)
    writer.writerow(('vertices','faces','part','modulus','graphs','without_S2','without_S1','checker_elapsed_s','plantri_cpu_s'))
    for f,(es,total,is_complete) in DATA.items():
        for e in es:
            writer.writerow((2*f-4,f,e['res'],MOD[f],e['graphs'],e['noS2'],e['noS1'],f"{e['tcheck']:.6f}",f"{e['tgen']:.2f}"))

parts=[]
for F,(entries,tot,complete) in DATA.items():
    n=2*F-4
    remaining=f'0/{MOD[F]}' if complete else f'{MOD[F]-len(entries)}/{MOD[F]}'
    status='complete' if complete else f'PARTIAL ({len(entries)}/{MOD[F]} parts)'
    parts.append(f'| {n} | {tot["graphs"]:,}' + ('' if complete else ' checked') + f' | {tot["noS2"]:,} | {tot["noS1"]:,} | {tot["tcheck"]:.2f} | {tot["tgen"]:.2f} | {status}; {remaining} remain |')
missing=[]
for F,(entries,tot,complete) in DATA.items():
    if not complete:
        done={e['res'] for e in entries}
        mm=MOD[F];remain=[i for i in range(mm) if i not in done]
        missing.append(f'- {2*F-4} vertices (F={F}): {len(remain)} of {mm} parts remain: ' + ', '.join(map(str,remain)))
report=f'''# Independent Barnette face-colour separation enumeration

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
'''+'\n'.join(parts)+'''

## Incomplete partitions

'''+ ('\n'.join(missing) if missing else 'None; all requested partitions are complete.')+'''

## Container

- Linux container with `nproc=5`, **4 effective CPU cores** (`/sys/fs/cgroup/cpu.max = 400000 100000`), **4 GiB cgroup memory limit** (`/sys/fs/cgroup/memory.max = 4294967296`), 5.8 GiB reported by `free -h`, GCC 14.2.0 and Clang 17.0.0 (compiler used: GCC).
- Complete results through F=27 (50 vertices) were recovered from previous saved parts. The F=28 (52-vertex) partitioned run was continued and its completed parts retained.
- "Without S1" counts refer to graphs lacking S1 among those without S2; every graph with S2 also has S1 by definition.
'''
(ROOT/'REPORT.md').write_text(report)

# Self-hashing manifest excluding itself. The zip lives outside the result tree.
manifest=ROOT/'MANIFEST.sha256'
with open(manifest,'w') as out:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p!=manifest and not p.name.endswith('.incomplete'):
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            out.write(f'{h}  {p.relative_to(ROOT)}\n')
print(f'Wrote REPORT.md and manifest ({len(manifest.read_text().splitlines())} files)')
if '--zip' in sys.argv:
    zpath=pathlib.Path('/mnt/data/barnette-separation-results.zip')
    with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and not p.name.endswith('.incomplete'):
                z.write(p,arcname='verification/chatgpt/2026-11-13-barnette-separation/result/'+p.relative_to(ROOT).as_posix())
    print(f'Wrote {zpath} ({zpath.stat().st_size} bytes)')
