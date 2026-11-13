"""Independently check S2-positive sample graphs from fresh plantri streams."""
from pathlib import Path
import subprocess, tempfile, sys
from verify_independent import load,face_data,s2,s1
ROOT=Path(__file__).resolve().parents[1]
PLANTRI=ROOT.parents[3]/'plantri55'/'plantri'
for F in (22,23,24,25,26,27,28):
    proc=subprocess.Popen([str(PLANTRI),'-dbc3',str(F)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    n=2*F-4
    buf=proc.stdout.read(15)
    assert buf==b'>>planar_code<<'
    for i in range(20):
        code=proc.stdout.read(1+4*n)
        if len(code)!=1+4*n:raise RuntimeError(f'Short source F={F}, i={i}')
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf+code);f.flush()
            adj,=load(f.name)
        dual,colors,_=face_data(adj)
        assert s2(dual,colors), f'S2 failed at F={F}, sample={i}'
    proc.kill()
    proc.communicate()
    print(f'F={F} n={n} S2-positive sample 20/20, independent dual test',flush=True)
