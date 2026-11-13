"""Re-run plantri for small sizes and check every positive S2 by an independent algorithm."""
import sys, pathlib, subprocess, tempfile
from verify_independent import load,face_data,s2,s1
base=pathlib.Path(__file__).resolve().parents[1]
plantri=base/'third_party'/'plantri55'/'plantri'
if not plantri.exists():plantri=base.parents[3]/'plantri55'/'plantri'
for F in [6,8,9,10,11,12,13,14,15,16]:
    data=subprocess.check_output([str(plantri),'-dbc3',str(F)],stderr=subprocess.DEVNULL)
    with tempfile.NamedTemporaryFile(suffix='.pcode') as tmp:
        tmp.write(data);tmp.flush()
        k=0
        for a in load(tmp.name):
            d,c,_=face_data(a)
            assert s2(d,c), ('failed S2 crosscheck',F,k)
            assert s1(d,c), ('failed S1 crosscheck',F,k)
            k+=1
        print('SMALL_CHECK F=',F,'n=',2*F-4,'graphs=',k,flush=True)
