#!/usr/bin/env python3
"""Check simple cubic, bipartite, 3-connected, spherical rotation systems."""
import itertools, sys
from collections import deque
from pathlib import Path

def check(raw):
    order, body = raw.decode('latin-1').split(' ',1)
    n = int(order)
    adj = [[ord(c)-97 for c in row] for row in body.split(',')]
    assert len(adj) == n and all(len(row)==3 and len(set(row))==3 for row in adj)
    assert all(0<=v<n and v!=u and u in adj[v] for u,row in enumerate(adj) for v in row)
    def reachable(removed):
        root=next(v for v in range(n) if v not in removed)
        seen={root}; stack=[root]
        while stack:
            for v in adj[stack.pop()]:
                if v not in seen and v not in removed: seen.add(v); stack.append(v)
        return len(seen)==n-len(removed)
    assert reachable(set())
    assert all(reachable(set(v)) for k in (1,2) for v in itertools.combinations(range(n),k))
    colour={0:0}; q=deque([0])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in colour: colour[v]=1-colour[u]; q.append(v)
            else: assert colour[v] != colour[u]
    seen=set(); faces=0
    for u,row in enumerate(adj):
        for v in row:
            if (u,v) in seen: continue
            start=(u,v); a,b=start
            while (a,b) not in seen:
                seen.add((a,b)); a,b=b,adj[b][(adj[b].index(a)+1)%3]
            assert (a,b)==start
            faces += 1
    assert len(seen)==3*n and n-3*n//2+faces==2
    return n, faces

for filename in sys.argv[1:]:
    for i,line in enumerate(Path(filename).read_bytes().split(b'\n'),1):
        if not line: continue
        n,faces=check(line)
        print(f'{filename} graph={i} n={n} faces={faces} class=PASS',flush=True)
