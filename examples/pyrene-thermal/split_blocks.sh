#!/bin/sh
# Tutorial 3, step 2: split the blocks of step 1 into files of N states (default 4), each with
# a copy of the .block file of its block, for anh_jobs.py --blocks (one job per file).
# Usage: split_blocks.sh [N]   (in the directory of step 1; writes jq/)
set -e
N=${1:-4}
mkdir -p jq
for f in s_quanta_block00?; do
  split -l "$N" -d -a 2 "$f" "jq/${f}_"
  for p in jq/"${f}"_*; do
    case $p in *.block) ;; *) cp "$f.block" "$p.block" ;; esac
  done
done
echo "done: $(ls jq | grep -vc '\.block$') files in jq/"
