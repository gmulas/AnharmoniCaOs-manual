# CLAUDE.md — instructions for Claude working on the AnharmoniCaOs user manual

The code is in `gmulas/AnharmoniCaOs` (its `CLAUDE.md` has the general
rules and the technical background). The theory notes are in
`gmulas/AnharmoniCaOs-notes`.

- Never commit or push to `main`. Overleaf is synchronised with `main`.
  Work on a branch (`docs/...`) and open a pull request, one topic per PR.
- Talk to the maintainer (Giacomo Mulas) in Italian. The manual, commit
  messages and comments are in English.
- One source, two outputs: the PDF (latexmk, Overleaf) and the HTML
  (LaTeXML, `make html`, `docker/Dockerfile`). Use only standard LaTeX and
  the packages in `macros.tex`. Check that the PDF builds (`make pdf`)
  before every commit.
- The manual is for users, written in the style of a program manual: what
  to do, with which files and options, and what to expect. Point to the
  theory notes with `\notes{...}` and to the literature with `\cite`
  instead of repeating derivations.
- Tutorials must be reproducible:
  - their inputs are in `examples/<name>/`, compressed with xz when large,
    with a `run.sh`;
  - every number quoted comes from runs of those inputs with a stated
    version of the code.
- When an option or output of the code changes, update the manual in a PR
  that names the code PR.
- The example data belong to the maintainer and are public. The theory
  notes are private until published: point to them with `\notes{...}`, do
  not copy their derivations into the manual. Source code goes in the code
  repository, not here.
