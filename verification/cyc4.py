"""Enumerate cyclic 3-edge cuts in cubic plantri ASCII graphs."""
import itertools, sys


def parse(gline):
    n = int(gline.split(' ', 1)[0]); g = [[ord(c) - 97 for c in p] for p in gline.split(' ', 1)[1].split(',')]; return n, g


def cyclic_3cuts(n, g):
    edges = sorted({(min(u, v), max(u, v)) for u in range(n) for v in g[u]}); cuts = []
    for trio in itertools.combinations(edges, 3):
        banned = set(trio); seen = {0}; stack = [0]
        while stack:
            u = stack.pop()
            for v in g[u]:
                e = (min(u, v), max(u, v))
                if e in banned or v in seen: continue
                seen.add(v); stack.append(v)
        if len(seen) < n and 2 <= len(seen) <= n - 2: cuts.append(trio)
    return cuts


if __name__ == "__main__":
    lines = [l for l in open(sys.argv[1], encoding='latin-1').read().split('\n') if l.strip()]; out = open(sys.argv[2], 'w', encoding='latin-1') if len(sys.argv) > 2 else None; c4 = 0
    for i, l in enumerate(lines, 1):
        n, g = parse(l.strip()); cuts = cyclic_3cuts(n, g)
        print(f"graph {i}: n={n}, cyclic 3-edge cuts {len(cuts)}{' - CYCLICALLY 4-EDGE-CONNECTED' if not cuts else ''}", flush=True)
        if not cuts:
            c4 += 1
            if out: out.write(l.strip() + "\n")
    print(f"total cyclically 4-edge-connected: {c4} of {len(lines)}")
