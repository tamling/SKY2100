# Claude Code brief: LaTeX lecture script → Quarto book

> **Status of THIS repo (SKY2100) — read before acting on §3–§9.**
> The conversion here is **already complete**: all 13 chapters + reading list
> are converted, self-checks/answer keys/Canvas exports exist, the site
> deploys via GitHub Actions → GitHub Pages. Do NOT run the §9 start prompt
> here. Deliberate deviations from this brief in this repo:
> - Frozen sources live in `legacy/` (tex + v2.8 PDF); figure sources in
>   `_tikz/` (+ `build.sh` → `chapters/figures/*.svg`), pre-rendered because
>   the preamble styles were reconstructed from the PDF.
> - Numbered blocks use Quarto's native theorem divs (`#def-`, `#exm-`,
>   `#exr-`), no extensions installed.
> - Answers are **not** in the chapters at all (not even collapsed) — per
>   instructor decision; keys live in `answers/` (excluded from render).
> - Hypothesis is enabled via `include-in-header` (not `comments:`), ON by
>   default; Google-Fonts imports are disabled in both themes
>   (`$web-font-path: false`) — a hanging fonts request otherwise blocks the
>   dark-mode stylesheet entirely.
> - HTML only; no PDF format configured yet (open item).
> - Deploy: Pages source "GitHub Actions", not `gh-pages`. StatiCrypt is
>   ON per §7 (secret `SITE_PASSWORD`; search disabled, search.json
>   dropped, plaintext-leak check in the workflow). The repo itself stays
>   public: `answers/` and `legacy/` are world-readable there.
> - `labs/` mirrors the practical-task worksheets (Canvas PDFs stay
>   authoritative; Solutions sections are stripped from the web pages;
>   Exercises 10/12 are linked thematically to two chapters each).
>
> For a fresh conversion (e.g. TK1104), copy this file into that repo and
> follow §3–§9 as written.

Put this file in the repo root as `CLAUDE.md` (Claude Code reads it
automatically) and start with the prompt in §9.

## 1. Goal

Convert the existing LaTeX lecture script into a Quarto book that renders to
HTML (primary, web) and PDF (secondary, same layout as today). The `.qmd`
files become the single source. The old `.tex` files are frozen, never edited
again.

Work is done chapter by chapter. After the first chapter: stop, render,
report, wait for review. No further chapters until explicitly released.

## 2. Repository layout

```
legacy/            frozen original .tex, .sty, .bib copies — read-only
chapters/          NN-slug.qmd, one per chapter
answers/           NN-slug.qmd, answer keys — not rendered
figures/           figure sources (tikz, svg, png)
filters/           Lua filters
_extensions/       installed Quarto extensions
canvas-export/     quiz exports for Canvas
_quarto.yml
CHANGELOG.md
CONTRIBUTING.md
references.bib
```

## 3. Setup (once)

- Copy every original source file into `legacy/` unchanged.
- `quarto create project book .` (or hand-write `_quarto.yml`),
  `project.type: book`.
- Formats: `html` and `pdf`. For PDF, take the existing preamble (packages,
  colours, box definitions, fonts) and load it via `include-in-header`. The
  PDF must look like the current script.
- Reuse `references.bib` as is; citations use `@key`.
- Enable built-ins in `_quarto.yml`:
  - `comments: hypothesis: true` — behind a config toggle; keep it OFF until
    Canvas LTI is confirmed
  - `search: true` (see §7 if StatiCrypt is used)
  - `lightbox: true`
  - `number-sections: true`, `crossref` defaults
- Install extensions (`quarto add`; verify each name still exists before
  installing, report replacements):
  - `quarto-ext/latex-environment` — map custom divs to the existing LaTeX
    environments so PDF boxes keep their look
  - `ute/custom-numbered-blocks` — numbered Definition / Example / Exercise
    blocks with cross-references
  - `pandoc-ext/diagram` — render TikZ / Mermaid / Graphviz from source
    inside `.qmd`
  - `quarto-ext/include-code-files` — include lab config files (Terraform,
    IAM policies, nginx, …) from disk
  - `jmgirard/embedpdf` — only if PDF attachments are needed
  - `r-wasm/quarto-live` — only for Python courses (in-browser Python
    exercises); skip for GRC / cloud security

## 4. Per-chapter conversion rules

1. `pandoc legacy/chapter.tex -o chapters/NN-slug.qmd --wrap=none`, then
   clean up by hand.
2. Wording is preserved exactly. Do not rewrite, shorten, modernise or
   "improve" prose. Fix only conversion damage.
3. Custom environments → blocks:
   - `definition` → `::: {.definition}` (custom-numbered-blocks), PDF via
     latex-environment to the original env
   - `example` → `::: {.example}`
   - `exercise` → `::: {.exercise}`
   - `warning` / `note` / `tip` without numbering → Quarto callouts
   - anything else: write a Lua filter in `filters/` so HTML and PDF render
     it consistently; document the mapping in a table at the top of
     `CONTRIBUTING.md`
4. TikZ / pgfplots: keep the source in the `.qmd` inside a diagram block
   (pandoc-ext/diagram). Only pre-render to SVG if the diagram uses packages
   the filter cannot handle; then store source and SVG in `figures/` and
   note it.
5. `\label` / `\ref` → `@sec-`, `@fig-`, `@tbl-`, `@def-` etc. Every figure
   and table gets a label and caption.
6. Drop layout-only LaTeX: minipage, `\newpage`, `\vspace`, manual column
   tricks.
7. Tables: convert to pipe tables where simple; complex tables to grid
   tables; note any table that lost merged cells.
8. Code listings: fenced blocks with language tag; lab config files via
   include-code-files rather than pasted.

## 5. Chapter skeleton to add

Every chapter gets, in this order:

```
# Title {#sec-slug}

::: {.callout-note title="Learning outcomes"}
<copy from source if present, else PLACEHOLDER>
:::

<converted body>

## In practice
<if source has a practice/industry example, move it here; else PLACEHOLDER>

## Self-check {.unnumbered}
<see §6>

## Related lab {.unnumbered}
PLACEHOLDER — link to lab task / CloudSec OS scenario

## Glossary terms introduced {.unnumbered}
<list terms defined in this chapter>
```

## 6. Self-check questions

- Draft 5–8 per chapter: multiple choice (4 options, one correct), short
  answer, and one applied/scenario question tied to the "In practice" box.
- Each question carries the section it tests (`@sec-…`) and a tag `basic` or
  `applied`.
- In the chapter: question visible, answer inside a collapsed callout
  (`collapse="true"`), so readers can self-test.
- Full answer key with rationale in `answers/NN-slug.qmd`, excluded from
  render.
- Export the same questions to `canvas-export/NN-slug.csv` (or QTI if a
  converter is available) for a Canvas quiz.
- A question must be answerable from the chapter text alone; flag any that
  is not.
- These are drafts for instructor review, not final. Say so in the report.

## 7. Access protection (StatiCrypt) — only if enabled

Add a step after `quarto render` in the GitHub Action:

```yaml
- name: Encrypt site
  run: |
    npx staticrypt "_book/**/*.html" -r -d _site \
      --password "${{ secrets.SITE_PASSWORD }}" \
      --remember 30 --short
    rm -f _site/search.json
```

Rules when StatiCrypt is on:

- Deploy `_site`, never `_book`.
- Delete `search.json` (contains full text) or set `search: false`.
- Remove the PDF download link from HTML; PDF is distributed via Canvas only.
- Verify that no unencrypted text reaches the `gh-pages` branch (grep the
  branch for a distinctive sentence from the script).
- Test Hypothesis on an encrypted page; if annotations fail, note it —
  annotation then stays Canvas-LTI only.

## 8. Deployment and housekeeping

- GitHub Action: on push to `main` → `quarto render` → (StatiCrypt) →
  publish to `gh-pages`.
- `robots.txt` with `Disallow: /` and `<meta name="robots"
  content="noindex">` while the site is unofficial.
- `CHANGELOG.md`: one section per semester version, entries per change,
  contributor credit by name.
- `CONTRIBUTING.md`: contribution types (glossary entry, worked example,
  exercise scenario), review rubric (technical correctness, fit with
  chapter, clarity, sources), contributor licence statement (placeholder
  CC BY-NC-SA, pending institutional decision), environment-mapping table
  from §4.
- Appendix page "How to annotate": what counts as substantive (question,
  correction, practice example), per-chapter quota placeholder, how
  annotations become script changes.

## 9. Start prompt

```
Read CLAUDE.md and follow it. Do the setup in §3, then convert ONLY the
first chapter according to §4–§6. Render HTML and PDF. Then stop and give me:
1. a list of every lossy or uncertain conversion decision,
2. the environment mapping you used,
3. which extensions installed cleanly and which needed a replacement,
4. a diff summary.
Do not touch other chapters until I say "next".
```

## 10. Review checklist (for me, per chapter)

- Wording unchanged against `legacy/`
- Boxes look right in HTML and PDF
- Every figure renders in both formats, has caption and label
- Cross-references resolve
- Self-check questions correct, distractors plausible
- No PLACEHOLDER left that should have been filled from source
