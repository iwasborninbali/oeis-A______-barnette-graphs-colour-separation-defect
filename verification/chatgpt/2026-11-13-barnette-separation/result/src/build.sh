#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HERE/third_party"
tar xzf "$HERE/third_party/plantri55.tar.gz" -C "$HERE/third_party"
make -C "$HERE/third_party/plantri55" plantri
gcc -O3 -std=c11 -Wall -Wextra -pedantic -o "$HERE/src/check_barnette" "$HERE/src/check_barnette.c"
echo "built $HERE/third_party/plantri55/plantri and $HERE/src/check_barnette"
