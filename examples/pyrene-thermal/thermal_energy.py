#!/usr/bin/env python3
"""How high must the starting states go for a spectrum at temperature T?

Exact harmonic counts of the vibrational states of pyrene (Beyer-Swinehart,
on a 10 cm-1 grain) give the thermal distribution of the vibrational energy,
P(E) proportional to g(E) exp(-E/kT). The script prints, for a few
temperatures, kT, the mean energy (checked against the exact harmonic
value sum_i w_i/(exp(w_i/kT)-1)), the energies below which 99 % and 99.9 % of
the population lie, and these in units of kT; with --plot it draws the
distributions (thermal_energy.png).

usage: thermal_energy.py [FREQSFILE] [--plot]   (needs numpy; matplotlib for --plot)
"""
import math
import os
import sys

import numpy as np

KB = 0.6950348  # cm-1/K
here = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
freqs = args[0] if args else os.path.join(here, "..", "pyrene", "freqsfile")
w = np.array([float(l.split()[0]) for l in open(freqs) if l.strip()])

grain, emax = 10.0, 90000.0
nb = int(emax/grain) + 1
g = np.zeros(nb)
g[0] = 1.0
for x in w:  # Beyer-Swinehart
    m = int(round(x/grain))
    for e in range(m, nb):
        g[e] += g[e-m]
E = np.arange(nb)*grain
# per 100 cm-1, for the plot and the peak
step = 100.0
k = int(step/grain)
E100 = E[:len(E)//k*k].reshape(-1, k).mean(axis=1)
g100 = g[:len(g)//k*k].reshape(-1, k).sum(axis=1)

Ts = (300, 500, 1000)
print("%6s %6s %8s %8s %8s %8s %6s %6s" % ("T (K)", "kT", "mean", "exact", "99%", "99.9%", "/kT", "5kT"))
dists = {}
for T in (100,) + Ts:
    kT = KB*T
    lw = np.log(np.maximum(g, 1e-300)) - E/kT
    p = np.exp(lw - lw.max())
    p /= p.sum()
    c = np.cumsum(p)
    mean = (p*E).sum()
    exact = sum(x/math.expm1(x/kT) for x in w)
    e99, e999 = E[np.searchsorted(c, 0.99)], E[np.searchsorted(c, 0.999)]
    print("%6d %6.0f %8.0f %8.0f %8.0f %8.0f %6.1f %6.0f"
          % (T, kT, mean, exact, e99, e999, e999/kT, 5*kT))
    lw100 = np.log(np.maximum(g100, 1e-300)) - E100/kT
    p100 = np.exp(lw100 - lw100.max())
    dists[T] = (p100/p100.sum()/step, kT, e999)

if "--plot" in sys.argv:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted = "#0b0b0b", "#52514e"
    cols = {300: "#2a78d6", 500: "#eb6834", 1000: "#1baf7a"}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=150)
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(colors=muted, labelsize=9)
        ax.grid(color="#e4e3df", linewidth=0.6)
        ax.set_axisbelow(True)
    # left: how fast ln g grows, against 1/kT
    ok = g100 > 0
    lg = np.log(np.maximum(g100, 1e-300))
    d = 5  # bins of 100 cm-1 on each side
    slope = (lg[2*d:] - lg[:-2*d])/(2*d*step)*1000   # per 10^3 cm-1
    Es = E100[d:-d]/1000
    a1.plot(Es[Es > 0.5], slope[Es > 0.5], color=ink, linewidth=2)
    a1.text(60, slope[np.searchsorted(Es, 60)] + 0.15, "d ln g/dE", color=ink, fontsize=9)
    for T in Ts:
        kT = KB*T
        y = 1000/kT
        a1.axhline(y, color=cols[T], linewidth=1.5, linestyle="--")
        a1.text(79, y + 0.15, "1/kT, %d K" % T, color=ink, fontsize=8, ha="right", va="bottom")
    a1.set_xlim(0, 80)
    a1.set_ylim(0, 6)
    a1.set_xlabel("vibrational energy E (10$^3$ cm$^{-1}$)", color=muted, fontsize=9)
    a1.set_ylabel("per 10$^3$ cm$^{-1}$", color=muted, fontsize=9)
    a1.set_title("P(E) peaks where ln g grows as fast as E/kT", color=ink, fontsize=10, loc="left")
    # right: the thermal distributions
    for T in Ts:
        p, kT, e999 = dists[T]
        a2.plot(E100/1000, p*1000, color=cols[T], linewidth=2)
        i = np.argmax(p)
        a2.text(E100[i]/1000 + 0.8, p[i]*1000, "%d K" % T, color=ink, fontsize=9, ha="left",
                va="bottom")
        a2.axvline(5*kT/1000, color=cols[T], linewidth=1, linestyle=":")
        a2.axvline(e999/1000, color=cols[T], linewidth=1, linestyle="--")
    a2.set_xlim(0, 45)
    a2.set_ylim(0, 0.52)
    a2.set_xlabel("vibrational energy E (10$^3$ cm$^{-1}$)", color=muted, fontsize=9)
    a2.set_ylabel("P(E) (per 10$^3$ cm$^{-1}$)", color=muted, fontsize=9)
    a2.set_title("P(E): dotted line 5 kT, dashed line 99.9 %", color=ink, fontsize=10, loc="left")
    fig.tight_layout()
    fig.savefig("thermal_energy.png")
    print("wrote thermal_energy.png")
