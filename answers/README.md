# Answer keys (source-only)

One file per converted chapter, named exactly like the chapter file:
`answers/NN-name.qmd` for `chapters/NN-name.qmd`.

This directory is **excluded from every render** by the `"!answers/"`
pattern under `project.render` in `_quarto.yml`, so answers never appear on
the published site. They reach students only as a self-marking Canvas quiz -
see `canvas-export/README.md`.

Each key mirrors the chapter's Self-check numbering (Q1…Qn) and gives, per
question: the correct option (multiple choice), the accepted answers (short
answer), or a model answer with grading notes (applied scenario). Use
`answers/00-template.qmd` as the starting point.
