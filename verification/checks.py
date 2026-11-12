"""Face tracing and unpruned Hamiltonian enumeration, adapted from the lab source."""
from collections import Counter

def faces(g):
    seen, fs = (set(), [])
    for u in range(len(g)):
        for v in g[u]:
            if (u, v) in seen:
                continue
            f, a, b = ([], u, v)
            while (a, b) not in seen:
                seen.add((a, b))
                f.append((a, b))
                nxt = g[b][(g[b].index(a) + 1) % 3]
                a, b = (b, nxt)
            fs.append(f)
    return fs

def ham_cycles(g):
    n = len(g)
    cyc = set()
    path = [0]
    seen = {0}

    def go(u):
        if len(path) == n:
            if 0 in g[u]:
                cyc.add(frozenset((frozenset((path[i], path[i + 1])) for i in range(n - 1))) | {frozenset((u, 0))})
            return
        for w in g[u]:
            if w not in seen:
                seen.add(w)
                path.append(w)
                go(w)
                path.pop()
                seen.discard(w)
    go(0)
    return cyc

def inside_faces(cycle, fs, g, edge_face):
    side = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for a, b in fs[i]:
            if frozenset((a, b)) in cycle:
                continue
            j = edge_face[b, a]
            if j not in side:
                side.add(j)
                stack.append(j)
    return side
