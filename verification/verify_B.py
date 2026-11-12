"""Independent face-colour separation and defect checks for plantri ASCII input."""
import sys
from collections import Counter, deque
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from checks import faces, ham_cycles, inside_faces


def colour_by_vertices(fs, g):
    edge_face = {(a, b): i for i, f in enumerate(fs) for (a, b) in f}
    col = {}; fs0 = [edge_face[(0, w)] for w in g[0]]
    for c, f in enumerate(fs0): col[f] = c
    q = deque([0]); seen = {0}
    while q:
        v = q.popleft(); ff = [edge_face[(v, w)] for w in g[v]]; known = [f for f in ff if f in col]
        if len(known) == 2: col[[f for f in ff if f not in col][0]] = ({0, 1, 2} - {col[f] for f in known}).pop()
        elif len(known) < 2: raise RuntimeError("underdetermined")
        for w in g[v]:
            if w not in seen: seen.add(w); q.append(w)
    proper = all(col[edge_face[(a, b)]] != col[edge_face[(b, a)]] for (a, b) in edge_face)
    return col, edge_face, proper


def separating(gline):
    n = int(gline.split(' ', 1)[0]); g = [[ord(c) - 97 for c in p] for p in gline.split(' ', 1)[1].split(',')]
    fs = faces(g); cyc = ham_cycles(g); col, ef, proper = colour_by_vertices(fs, g); sep = Counter()
    for c in cyc:
        ins = inside_faces(c, fs, g, ef); outs = set(range(len(fs))) - ins
        cin = {col[i] for i in ins}; cout = {col[i] for i in outs}
        for x in range(3):
            for y in range(3):
                if x != y and x not in cout and y not in cin: sep[(x, y)] += 1
    return n, len(fs), tuple(sorted(Counter(len(f) for f in fs).items())), len(cyc), proper, dict(sep)


def defect_and_forced(gline):
    """Minimize misassigned faces over cycles and distinct colour pairs."""
    n = int(gline.split(' ', 1)[0]); g = [[ord(c) - 97 for c in p] for p in gline.split(' ', 1)[1].split(',')]
    fs = faces(g); cyc = ham_cycles(g); col, ef, proper = colour_by_vertices(fs, g); best = None
    for c in cyc:
        ins = inside_faces(c, fs, g, ef); cin = Counter(col[i] for i in ins); cout = Counter(col[i] for i in range(len(fs)) if i not in ins)
        d = min(cout[x] + cin[y] for x in range(3) for y in range(3) if x != y); best = d if best is None else min(best, d)
    forced = frozenset.intersection(*cyc) if cyc else frozenset()
    return len(cyc), best, len(forced), max(len(f) for f in fs)


if __name__ == "__main__":
    for i, l in enumerate([l for l in open(sys.argv[1], encoding='latin-1').read().split('\n') if l.strip()], 1):
        n, nf, prof, h, proper, sep = separating(l.strip()); h2, d, nforced, maxface = defect_and_forced(l.strip())
        print(f"graph {i}: n={n}, faces {nf} {prof}, cycles {h}, proper colouring {proper}; separating cycles by colour pair: {sep if sep else 'NONE'}; defect {d}, forced edges {nforced}, max face {maxface}")
