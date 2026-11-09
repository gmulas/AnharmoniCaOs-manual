#!/bin/sh
# Tutorial 1: absorption spectrum of pyrene from the ground state.
# Usage: run.sh BINDIR [NPROC]   (BINDIR: where the three programs are)
set -e
B=${1:?usage: run.sh BINDIR [NPROC]}; NP=${2:-4}
for f in phi3file phi4file dmu2file; do [ -f $f ] || xz -dk $f.xz; done
# each program overwrites out.oct (the options it used): keep one copy per phase
$B/thermal_anharmonicity_fase1 > fase1.log; cp out.oct out.fase1.oct
$B/thermal_anharmonicity_fase2a > fase2a.log; cp out.oct out.fase2a.oct
mpirun -np $NP $B/thermal_anharmonicity_fase2b > fase2b.log; cp out.oct out.fase2b.oct
echo "done: see resonanceslist, dunhamparams, bandlist and hist_abs_*"
