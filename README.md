# AnharmoniCaOs user manual

The user manual of [AnharmoniCaOs](https://sourceforge.net/projects/anharmonica/),
a code for the anharmonic infrared spectra of large molecules: how to
install it, its input files and options, its outputs, and tutorials that
can be reproduced. The code is on SourceForge (public release) and on
GitHub (development); the input parser is
[liboct-parser](https://github.com/gmulas/oct-parser-fork), from Octopus.

Authors: Giacomo Mulas (INAF – Osservatorio Astronomico di Cagliari) and
Cyril Falvo (Université Paris-Saclay), with contributions by Claude (AI
model by Anthropic) since 2026.

The examples in `examples/` (force fields, dipole derivatives, inputs) are
the data of the tutorials and are distributed under the same licence as
the manual.

## Building

There is one LaTeX source and two outputs:

- **PDF**: `make pdf`, or compile `manual.tex` on Overleaf.
- **HTML**: `make html`, which uses [LaTeXML](https://math.nist.gov/~BMiller/LaTeXML/).
- **Docker image** (Debian slim + Apache) serving the HTML, with the PDF next to it:
  ```
  docker build -f docker/Dockerfile -t anharmonicaos-manual .
  docker run -p 8080:80 anharmonicaos-manual
  ```

Rules for the sources:

- Use only the packages loaded in `macros.tex` and standard LaTeX, so that
  LaTeXML converts everything. No TikZ: use included PDF/PNG figures, and
  provide a PNG version for HTML (LaTeXML picks it up automatically).
- One chapter per file in `chapters/`.
- Tutorials must be reproducible: their inputs live in `examples/<name>/`,
  with a `run.sh`, and every number quoted in the text comes from those
  runs.
- Point to the theory notes with `\notes{§...}`, and to the literature
  with `\cite`.

## License

This manual is distributed under the GNU General Public License, version 3
(SPDX `GPL-3.0-only`), the same license as AnharmoniCaOs; see
[`COPYING`](COPYING).
