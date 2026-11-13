/* Exact S2/S1 checker for cubic plane bipartite graphs in planar_code.
 * Usage: check_barnette [F] [non_S2.planar_code]
 * Input: planar_code on stdin, streamed from plantri -dbc3 F [res/mod].
 * Each input graph is classified independently; outputs non-S2 codes as read.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>
#include <time.h>

#define NV 64
#define NF 40
static int n,F, adj[NV][3], rev[NV][3], faces_of_dart[NV*3];
static int fc[NF], vf[NV][3], by_missing[NV][3];
static uint64_t dualadj[NF];
static void die(const char *s);
static uint64_t attemptsS2, attemptsS1;
#define MAXCLASS 14
static uint16_t s2order[MAXCLASS][1<<(MAXCLASS-1)];
static int s2order_ready[MAXCLASS];
static void build_order(int k) {
  if(k>=MAXCLASS) die("too many same-colour faces");
  if(s2order_ready[k]) return;
  int cnt=0,lim=1<<k;
  for(int d=0;d<=k;d++) for(int i=0;i<lim;i++)
    if(abs(2*__builtin_popcount((unsigned int)i)-k)==d) s2order[k][cnt++]=i;
  if(cnt!=lim) die("mask permutation broken");
  s2order_ready[k]=1;
}
static uint64_t noS2, noS1, graphs;



static void die(const char *s) { fprintf(stderr,"ERROR: %s (graph=%" PRIu64 ", n=%d, F=%d)\n", s,graphs,n,F); exit(2); }

static int read_one(unsigned char *raw, int *rawlen) {
  int c=fgetc(stdin);
  if(c==EOF) return 0;
  if(c=='>' ) { // planar_code header; can appear on concatenated streams
     char header[64]; int k=0; header[k++]=(char)c;
     while (k<63 && (c=fgetc(stdin))!=EOF) { header[k++]=(char)c; if(c=='<' && k>=2 && header[k-2]=='<') break; }
     header[k]=0;
     if(strcmp(header,">>planar_code<<")!=0) die("bad planar_code header");
     c=fgetc(stdin);
  }
  if(c==EOF) return 0;
  if(c==0) die("unsupported extended planar_code");
  n=c;
  if(n>NV || n<4 || (n&1)) die("invalid vertex count");
  int len=0; raw[len++]=(unsigned char)n;
  for(int u=0;u<n;u++) {
    int j=0;
    while((c=fgetc(stdin))!=EOF && c) {
      if(len>=NV*4+1 || j>=3 || c>n) die("bad neighbour list");
      raw[len++]=(unsigned char)c; adj[u][j++]=c-1;
    }
    if(c==EOF || j!=3) die("bad degree or EOF");
    raw[len++]=0;
  }
  *rawlen=len;
  return 1;
}

static void prepare_graph(void) {
  for(int u=0;u<n;u++) for(int j=0;j<3;j++) {
    int v=adj[u][j], found=-1;
    if(u==v) die("self-loop");
    for(int k=0;k<3;k++) if(adj[v][k]==u) { if(found>=0) die("multi reciprocal"); found=k; }
    if(found<0) die("missing reciprocal");
    rev[u][j]=found;
  }
  for(int d=0;d<3*n;d++) faces_of_dart[d]=-1;
  F=0;
  for(int d=0;d<3*n;d++) if(faces_of_dart[d]<0) {
    int cur=d, hops=0;
    if(F>=NF) die("too many faces");
    do {
      if(faces_of_dart[cur]>=0) die("facial walk crossed");
      faces_of_dart[cur]=F;
      int u=cur/3,j=cur%3,v=adj[u][j],k=rev[u][j];
      cur=3*v+(k+1)%3;
      if(++hops>3*n) die("face too long");
    } while (cur!=d);
    F++;
  }
  if(F!=n/2+2) die("Euler formula wrong");
  for(int f=0;f<F;f++) { fc[f]=-1; dualadj[f]=0; }
  for(int u=0;u<n;u++) for(int j=0;j<3;j++) {
    int a=faces_of_dart[3*u+j], v=adj[u][j], b=faces_of_dart[3*v+rev[u][j]];
    if(a==b) die("bridge");
    dualadj[a] |= (uint64_t)1<<b;
  }
  // Face-colouring by propagation through the three triangular sectors at vertices.
  for(int j=0;j<3;j++) {
    int f=faces_of_dart[j];
    for(int k=0;k<j;k++) if(faces_of_dart[k]==f) die("nontriangular dual vertex");
    fc[f]=j;
  }
  int unfilled=F-3;
  while(unfilled) {
    int progress=0;
    for(int u=0;u<n;u++) {
      int id[3], seen[3]={0,0,0}, missing=-1, known=0;
      for(int j=0;j<3;j++) {
        id[j]=faces_of_dart[3*u+j];
        if(fc[id[j]]<0) missing=id[j];
        else { if(seen[fc[id[j]]]++) die("invalid colour propagation"); known++; }
      }
      if(known==2) {
        int x=0; while(seen[x])x++;
        fc[missing]=x; progress++; unfilled--;
      }
    }
    if(!progress) die("face colouring propagation stuck");
  }
  for(int u=0;u<n;u++) {
    for(int c=0;c<3;c++) vf[u][c]=-1,by_missing[u][c]=-1;
    for(int j=0;j<3;j++) {
      int f=faces_of_dart[3*u+j];
      if(vf[u][fc[f]]>=0) die("repeated face colour at vertex");
      vf[u][fc[f]]=f;
      int v=adj[u][j], g=faces_of_dart[3*v+rev[u][j]];
      int miss=3-fc[f]-fc[g]; // 0+1+2 ==3
      if(miss<0 || miss>2 || fc[f]==fc[g]) die("bad adjacent colours");
      by_missing[u][miss]=v;
    }
    for(int c=0;c<3;c++) if(by_missing[u][c]<0 || vf[u][c]<0) die("missing vertex colour");
  }
}

static int testS2(void) {
  int counts[3]={0,0,0}, index[NF], order[3]={0,1,2};
  for(int i=0;i<F;i++) counts[fc[i]]++;
  // Try the colour with fewest faces as free variable first.
  for(int a=0;a<3;a++) for(int b=a+1;b<3;b++) if(counts[order[b]]<counts[order[a]]) {
    int t=order[a]; order[a]=order[b];order[b]=t;
  }
  for(int i=0;i<3;i++) {
    int z=order[i],x=(z+1)%3,y=(z+2)%3, cnt=0;
    int zloc[NV];
    for(int f=0;f<F;f++) if(fc[f]==z) index[f]=cnt++;
    if(cnt>30) die("S2 enumeration overflow");
    for(int u=0;u<n;u++) zloc[u]=index[vf[u][z]];
    uint32_t lim=(uint32_t)1<<cnt;
    build_order(cnt);
    for(uint32_t ii=0;ii<lim;ii++) {
      uint32_t mask=s2order[cnt][ii];
      attemptsS2++;
      int u=0,steps=0;
      do {
        int w=by_missing[u][z]; // mandatory edge between x and y faces
        u=by_missing[w][(mask & ((uint32_t)1<<zloc[w]))?x:y];
        steps++;
      } while(u!=0 && steps<n/2);
      if(u==0 && steps==n/2) return 1;
    }
  }
  return 0;
}

static uint32_t blocked[NF];
static int fidx[NF], others[NF], m, one_x;
static int excluded[NV];

static int testS1_cycle(uint32_t mask) {
  attemptsS1++;
  for(int u=0;u<n;u++) {
    int y=(one_x+1)%3,z=(one_x+2)%3;
    int yi=fidx[vf[u][y]], zi=fidx[vf[u][z]];
    int iy=!!(mask & ((uint32_t)1<<yi));
    int iz=!!(mask & ((uint32_t)1<<zi));
    if(iy && iz) die("invalid S1 independent set");
    excluded[u]=by_missing[u][iy?z:(iz?y:one_x)];
  }
  int u=0, prev=-1,steps=0;
  do {
    int next=-1;
    for(int j=0;j<3;j++) if(adj[u][j]!=excluded[u] && adj[u][j]!=prev) {
      next=adj[u][j];break;
    }
    if(next<0) die("broken S1 cycle");
    prev=u;u=next;steps++;
  } while(u!=0 && steps<n);
  return u==0 && steps==n;
}

static int s1_dfs(int pos, uint32_t selected, uint32_t forbidden) {
  if(pos==m) return testS1_cycle(selected);
  uint32_t bit=(uint32_t)1<<pos;
  // Try including a face (connects interior components) first.
  if(!(forbidden&bit)) {
    if(s1_dfs(pos+1,selected|bit,forbidden|blocked[pos])) return 1;
  }
  return s1_dfs(pos+1,selected,forbidden);
}

static int testS1(void) {
  for(int x=0;x<3;x++) {
    one_x=x;m=0;
    for(int f=0;f<F;f++) fidx[f]=-1;
    for(int f=0;f<F;f++) if(fc[f]!=x) { fidx[f]=m; others[m++]=f; }
    if(m>=31) die("S1 enumeration overflow");
    for(int i=0;i<m;i++) blocked[i]=0;
    int y=(x+1)%3,z=(x+2)%3;
    for(int u=0;u<n;u++) {
      int i=fidx[vf[u][y]],j=fidx[vf[u][z]];
      if(i<0 || j<0 || i==j) die("bad S1 adjacency");
      blocked[i] |= (uint32_t)1<<j;
      blocked[j] |= (uint32_t)1<<i;
    }
    if(s1_dfs(0,0,0)) return 1;
  }
  return 0;
}

static double now(void){ struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9; }

int main(int argc,char **argv) {
  if(argc!=3) { fprintf(stderr,"usage: %s F nonS2.planar_code\n",argv[0]); return 2; }
  int argF=atoi(argv[1]);
  FILE *out=fopen(argv[2],"wb"); if(!out) {perror("output");return 2;}
  fputs(">>planar_code<<",out);
  double t0=now();
  unsigned char raw[NV*4+2]; int len;
  while(read_one(raw,&len)) {
    prepare_graph();
    if(F!=argF)die("unexpected number of faces");
    graphs++;
    if(!testS2()) {
      noS2++;
      if(fwrite(raw,1,len,out)!=(size_t)len) die("write error");
      if(!testS1())noS1++;
    }
    if(graphs%1000000==0) {
      fprintf(stderr,"PROGRESS F=%d graphs=%" PRIu64 " noS2=%" PRIu64 " noS1=%" PRIu64 " time=%.3f\n",F,graphs,noS2,noS1,now()-t0);
      fflush(stderr);
    }
  }
  if(fclose(out))die("close error");
  printf("COMPLETE F=%d n=%d graphs=%" PRIu64 " noS2=%" PRIu64 " noS1=%" PRIu64 " attemptsS2=%" PRIu64 " attemptsS1=%" PRIu64 " seconds=%.6f\n",argF,2*argF-4,graphs,noS2,noS1,attemptsS2,attemptsS1,now()-t0);
  return 0;
}
