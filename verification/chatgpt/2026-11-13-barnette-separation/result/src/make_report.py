"""Generate REPORT.md and MANIFEST.sha256 after validate_and_aggregate.py."""
from pathlib import Path
import csv, datetime, hashlib, subprocess
base=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader(open(base/'summary.csv')))
assert rows
header='''# Independent enumeration of Barnette graphs with S2/S1 defects

**Status:** {status}. **Report generated:** {generated} UTC.
The count for 10 vertices is zero (there is no Barnette graph of that order).

## Method and exactness

The input generator is **plantri 5.5**, using exactly `-dbc3 F`, where `F = (n+4)/2` is the face count. Plantri's output is binary `planar_code`, with one plane 3-connected cubic bipartite graph per isomorphism class. The original `plantri55.tar.gz` has SHA-256 `911cdf5bcca7294eb80f8f79fefc148183f7ba81da15b3aa4d6d2401a3bc7ded`, and its copy is in `third_party/`.

`src/check_barnette.c` reads planar-code records, reconstructs the embedding's facial walks from the cyclic neighbor lists, and three-colours faces by triangle propagation from the first vertex. For each edge, it records the two incident face colours, and for each primal vertex it records the three incident faces (of three distinct colours). It checks cubic adjacency, Euler's formula, face colouring, and the expected face count.

* **S2**: Choose the free colour `z` in each of 3 ways, and let the other colours be `x` and `y`. Put all `x` faces on side 1 and all `y` faces on side 0, then exhaust **every** binary side assignment to the `z` faces. At each primal vertex there is exactly one face of each colour, so the edges separating sides form a spanning 2-regular subgraph. The `x-y` edge is obligatory at each vertex; the other chosen edge is determined solely by the bit of the adjacent `z` face. Follow the resulting 2-factor's alternating mandatory/nonmandatory edges from vertex zero. It is Hamiltonian if and only if the first return occurs after exactly `n/2` mandatory-edge steps. Side labels can be complemented without changing the boundary, so one fixed orientation per unordered colour pair is enough.
* **S1**: This search is necessary only for graphs rejected by S2 (because S2 implies S1). Fix one of three colours `x` to side 1. Enumerate side assignments to **all** other faces by an exhaustive depth-first search. The sole local admissibility restriction is that the two non-`x` faces incident at a vertex cannot both be side 1; otherwise the boundary would omit this vertex. Such prohibited simultaneous choices form an independent-set constraint in a dual bipartite graph, used only to prune impossible assignments. Every valid assignment gives a spanning 2-factor. Trace the boundary by excluding the unique same-side edge at each vertex; accept precisely when it is one cycle of length `n`. Complementing the side labels makes it sufficient to fix `x` to side 1.

These tests are exact because each Hamiltonian cycle induces one of the enumerated face-side assignments, and every accepted assignment produces a simple spanning cycle. They do not use random sampling or heuristic early rejection. Mask order is a *search order* optimization; all masks remain covered on failure. The earliest runs used the same logic in `src/check_barnette_v1.c`, with masks enumerated numerically; the current code tries balanced free-colour assignments first. Recomputing partition `F26 0/32` with both versions gave identical output byte hashes `41aceaee2dc95492e1bb705c715496c8a5073a3d5d0a7f48c57df752b8402ee0`.

`src/verify_independent.py` is a second, structurally different implementation: it enumerates the same face-side possibilities but decides whether they yield a Hamiltonian cycle by checking *connectivity of both induced face regions in the dual*. It has been run for every stored non-S2 graph up to the verification-log cutoff, checking both absence of S2 and presence or absence of S1. `src/crosscheck_small.py` additionally tests every graph through 28 vertices with this independent implementation. Verification logs are in `logs/`. For remaining graphs, the exact C algorithm is the primary check.

## Results

The counts labelled *partial* are **not** counts for the full order. All completed-order graph totals were checked against the values in the task brief (OEIS A007083).

| Vertices | Graphs processed | Without S2 | Without S1 | Parts done | Status |
|---:|---:|---:|---:|---:|:---|
{table}

A summary in machine-readable form is `summary.csv`, with one record per order; `per_part.csv` has counts and checker timings for every completed partition. Every exception graph is preserved in per-part `graphs/F{{F}}_{{res}}of{{mod}}.pcode`; combined planar-code outputs are `graphs/nonS2_n{{n}}.pcode` for finished orders and `graphs/nonS2_n52_PARTIAL_...pcode` when 52 is incomplete. All combined outputs are under 20 MB.

## Reproduction and continuation

Resources: `nproc` = **5**; CPU quota in `/sys/fs/cgroup/cpu.max` = **400000 / 100000**, i.e. **4 effective cores**; cgroup memory limit `/sys/fs/cgroup/memory.max` = **4294967296 bytes (4 GiB)**. The `free -h` snapshot reported **5.8 GiB** total addressable memory, but the 4 GiB cgroup limit controls the container. `gcc` = **14.2.0** (Debian 14.2.0-19); `clang` = **17.0.0**; architecture `{arch}`. Four worker processes were used for the main split batches; a later background batch used five processes under the same four-core quota.

Build:

```bash
cd verification/chatgpt/2026-11-13-barnette-separation/result
bash src/build.sh
```

For a partition (`F=28`, residue 64 of 512 as an example), the exact generator command is:

```bash
./third_party/plantri55/plantri -dbc3 28 64/512 | ./src/check_barnette 28 graphs/F28_64of512.pcode
```

Prefer the resumable launcher, which captures generator/checker logs and installs atomic completion markers only if both processes exit successfully:

```bash
python3 src/run_parts.py 28 512 64 72 4
python3 src/validate_and_aggregate.py
python3 src/make_report.py
```

Change `64 72` to the next range of unfinished residues. The launcher skips a residue only if the completion marker and its planar-code output both exist, so an interrupted run is resumable. For `n=50`, the full order was split as `F=27`, `mod=128`; for `n=48`, `F=26`, `mod=32`; for `n=46`, `F=25`, `mod=8`; for `n=44,42`, `F=24,23`, `mod=4`. Small orders `F=6,8,...,22` were run unsplit. The `plantri` stderr log gives its generator count for each part.

**Timing interpretation:** the following seconds are sums of the per-part wall-clock durations measured by the checker, **not** a single elapsed wall time: parts ran concurrently. As a rough upper bound on CPU work these numbers are useful, but they should not be presented as the elapsed duration of a four-worker campaign.

| Vertices | Sum of per-part elapsed seconds | S2 candidate checks | S1 candidate checks |
|---:|---:|---:|---:|
{timings}

## Data integrity, limitations and GitHub

The provided plantri archive checksum was verified. All committed part markers and planar-code output lengths are rechecked by `src/validate_and_aggregate.py`. `MANIFEST.sha256` lists SHA-256 hashes of every file under `result/` except the manifest itself, which cannot include its own stable hash. Combined exception outputs do **not** include isomorphism-repeated graphs from different parts, because plantri's `res/mod` decomposition partitions the isomorphism classes disjointly. The logs include independent verification output.

{limitations}
'''
finished=all(int(r['complete']) for r in rows)
status='Complete through 52 vertices' if finished else f"Complete through 50 vertices; 52 vertices partial ({rows[-1]['complete_parts']}/{rows[-1]['total_parts']} partitions)"
table='\n'.join(f"| {r['n']} | {int(r['graphs']):,} | {int(r['without_S2']):,} | {int(r['without_S1']):,} | {r['complete_parts']}/{r['total_parts']} | {'complete' if int(r['complete']) else 'partial'} |" for r in rows)
timings='\n'.join(f"| {r['n']} | {float(r['sum_part_wall_seconds']):,.3f} | {int(r['S2_attempts']):,} | {int(r['S1_attempts']):,} |" for r in rows)
limitations=('Every required order has been enumerated and checked.' if finished else 'The 52-vertex order is incomplete: the remaining partitions have not yet been counted. Its S2/S1 defect counts are lower bounds only. No GitHub branch or pull request has been created, because the brief requests GitHub submission when the full computation is complete or explicitly requested.')
arch=subprocess.check_output(['uname','-m'],text=True).strip()
text=header.format(status=status,generated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),table=table,timings=timings,limitations=limitations,arch=arch)
(base/'REPORT.md').write_text(text)
print('Wrote REPORT.md',len(text),'bytes. Status:',status)
# Rebuild manifest; ignore manifest itself, and any unfinished temporary outputs.
files=sorted(p for p in base.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256' and not p.name.endswith('.incomplete') and '__pycache__' not in p.parts)
with open(base/'MANIFEST.sha256','w') as f:
 for p in files:f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(base))+'\n')
print('Manifest entries:',len(files))
