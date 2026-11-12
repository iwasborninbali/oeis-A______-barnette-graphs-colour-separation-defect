#!/usr/bin/env python3
import re
from pathlib import Path
old = Path('verification/logs/verify_B_44.txt').read_text()
new = Path('verification/logs/fast_44.txt').read_text()
x = [int(a) for a in re.findall(r'cycles (\d+),', old)]
y = [int(a) for a in re.findall(r'cycles=(\d+)', new)]
assert x == y and len(x) == 8
print('Direct and fast cycle counts agree on all 8 graphs:', *x)
