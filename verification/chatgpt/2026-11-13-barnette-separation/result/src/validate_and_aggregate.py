"""Verify complete part markers and associated planar-code files, collect results.
Outputs summary.csv, per_part.csv, and order-wise planar-code exception files.
Run after each batch. Requires no third-party packages.
"""
from pathlib import Path
from collections import defaultdict
import csv, re, sys
base=Path(__file__).resolve().parents[1]
expected={6:1,8:1,9:1,10:2,11:2,12:8,13:8,14:32,15:57,16:185,17:466,18:1543,19:4583,20:15374,21:50116,22:171168,23:582603,24:2024119,25:7057472,26:24873248,27:88111772,28:314301078}
mods={F:(1 if F<=22 else {23:4,24:4,25:8,26:32,27:128,28:512}[F]) for F in expected}
keyre=re.compile(r'^COMPLETE F=(\d+) n=(\d+) graphs=(\d+) noS2=(\d+) noS1=(\d+) attemptsS2=(\d+) attemptsS1=(\d+) seconds=([\d.]+)')
rows=[]
for F in expected:
  mod=mods[F]
  for j in range(mod):
    label=f'F{F}_{j}of{mod}'
    t=base/'parts'/f'{label}.txt'; p=base/'graphs'/f'{label}.pcode'
    if not (t.exists() and p.exists()):continue
    match=keyre.search(t.read_text().strip())
    assert match,(label,'bad completion marker')
    f,n,graphs,s2,s1,a2,a1,seconds=match.groups()
    f,n,graphs,s2,s1,a2,a1=map(int,(f,n,graphs,s2,s1,a2,a1))
    assert f==F and n==2*F-4
    assert 0<=s1<=s2<=graphs
    data=p.read_bytes()
    assert data.startswith(b'>>planar_code<<'),label
    assert len(data)==len(b'>>planar_code<<')+s2*(4*n+1),(label,'bad planar-code bytes')
    rows.append(dict(F=F,n=n,residue=j,modulus=mod,graphs=graphs,noS2=s2,noS1=s1,attemptsS2=a2,attemptsS1=a1,part_seconds=seconds))
with open(base/'per_part.csv','w',newline='') as w:
  out=csv.DictWriter(w,fieldnames=list(rows[0]));out.writeheader();out.writerows(rows)
summary=[]
for F in expected:
  rr=[r for r in rows if r['F']==F]
  n=2*F-4;tot=sum(r['graphs'] for r in rr);s2=sum(r['noS2'] for r in rr);s1=sum(r['noS1'] for r in rr)
  full=len(rr)==mods[F]
  if full:assert tot==expected[F],(n,tot,expected[F])
  assert tot<=expected[F],(n,tot,expected[F])
  summary.append(dict(n=n,F=F,complete_parts=len(rr),total_parts=mods[F],graphs=tot,expected_graphs=expected[F],without_S2=s2,without_S1=s1,complete=int(full),sum_part_wall_seconds=round(sum(float(r['part_seconds']) for r in rr),3),S2_attempts=sum(r['attemptsS2'] for r in rr),S1_attempts=sum(r['attemptsS1'] for r in rr)))
  if s2:
    name=f'nonS2_n{n}.pcode' if full else f'nonS2_n{n}_PARTIAL_0to{len(rr)-1}of{mods[F]}.pcode'
    assert full or [r['residue'] for r in rr]==list(range(len(rr))),(F,'nonconsecutive part range')
    path=base/'graphs'/name
    with open(path,'wb') as w:
      w.write(b'>>planar_code<<')
      for r in rr:
        data=(base/'graphs'/f"F{F}_{r['residue']}of{mods[F]}.pcode").read_bytes()
        w.write(data[len(b'>>planar_code<<'):])
    assert path.stat().st_size==len(b'>>planar_code<<')+s2*(4*n+1)
    assert path.stat().st_size<20_000_000,name
with open(base/'summary.csv','w',newline='') as w:
  out=csv.DictWriter(w,fieldnames=list(summary[0]));out.writeheader();out.writerows(summary)
for r in summary:print(f"n={r['n']} parts={r['complete_parts']}/{r['total_parts']} graphs={r['graphs']}/{r['expected_graphs']} noS2={r['without_S2']} noS1={r['without_S1']} partWallSum={r['sum_part_wall_seconds']}s")
