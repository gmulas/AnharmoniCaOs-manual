# One source, two outputs.
#   make pdf    -> manual.pdf (pdflatex via latexmk; Overleaf does the same)
#   make html   -> html/ (LaTeXML: latexmlc, MathML + MathJax fallback)
#   make docker -> image serving html/ (see docker/Dockerfile)
MAIN = manual
SRC  = $(MAIN).tex macros.tex $(MAIN).bib $(wildcard chapters/*.tex)

pdf: $(MAIN).pdf
$(MAIN).pdf: $(SRC)
	latexmk -pdf -interaction=nonstopmode $(MAIN).tex

html: html/index.html
html/index.html: $(SRC)
	latexmlc --dest=html/index.html --split --splitat=chapter \
	  --navigationtoc=context --bibtex --css=LaTeXML-navbar-left.css \
	  --javascript='https://cdn.jsdelivr.net/npm/mathjax@3/es5/mml-chtml.js' \
	  $(MAIN).tex

docker:
	docker build -f docker/Dockerfile -t anharmonicaos-manual .

clean:
	latexmk -C $(MAIN).tex; rm -rf html
.PHONY: pdf html docker clean
