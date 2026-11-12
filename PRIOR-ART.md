# Prior art and credit

On 2026-11-13 the OEIS JSON searches `0,0,0,0,0,2,0,8,88`, `0,0,2,0,8,88`, `2,0,8,88`, and `Barnette face colour separation defect` each returned `null` (zero results). The first two omit leading zeros; the last numeric query starts at the first nonzero term. The many leading zeros make search inconclusive. [A007083](https://oeis.org/A007083) counts all graphs in the class, not just those with the defect. [A216800](https://oeis.org/A216800) contains some of the same small values but counts a different object. No claim of OEIS novelty follows from these searches.

Alt, Payne, Schmidt and Wood, [“Thoughts on Barnette's conjecture”](https://ajc.maths.uq.edu.au/pdf/64/ajc_v64_p354.pdf), Australasian J. Combin. 64 (2016), 354–365, Theorem 4 and Lemma 5, establish examples in dual terms for which no Hamiltonian cycle separates the two colours; the qualitative failure of universal separation was known. Their Theorem 4 is stronger than merely asserting positive defect. On p. 361 the authors mention examples without separating triangles but omit details. The source research notes a potential omitted step in the printed proof; this repository does not verify that proof or the precise size of their examples.

Holton, Manvel and McKay, “Hamiltonian cycles in cubic 3-connected bipartite planar graphs”, J. Combin. Theory B 38 (1985), 279–297, investigated Hamiltonicity of this graph class. Brinkmann and McKay, “Fast generation of planar graphs”, MATCH 58 (2007), 323–357, describe plantri's generator. A007083 supplies an independent published census of class sizes, not a verification of the separation property.

The lab source ledger attributes the August 2026 census and stored graphs to vtora; `verify_B.py` and `cyc4.py` are lab checks. Whether the particular order-by-order defect table was previously known has not been established.

Full-term and shifted OEIS JSON searches on 2026-11-13 also returned `null` (zero results): `0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,8,88`, `0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,8,88`, and `0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,8,88`.
