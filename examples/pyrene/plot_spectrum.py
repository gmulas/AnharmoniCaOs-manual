#!/usr/bin/env python3
"""Tutorial 1: absorption spectrum of pyrene from the ground state.

Reads the histograms hist_abs_0, _1, _2 (x, y, z components of |mu_fi|^2 in
atomic units, one column per 0.01 cm-1 bin) of a finished run, adds the three
components, converts them to integrated intensities in km/mol
(I = 16.194 * nu * |mu|^2), merges the bins closer than 0.5 cm-1 into lines,
and prints the strongest lines. With matplotlib, it also draws the line
spectrum against the harmonic one from freqsfile (pyrene-spectrum.png).

Usage: plot_spectrum.py [RUNDIR] [NLINES]     (default: current directory, 15)
"""
import os, sys
import numpy as np

KMMOL = 16.194   # |mu|^2 (a.u.) * wavenumber (cm-1) -> km/mol


def read_lines(d):
    acc = {}
    for c in (0, 1, 2):
        for line in open(os.path.join(d, 'hist_abs_%d' % c)):
            t = line.split()
            if line.startswith('#') or len(t) != 2:
                continue
            v = float(t[1])
            if v != 0:
                k = float(t[0])
                acc[k] = acc.get(k, 0.) + v
    nu = np.array(sorted(acc))
    I = KMMOL * nu * np.array([acc[k] for k in nu])
    # merge bins closer than 0.5 cm-1 (intensity-weighted position)
    lines, cur = [], [nu[0], I[0], nu[0] * I[0]]
    for x, y in zip(nu[1:], I[1:]):
        if x - cur[0] < 0.5:
            cur[1] += y; cur[2] += x * y
        else:
            lines.append((cur[2] / cur[1], cur[1])); cur = [x, y, x * y]
    lines.append((cur[2] / cur[1], cur[1]))
    return np.array(lines)


def harmonic(d):
    F = np.loadtxt(os.path.join(d, 'freqsfile'), usecols=(0, 1, 2, 3))
    return F[:, 0], KMMOL * F[:, 0] * (F[:, 1:] ** 2).sum(1) / 2


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    L = read_lines(d)
    print('%d lines, total %.1f km/mol' % (len(L), L[:, 1].sum()))
    print('strongest lines:\n  wavenumber (cm-1)   intensity (km/mol)')
    for nu, I in sorted(L, key=lambda x: -x[1])[:n]:
        print('  %16.2f %20.2f' % (nu, I))
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return
    hw, hI = harmonic(d)
    fig, ax = plt.subplots(2, 1, figsize=(9, 6))
    for a, (lo, hi) in zip(ax, ((0, 1700), (2950, 3200))):
        s = (L[:, 0] >= lo) & (L[:, 0] <= hi)
        a.vlines(L[s, 0], 0, L[s, 1], color='#1f4e9c', lw=1, label='anharmonic (AnharmoniCaOs)')
        s = (hw >= lo) & (hw <= hi)
        a.vlines(hw[s], 0, -hI[s], color='#b0413e', lw=1, label='harmonic (freqsfile)')
        a.axhline(0, color='k', lw=0.5)
        a.set_xlim(lo, hi)
        a.set_ylabel('intensity (km/mol)')
    ax[0].legend(fontsize=8, loc='upper left')
    ax[1].set_xlabel('wavenumber (cm$^{-1}$)')
    fig.tight_layout()
    fig.savefig('pyrene-spectrum.png', dpi=150)
    print('written pyrene-spectrum.png')


if __name__ == '__main__':
    main()
