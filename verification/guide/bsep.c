/* Guide's independent count (13 Nov 2026). Input: plantri -dbc3 output (planar code), i.e. Barnette graphs (3-connected
   cubic bipartite plane graphs). Output: how many of them have NO Hamiltonian cycle C with all faces of one colour x inside
   C and all faces of another colour y outside (faces properly 3-coloured; the colouring is unique up to permutation).
   Graphs without any Hamiltonian cycle are counted as having none.

   Method (no enumeration of Hamiltonian cycles). At each vertex the three faces have the three colours, so each edge has a
   type {c1,c2}. Let z be the third colour. An edge is on C iff its two faces lie on different sides of C. Hence if x-faces
   are inside and y-faces outside: every {x,y}-edge is on C, and for each z-face f: if f is outside its {x,z}-edges are on C
   and its {y,z}-edges are not; if inside, the reverse. Conversely, for a set S of z-faces ("inside"), let F be the {x,y}-edges,
   the {y,z}-edges of faces in S and the {x,z}-edges of faces not in S; every vertex meets exactly two edges of F. If F is a
   single cycle C, label x-faces and faces in S by A and y-faces and the other z-faces by B: two adjacent faces get the same
   label exactly when their common edge is not in F. Crossing an edge of a cycle changes sides and crossing any other edge
   does not, and the faces form a connected adjacency graph, so the labels are the sides of C: x-faces on one side, y-faces
   on the other. So a separating Hamiltonian cycle exists iff for some z and some S the set F is one cycle of length n.
   The program tries the 3 choices of z and all 2^k subsets S of the k z-faces, stopping at the first success. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXV 128
static int n, adj[MAXV][3], fid[MAXV][3], nf, fcol[2 * MAXV];
static int other(int v, int u) { for (int i = 0; i < 3; i++) if (adj[v][i] == u) return i; return -1; }
static int read_graph(FILE *in) {
  int c = getc(in); if (c == EOF) return 0; n = c; if (n == 0) { fprintf(stderr, "n >= 256 not supported\n"); exit(2); }
  for (int v = 0; v < n; v++) { for (int i = 0; i < 3; i++) { int w = getc(in); if (w <= 0) { fprintf(stderr, "not cubic\n"); exit(2); } adj[v][i] = w - 1; }
    if (getc(in) != 0) { fprintf(stderr, "not cubic\n"); exit(2); } }
  return 1;
}
static int analyse(void) {           /* returns 1 if a separating Hamiltonian cycle exists */
  for (int v = 0; v < n; v++) for (int i = 0; i < 3; i++) fid[v][i] = -1;
  nf = 0;
  for (int v = 0; v < n; v++) for (int i = 0; i < 3; i++) if (fid[v][i] < 0) {   /* face of directed edge v -> adj[v][i] */
    int a = v, j = i;
    while (fid[a][j] < 0) { fid[a][j] = nf; int b = adj[a][j]; int k = other(b, a); a = b; j = (k + 1) % 3; }
    nf++;
  }
  if (nf != n / 2 + 2) { fprintf(stderr, "Euler check failed\n"); exit(3); }
  /* face colouring: faces at a vertex = fid[v][0..2] */
  for (int f = 0; f < nf; f++) fcol[f] = -1;
  fcol[fid[0][0]] = 0; fcol[fid[0][1]] = 1; fcol[fid[0][2]] = 2;
  for (int changed = 1; changed;) { changed = 0;
    for (int v = 0; v < n; v++) { int cnt = 0, used = 0, miss = -1;
      for (int i = 0; i < 3; i++) { int c = fcol[fid[v][i]]; if (c >= 0) { cnt++; used |= 1 << c; } else miss = i; }
      if (cnt == 2) { fcol[fid[v][miss]] = (used == 3) ? 2 : (used == 5) ? 1 : 0; changed = 1; }
      else if (cnt == 3 && used != 7) { fprintf(stderr, "faces not properly 3-coloured\n"); exit(3); } } }
  for (int f = 0; f < nf; f++) if (fcol[f] < 0) { fprintf(stderr, "uncoloured face\n"); exit(3); }
  for (int v = 0; v < n; v++) { int used = 0; for (int i = 0; i < 3; i++) used |= 1 << fcol[fid[v][i]]; if (used != 7) { fprintf(stderr, "bad colouring\n"); exit(3); } }
  /* edge v-adj[v][i] has faces fid[v][i] and fid[adj[v][i]][other] */
  for (int z = 0; z < 3; z++) {
    int zf[MAXV], k = 0, zidx[2 * MAXV];
    for (int f = 0; f < nf; f++) { zidx[f] = -1; if (fcol[f] == z) { zidx[f] = k; zf[k++] = f; } }
    if (k > 30) { fprintf(stderr, "too many z-faces\n"); exit(4); }
    /* for each vertex: its {x,y}-edge (always on C), and its z-face with the edge of type {x,z} and {y,z} */
    int xy[MAXV], ez[MAXV][2], zface[MAXV];
    int x = (z + 1) % 3;
    for (int v = 0; v < n; v++) for (int i = 0; i < 3; i++) {
      int u = adj[v][i], f1 = fid[v][i], f2 = fid[u][other(u, v)];
      int c1 = fcol[f1], c2 = fcol[f2];
      if (c1 != z && c2 != z) xy[v] = u;
      else { int zfce = c1 == z ? f1 : f2, oc = c1 == z ? c2 : c1; zface[v] = zidx[zfce]; ez[v][oc == x ? 0 : 1] = u; }
    }
    for (long s = 0; s < (1L << k); s++) {      /* bit set: z-face inside -> its {y,z} edges on C; else {x,z} edges */
      int prev = -1, cur = 0, len = 0;
      do { int nb1 = xy[cur], nb2 = ez[cur][(s >> zface[cur]) & 1 ? 1 : 0];
           int nxt = (nb1 != prev) ? nb1 : nb2; if (nb1 == nb2) { len = -1; break; }
           prev = cur; cur = nxt; len++; } while (cur != 0 && len <= n);
      if (len == n) return 1;
    }
  }
  return 0;
}
int main(void) {
  char hdr[15]; if (fread(hdr, 1, 15, stdin) != 15 || memcmp(hdr, ">>planar_code<<", 15)) { fprintf(stderr, "expected planar_code\n"); return 2; }
  long graphs = 0, bad = 0; int order = -1;
  while (read_graph(stdin)) { if (order < 0) order = n; graphs++; if (!analyse()) { bad++; } }
  printf("vertices=%d graphs=%ld no_separating_hamiltonian_cycle=%ld\n", order, graphs, bad);
  return 0;
}
