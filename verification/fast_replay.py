#!/usr/bin/env python3
"""Replay verify_B with a separately written, cached path enumerator.

The necessary degree test removes only paths for which an unused vertex
has fewer than two possible cycle neighbours remaining. Face processing and
both defect checks are the unmodified verify_B routines.
"""
import functools, sys
from pathlib import Path
import verify_B

@functools.lru_cache(maxsize=2)
def paths(g):
    n = len(g)
    allbits = (1 << n) - 1
    masks = [sum(1 << v for v in row) for row in g]
    path = [0]
    cycles = set()
    def visit(u, visited):
        if visited == allbits:
            if masks[u] & 1 and path[1] < u:
                cycles.add(frozenset(frozenset((path[i], path[(i+1)%n])) for i in range(n)))
            return
        choices = masks[u] & ~visited
        while choices:
            bit = choices & -choices; choices -= bit
            v = bit.bit_length()-1
            rem = allbits ^ (visited | bit)
            permitted = rem | bit | 1
            r = rem
            while r:
                b = r & -r; r -= b
                if (masks[b.bit_length()-1] & permitted).bit_count() < 2:
                    break
            else:
                path.append(v); visit(v, visited | bit); path.pop()
    visit(0, 1)
    return cycles

def fast(g):
    return paths(tuple(tuple(row) for row in g))
verify_B.ham_cycles = fast
for filename in sys.argv[1:]:
    lines = [x for x in Path(filename).read_bytes().split(b'\n') if x]
    for i, raw in enumerate(lines, 1):
        line = raw.decode('latin-1')
        n, nf, profile, h, proper, sep = verify_B.separating(line)
        h2, defect, forced, maxface = verify_B.defect_and_forced(line)
        assert h == h2 and proper and not sep and defect == 1
        print(f'{filename} graph={i} n={n} faces={nf} cycles={h} proper={proper} separating={len(sep)} defect={defect} forced={forced}', flush=True)
