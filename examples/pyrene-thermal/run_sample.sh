#!/bin/sh
# Tutorial 3, step 1: starting states of pyrene up to 2500 cm-1: every state up to 2550 cm-1
# enumerated, four blocks of eight draws per bin in two strata of the harmonic emission rate.
# Usage: run_sample.sh CODEDIR   (CODEDIR: the AnharmoniCaOs source tree, with tools/)
# Needs Python 3 with numpy. Runs in the current directory, in about 20 seconds; writes a
# 150 MB s_states.dat.
set -e
C=${1:?usage: run_sample.sh CODEDIR}
E=$(dirname "$0")/../pyrene
python3 "$C/tools/anh_sample.py" --inp "$E/inp" --freqsfile "$E/freqsfile" \
  --enum 2550 --emax 2500 --ehistmin -50 --ehiststep 100 \
  --per-bin 8 --blocks 4 --draws --hstrata 2 --seed 20261126 --prefix s
echo "done: see s_dos.dat, s_hstrata.dat and s_quanta_block000 ... s_quanta_block004"
