# Canvas export

One machine-readable questions file per converted chapter,
`NN-name.questions.yml` (see `00-template.questions.yml`), holding exactly
the questions from that chapter's Self-check section plus the answers from
`answers/NN-name.qmd`. From it, `make_canvas_quiz.py` generates:

- `NN-name.qti.zip` — a QTI 1.2 package Canvas imports as a **Classic
  Quiz** (Course → Settings → Import Course Content → *QTI .zip file*).
  Multiple choice and short-answer questions self-mark; the applied
  scenario becomes an essay question for manual marking.
- `NN-name.csv` — the same questions flat in a spreadsheet, for review or
  for building a New Quizzes item bank by hand.

```sh
python3 make_canvas_quiz.py 03-name.questions.yml   # one chapter
python3 make_canvas_quiz.py                          # all *.questions.yml
```

Requires Python 3.8+ and PyYAML (`pip install pyyaml`).

Generated `*.qti.zip` / `*.csv` files are build artifacts — regenerate
rather than edit them.

After importing, paste the quiz URL into the chapter's Self-check callout
(`CANVAS-QUIZ-URL-PLACEHOLDER` in the template).

Questions with `flag:` set (needs knowledge not in the script) are **skipped
with a warning** at export time — resolve the flag first.
