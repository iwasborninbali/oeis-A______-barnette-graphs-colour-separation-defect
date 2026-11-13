"""Launch/resume independent plantri res/mod partitions, with atomic completion markers.
Usage: python run_parts.py F modulus start end jobs
Never reuses a result unless the COMPLETE marker and planar-code output exist.
"""
import sys, os, pathlib, time, subprocess, concurrent.futures
F,MOD,START,END,JOBS=map(int,sys.argv[1:])
base=pathlib.Path(__file__).resolve().parents[1]
plantri=base/'third_party'/'plantri55'/'plantri'
if not plantri.exists():
    plantri=base.parents[3]/'plantri55'/'plantri'
checker=base/'src'/'check_barnette'
assert plantri.exists(),plantri

def run(res):
    name=f'F{F}_{res}of{MOD}'
    parts=base/'parts';logs=base/'logs';graphs=base/'graphs'
    path=parts/(name+'.txt'); out=graphs/(name+'.pcode'); tmp=graphs/(name+'.pcode.incomplete')
    if path.exists() and out.exists() and path.read_text().startswith('COMPLETE'):
        return f'SKIP {name} {path.read_text().strip()}'
    t=time.monotonic()
    with open(logs/(name+'.plantri.log'),'wb') as plog, open(logs/(name+'.check.log'),'wb') as clog, open(parts/(name+'.incomplete'),'wb') as summary:
        p=subprocess.Popen([str(plantri),'-dbc3',str(F),f'{res}/{MOD}'],stdout=subprocess.PIPE,stderr=plog)
        q=subprocess.Popen([str(checker),str(F),str(tmp)],stdin=p.stdout,stdout=summary,stderr=clog)
        p.stdout.close()
        qret=q.wait(); pret=p.wait()
    if qret or pret:
        raise RuntimeError(f'{name}: plantri={pret}, checker={qret}; see logs')
    text=(parts/(name+'.incomplete')).read_text()
    assert text.startswith('COMPLETE'),(name,text)
    os.replace(tmp,out)
    os.replace(parts/(name+'.incomplete'),path)
    return f'DONE {name} wall={time.monotonic()-t:.3f}s {text.strip()}'

print(f'RUN F={F} modulus={MOD} parts=[{START},{END}) parallel={JOBS}',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
    futures={pool.submit(run,i):i for i in range(START,END)}
    for future in concurrent.futures.as_completed(futures):
        print(future.result(),flush=True)
