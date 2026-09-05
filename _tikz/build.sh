#!/bin/sh
# Rebuild the chapter figures from their TikZ sources.
# Requires: pdflatex with TikZ (texlive-pictures, standalone class from
# texlive-latex-extra) and pdftocairo (poppler-utils).
# Output goes to chapters/figures/<name>.svg.
set -e
cd "$(dirname "$0")"
for f in fig-*.tikz; do
  n="${f%.tikz}"
  { cat preamble.tex; cat "$f"; printf '\\end{document}\n'; } > "/tmp/$n.tex"
  pdflatex -interaction=batchmode -halt-on-error -output-directory /tmp "/tmp/$n.tex" >/dev/null
  pdftocairo -svg "/tmp/$n.pdf" "../chapters/figures/$n.svg"
  echo "built $n.svg"
done
