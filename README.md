# SKY2100 — course script (Quarto)

Quarto book project for the SKY2100 course script.

```
_quarto.yml               project config; annotations flag; answers/ excluded
_quarto-annotations.yml   render profile that switches Hypothesis ON
includes/hypothesis.html  the Hypothesis embed snippet (header include)
index.qmd                 book landing page
chapters/                 converted chapters land here (NN-name.qmd)
_templates/               Self-check section template for chapters
_tikz/                    TikZ sources for the figures + build.sh → chapters/figures/*.svg
answers/                  per-chapter answer keys — source-only, never rendered
canvas-export/            per-chapter questions.yml → Canvas QTI zip + CSV
appendix/how-to-annotate.qmd  annotation rules, quota, credit flow
CONTRIBUTING.md           co-authorship flow, review rubric, licence statement
CHANGELOG.md              script changes + credited contributions
```

Render: `quarto render` (annotations off) ·
`quarto render --profile annotations` (Hypothesis on — only once the Canvas
LTI setup is confirmed).

## Per-chapter checklist

When a converted chapter `chapters/NN-name.qmd` lands:

1. Add it to `book.chapters` in `_quarto.yml`.
2. Append a **Self-check** section from `_templates/chapter-self-check.qmd`:
   5–8 questions (MCQ ×4-options, short answer, one applied/scenario tied to
   the chapter's practice box), each marked `(tests @sec-… · basic|applied)`.
   Flag any question that needs knowledge not in the chapter text.
3. Write the answer key `answers/NN-name.qmd` (never linked, never rendered).
4. Write `canvas-export/NN-name.questions.yml` and run
   `python3 canvas-export/make_canvas_quiz.py` to get the Canvas quiz
   (QTI zip) + review CSV; import in Canvas and paste the quiz URL into the
   chapter's Self-check callout.
