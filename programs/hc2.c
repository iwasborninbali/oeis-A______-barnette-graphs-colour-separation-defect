
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 64
typedef unsigned __int128 u128;
static int n, adj[MAXN][3], eid[MAXN][MAXN], m, nf, face_of[MAXN][MAXN], fsize[MAXN], fcol[MAXN];
static int visited[MAXN], avail[MAXN], path[MAXN]; static long h; static uint64_t pairs[64]; static int bok, mindef; static u128 forced; static int haveforced;
static int cycle_defect(u128 cyc){ static int side[MAXN], st[MAXN]; memset(side, 0, sizeof(int) * nf); int sp = 0; st[sp++] = 0; side[0] = 1;
    while (sp){ int f = st[--sp]; for (int u = 0; u < n; u++) for (int i = 0; i < 3; i++){ int v = adj[u][i]; if (face_of[u][v] != f) continue;
        if ((cyc >> eid[u][v]) & 1) continue; int g = face_of[v][u]; if (!side[g]){ side[g] = 1; st[sp++] = g; } } }
    int cin[3] = {0,0,0}, cout[3] = {0,0,0}; for (int f = 0; f < nf; f++){ if (side[f]) cin[fcol[f]]++; else cout[fcol[f]]++; }
    int best = 1 << 30; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) if (x != y){ int d = cout[x] + cin[y]; if (d < best) best = d; } return best; }
static void found(void){ if (path[1] > path[n-1]) return; h++; u128 cyc = 0; int es[MAXN];
    for (int i = 0; i < n; i++){ int u = path[i], v = path[(i + 1) % n]; es[i] = eid[u][v]; cyc |= (u128)1 << es[i]; }
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++){ int a = es[i] < es[j] ? es[i] : es[j], b = es[i] < es[j] ? es[j] : es[i]; int p = b * (b - 1) / 2 + a; pairs[p >> 6] |= 1ULL << (p & 63); }
    if (haveforced) forced &= cyc; else { forced = cyc; haveforced = 1; }
    if (mindef > 0){ int d = cycle_defect(cyc); if (d < mindef) mindef = d; } }
static void dfs(int u, int depth){
    if (depth == n){ for (int i = 0; i < 3; i++) if (adj[u][i] == 0) found(); return; }
    for (int i = 0; i < 3; i++){ int w = adj[u][i]; if (visited[w]) continue; int ok = 1;
        if (depth > 1) for (int j = 0; j < 3; j++){ int x = adj[u][j]; if (x != w && !visited[x]){ if (--avail[x] < 2) ok = 0; } }
        if (ok){ visited[w] = 1; path[depth] = w; dfs(w, depth + 1); visited[w] = 0; }
        if (depth > 1) for (int j = 0; j < 3; j++){ int x = adj[u][j]; if (x != w && !visited[x]) avail[x]++; } } }
static int colour_faces(void){ for (int f = 0; f < nf; f++) fcol[f] = -1; static int q[MAXN], seen[MAXN]; memset(seen, 0, sizeof seen); int qh = 0, qt = 0;
    fcol[face_of[0][adj[0][0]]] = 0; fcol[face_of[0][adj[0][1]]] = 1; fcol[face_of[0][adj[0][2]]] = 2; q[qt++] = 0; seen[0] = 1;
    while (qh < qt){ int v = q[qh++]; int fs[3]; for (int i = 0; i < 3; i++) fs[i] = face_of[v][adj[v][i]];
        int used = 0, miss = -1, cnt = 0; for (int i = 0; i < 3; i++){ if (fcol[fs[i]] >= 0){ used |= 1 << fcol[fs[i]]; cnt++; } else miss = i; }
        if (cnt == 2) fcol[fs[miss]] = used == 3 ? 2 : used == 5 ? 1 : 0; else if (cnt < 2) return 0;
        for (int i = 0; i < 3; i++){ int w = adj[v][i]; if (!seen[w]){ seen[w] = 1; q[qt++] = w; } } }
    for (int u = 0; u < n; u++) for (int i = 0; i < 3; i++){ int v = adj[u][i]; if (fcol[face_of[u][v]] == fcol[face_of[v][u]]) return 0; } return 1; }
int main(int argc, char **argv){
    int verbose = argc > 1 && !strcmp(argv[1], "-v"); int printdef = argc > 1 && !strcmp(argv[1], "-d");  char line[8192]; long graphs = 0, failA_pairs = 0, failA_graphs = 0, forced_graphs = 0, forced_edges = 0, defhist[4] = {0,0,0,0}, maxdef = 0, minh = -1, g6 = 0, g6def[4] = {0,0,0,0}; char minprof[256] = "";
    while (fgets(line, sizeof line, stdin)){
        char *p = line; n = (int)strtol(p, &p, 10); if (n <= 0 || n > MAXN) continue; while (*p == ' ') p++;
        for (int v = 0; v < n; v++){ for (int i = 0; i < 3; i++) adj[v][i] = (int)(unsigned char)p[i] - 'a'; p += 3; if (*p == ',') p++; }
        m = 0; for (int u = 0; u < n; u++) for (int i = 0; i < 3; i++){ int v = adj[u][i]; if (u < v){ eid[u][v] = eid[v][u] = m; m++; } }
        static int seen[MAXN][MAXN]; memset(seen, 0, sizeof seen); nf = 0;
        for (int u = 0; u < n; u++) for (int i = 0; i < 3; i++){ int v = adj[u][i]; if (seen[u][v]) continue; int a = u, b = v, len = 0;
            while (!seen[a][b]){ seen[a][b] = 1; face_of[a][b] = nf; len++; int k = 0; while (adj[b][k] != a) k++; int nx = adj[b][(k + 1) % 3]; a = b; b = nx; } fsize[nf++] = len; }
        int col_ok = colour_faces(); int maxface = 0; for (int f = 0; f < nf; f++) if (fsize[f] > maxface) maxface = fsize[f];
        memset(visited, 0, sizeof visited); memset(pairs, 0, sizeof pairs); h = 0; bok = 0; mindef = 1 << 30; haveforced = 0; forced = 0;
        for (int v = 0; v < n; v++) avail[v] = 3; visited[0] = 1; path[0] = 0; dfs(0, 1);
        long npairs = (long)m * (m - 1) / 2, cov = 0; for (int p2 = 0; p2 < npairs; p2++) if (pairs[p2 >> 6] >> (p2 & 63) & 1) cov++;
        long fa = npairs - cov; int nforced = 0; for (int e = 0; e < m; e++) if ((forced >> e) & 1) nforced++; if (h == 0) nforced = -1;
        int d = mindef > 3 ? 3 : mindef; graphs++; failA_pairs += fa; if (fa) failA_graphs++; if (nforced > 0){ forced_graphs++; forced_edges += nforced; }
        defhist[d]++; if (mindef > maxdef) maxdef = mindef; if (maxface <= 6){ g6++; g6def[d]++; }
        int cnt[MAXN] = {0}; for (int f = 0; f < nf; f++) cnt[fsize[f]]++; char prof[256] = ""; for (int s = 0; s < MAXN; s++) if (cnt[s]){ char t[32]; sprintf(t, "%d^%d ", s, cnt[s]); strcat(prof, t); }
        if (minh < 0 || h < minh){ minh = h; strcpy(minprof, prof); }
        int bad = fa || nforced != 0 || mindef >= 2 || (maxface <= 6 && mindef >= 1) || !col_ok;
        if (bad){ printf("FAIL %s%s%s%s%s h=%ld failA_pairs=%ld forced=%d defect=%d %s", fa ? "A" : "", nforced > 0 ? "F" : "", mindef >= 2 ? "D2" : "", (maxface <= 6 && mindef >= 1) ? "G" : "", !col_ok ? "C" : "", h, fa, nforced, mindef, line); fflush(stdout); }
        else if (printdef && mindef >= 1){ printf("DEF %d h=%ld %s", mindef, h, line); fflush(stdout); }
        else if (verbose) printf("G h=%ld failA_pairs=%ld forced=%d defect=%d faces %s\n", h, fa, nforced, mindef, prof); }
    printf("SUMMARY graphs=%ld failA_pairs=%ld failA_graphs=%ld forced_graphs=%ld forced_edges=%ld def0=%ld def1=%ld def2=%ld def3plus=%ld maxdef=%ld g6=%ld g6def0=%ld g6def1plus=%ld minh=%ld minprof=%s\n",
        graphs, failA_pairs, failA_graphs, forced_graphs, forced_edges, defhist[0], defhist[1], defhist[2], defhist[3], maxdef, g6, g6def[0], g6def[1] + g6def[2] + g6def[3], minh, minprof);
    return 0; }
