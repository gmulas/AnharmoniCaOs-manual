#!/bin/sh
# Tutorial 3, light version: thermal spectrum of benzonitrile from every state up to 1012.5 cm-1.
# Usage: run.sh CODEDIR BINDIR
#   CODEDIR: the AnharmoniCaOs source tree (with tools/); BINDIR: where the three programs are.
# Runs in the current directory: base/ (phase 1), bn_* (the starting states), jobs/ (six jobs of
# phases 2a and 2b, one after the other, 4 threads each) and spectra/ (0, 100, 200, 300 K).
# Needs Python 3 with numpy. About 5 minutes on a laptop.
set -e
C=${1:?usage: run.sh CODEDIR BINDIR}; B=${2:?usage: run.sh CODEDIR BINDIR}
E=$(cd "$(dirname "$0")" && pwd)
mkdir base
cp "$E"/inp "$E"/quantafile "$E"/freqsfile base/
for f in phi3file phi4file dmu2file dmu3file; do xz -dc "$E/$f.xz" > base/$f; done
# step 0: phase 1 (resonances, effective Hamiltonian), once for all the jobs
(cd base && "$B"/thermal_anharmonicity_fase1 > fase1.log && cp out.oct out.fase1.oct)
# step 1: every harmonic state up to 1012.5 cm-1, energy bins of 25 cm-1
python3 "$C/tools/anh_sample.py" --inp base/inp --freqsfile base/freqsfile \
  --enum 1012.5 --emax 1012.5 --ehistmin -12.5 --ehiststep 25 --per-bin 100000 --blocks 1 \
  --species "$E/species" --prefix bn
# step 2: the jobs (the laptop profile), diagonalisation instead of the spectral method
python3 "$C/tools/anh_jobs.py" --base base --profile laptop --out jobs \
  --states bn_quanta_block000 --Ehistmin -12.5 --Ehiststep 25 --Emax 1012.5 --wnumstep 0.5 \
  --inp-extra "spectral = 0" "eigensolver = 2"
ANHBIN="$B" jobs/submit_all.sh
# step 3: the spectra, with the dipole components along the principal axes a, b, c
python3 "$C/tools/anh_assemble.py" --jobs jobs --out spectra --T 0 100 200 300 \
  --lng bn_dos.dat --axes "$E/principal_axes"
echo "done: see spectra/thermal_T*.dat and spectra/thermal_T*_components.dat"
