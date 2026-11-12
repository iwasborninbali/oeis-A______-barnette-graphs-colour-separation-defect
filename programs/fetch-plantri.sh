#!/bin/sh
set -eu
url=https://www-ftp.lip6.fr/pub/math/sagemath/spkg/upstream/plantri/plantri55.tar.gz
curl -fL "$url" -o plantri55.tar.gz
printf '%s  %s\n' 911cdf5bcca7294eb80f8f79fefc148183f7ba81da15b3aa4d6d2401a3bc7ded plantri55.tar.gz | shasum -a 256 -c -
tar -xzf plantri55.tar.gz
cc -O3 plantri55/plantri.c -o plantri
