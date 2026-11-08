#!/bin/sh
# Tutorial 1: absorption spectrum of pyrene from the ground state.
# Usage: run.sh BINDIR [NPROC]   (BINDIR: where the three programs are)
set -e
B=${1:?usage: run.sh BINDIR [NPROC]}; NP=${2:-4}
for f in phi3file phi4file dmu2file; do [ -f $f ] || xz -dk $f.xz; done
$B/thermal_anharmonicity_fase1 > fase1.log
$B/thermal_anharmonicity_fase2a > fase2a.log
mpirun -np $NP $B/thermal_anharmonicity_fase2b > fase2b.log
echo "done: see resonanceslist, dunhamparams, bandlist and hist_abs_*"
