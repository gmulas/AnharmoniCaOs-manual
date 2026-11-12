#!/bin/sh
# Tutorial 3, step 1: starting states of pyrene up to 2500 cm-1.
# Usage: run_sample.sh CODEDIR   (CODEDIR: the AnharmoniCaOs source tree, with tools/)
# Needs Python 3 with numpy. Runs in the current directory, in a few seconds.
set -e
C=${1:?usage: run_sample.sh CODEDIR}
E=$(dirname "$0")/../pyrene
python3 "$C/tools/anh_sample.py" --inp "$E/inp" --freqsfile "$E/freqsfile" \
  --enum 1000 --emax 2500 --ehistmin -50 --ehiststep 100 \
  --walkers 2 --per-bin 2 --blocks 1 --prefix s
echo "done: see s_dos.dat, s_states.dat and s_quanta_block000"
