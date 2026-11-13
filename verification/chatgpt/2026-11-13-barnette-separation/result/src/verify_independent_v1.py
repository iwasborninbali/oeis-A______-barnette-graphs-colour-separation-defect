"""Independent Python checker via connectivity of face regions (not cycle walking).
Takes planar-code containing non-S2 graphs, checks absence of S2 and existence/absence of S1.
For S1, exhaustive face assignments with an independent-set pruning rule.
"""
import sys, itertools, collections, time

def load(path):
    z=open(path,'rb').read()
    assert z.startswith(b'>>planar_code<<');z=z[len(b'>>planar_code<<'):]
    i=0
    while i<len(z):
        n=z[i];i+=1
        adj=[]
        for v in range(n):
            end=z.index(0,i);adj.append([x-1 for x in z[i:end]]);i=end+1
        yield adj

def face_data(adj):
    n=len(adj);face={};ff=[]
    for u in range(n):
        for v in adj[u]:
            if (u,v) in face: continue
            f=len(ff);walk=[];a,b=u,v
            while (a,b) not in face:
                face[a,b]=f;walk.append((a,b))
                at=adj[b].index(a)
                a,b=b,adj[b][(at-1)%3] # opposite orientation versus C
            assert (a,b)==(u,v)
            ff.append(walk)
    assert len(ff)==n//2+2
    du=[set() for _ in ff]
    for (u,v),f in face.items():
        g=face[v,u]
        du[f].add(g)
    colours=[None]*len(ff)
    for j,v in enumerate(adj[0]):colours[face[0,v]]=j
    while None in colours:
        progress=False
        for u in range(n):
            fs=[face[u,v] for v in adj[u]]
            known=[colours[f] for f in fs]
            if known.count(None)==1:
                missing=({0,1,2}-set(x for x in known if x is not None)).pop()
                colours[fs[known.index(None)]]=missing;progress=True
        assert progress
    return du,colours,face

def conn(du,mask):
    if not mask:return False
    bits=mask & -mask
    reached=bits
    while True:
        old=reached
        for i in range(len(du)):
            if reached>>i & 1:
                for j in du[i]:
                    if mask>>j&1:reached|=1<<j
        if reached==old:break
    return reached==mask

def separate(du,inside):
    full=(1<<len(du))-1
    return conn(du,inside) and conn(du,full^inside)

def s2(du,col):
    base=[sum(1<<i for i,c in enumerate(col) if c==x) for x in range(3)]
    for free in range(3):
        x,y=[q for q in range(3) if q!=free]
        fs=[i for i,c in enumerate(col) if c==free]
        for k in range(1<<len(fs)):
            inside=base[x]
            for j,f in enumerate(fs):
                if k>>j&1: inside|=1<<f
            if separate(du,inside):return True
    return False

def s1(du,col):
    base=[sum(1<<i for i,c in enumerate(col) if c==x) for x in range(3)]
    for x in range(3):
        fs=[i for i,c in enumerate(col) if c!=x]
        fs.sort(key=lambda f:-sum(col[g]!=x for g in du[f]))
        def dfs(pos,inside,excluded):
            if pos==len(fs):return separate(du,inside)
            f=fs[pos]
            if not(excluded>>f&1):
                newexcluded=excluded
                for g in du[f]:
                    if col[g]!=x:newexcluded|=1<<g
                if dfs(pos+1,inside|1<<f,newexcluded):return True
            return dfs(pos+1,inside,excluded)
        if dfs(0,base[x],0):return True
    return False

if __name__=='__main__':
    for path in sys.argv[1:]:
        t=time.monotonic();ns2=ns1=0;cnt=0
        for adj in load(path):
            du,co,fc=face_data(adj)
            assert not s2(du,co), 'Unexpected S2 graph in no-S2 output'
            ns2+=1
            ns1+=not s1(du,co)
            cnt+=1
        print(path, 'total_noS2',cnt, 'total_noS1',ns1,'seconds',round(time.monotonic()-t,3),flush=True)
