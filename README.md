# AnharmoniCaOs user manual

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
