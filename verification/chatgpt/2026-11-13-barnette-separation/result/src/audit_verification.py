#!/usr/bin/env python3
"""Audit independent face-dual verifier logs against all completed source parts."""
import pathlib,re,collections,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
line_re=re.compile(r'(?:graphs/)?(F\d+_\d+of\d+)\.pcode total_noS2 (\d+) total_noS1 (\d+) seconds ([\d.]+)')
summary_re=re.compile(r'graphs=(\d+) noS2=(\d+) noS1=(\d+)')
verified={};errors=[]
for log in sorted((ROOT/'logs').glob('*verify_independent*.log')):
    for line in log.read_text().splitlines():
        match=line_re.search(line)
        if not match:continue
        part,s2,s1,_=match.groups()
        s2,s1=int(s2),int(s1)
        prev=verified.get(part)
        if prev and prev!=(s2,s1):errors.append(f'conflicting verification for {part}: {prev} vs {(s2,s1)}')
        verified[part]=(s2,s1)
missing=[];present=collections.Counter()
for part in sorted((ROOT/'parts').glob('F*_*of*.txt')):
    # Source parts F>=22 have some nonS2; S2-positive orders need no secondary checking.
    m=summary_re.search(part.read_text())
    if not m:errors.append(f'malformed primary summary {part}');continue
    n,s2,s1=map(int,m.groups())
    F=int(re.search(r'^F(\d+)_',part.name)[1])
    if F<22:continue
    got=verified.get(part.stem)
    if got is None:missing.append(part.stem)
    elif got!=(s2,s1):errors.append(f'{part.stem}: independent {got} differs from primary {(s2,s1)}')
    else:present[F]+=1
print('Verified independent partitions by number of faces:',dict(sorted(present.items())))
print('Missing',len(missing),'out of',sum(1 for _ in (ROOT/'parts').glob('F*_*of*.txt')),'total saved parts')
if missing:print('Missing partitions:', ', '.join(missing[:35]))
for e in errors:print('ERROR:',e)
sys.exit(2 if errors else 0)
