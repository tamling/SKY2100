# Contributing to the course script

## Environment mapping (LaTeX → Quarto)

How the original LaTeX environments render in this Quarto book:

| LaTeX (legacy/)          | Quarto (.qmd)                                   | Rendered as                    |
|--------------------------|-------------------------------------------------|--------------------------------|
| `\begin{definition}[T]`  | `::: {#def-slug}` + `## T`                      | numbered Definition, `@def-`   |
| `\begin{example}[T]`     | `::: {#exm-slug}` + `## T`                      | numbered Example, `@exm-`      |
| `\begin{exercise}[T]`    | `::: {#exr-NN-slug}` + `## T`                   | numbered Exercise, `@exr-`     |
| `\begin{realworld}`      | `::: {.callout-note title="Real world: …"}`     | callout box                    |
| `\section*{Self-check}`  | `## Exercises {#sec-NN-exercises}`              | exercise block (quiz section takes the Self-check name) |
| `\paragraph{Sketch answers.}` | moved to `answers/NN-slug.qmd`             | never rendered                 |
| `tikzpicture`            | source in `_tikz/fig-*.tikz`, built to SVG      | `![…](figures/fig-*.svg){#fig-…}` |
| `tabular`/`longtable`    | pipe table + `: Caption {#tbl-…}`               | cross-referenced table         |

Students and colleagues can become contributors — and, with sustained
substantive contributions, credited co-authors — of this script. Smaller
in-place suggestions go through annotations (see the *How to annotate*
appendix); everything larger goes through this flow.

## Contribution types

- **Glossary entry** — a precise definition (2–5 sentences) of a term used
  in the script, with the chapter/section it belongs to and, if the term is
  contested, the competing usages.
- **Worked example** — a step-by-step example illustrating one concept from
  a chapter, complete enough to follow without the contributor present.
- **Exercise scenario** — an applied scenario (like the chapters' practice
  boxes) with a task statement, the chapter sections it exercises, and a
  model answer for the answer key (`answers/`, never shown in the chapter).

Submit as a pull request against the chapter file (plus `answers/` and
`canvas-export/` where an exercise adds self-check material), or — if you
don't work with git — as a document to the course lead, who will turn it
into a PR crediting you.

## Review rubric

Every contribution is reviewed against four criteria; all four must pass:

1. **Technical correctness** — factually and technically accurate;
   verifiable claims are sourced.
2. **Fit** — belongs in the chapter it targets, matches the script's scope
   and level, and doesn't duplicate existing content.
3. **Clarity** — understandable to a fellow student on first reading;
   terminology consistent with the rest of the script.
4. **Sources** — external material is cited, licence-compatible, and not
   copied beyond quotation; examples drawn from real organisations are
   anonymised where appropriate.

The reviewer (course lead) may edit for style and integration. Accepted
contributions are credited in `CHANGELOG.md` (contributor name or chosen
handle + what was merged); recurring contributors are listed on the script's
contributors page.

## Licence and contributor statement

By submitting a contribution you confirm that:

- the contribution is your own work (or clearly attributed and
  licence-compatible), and
- you licence it under the script's licence — **placeholder: CC BY-NC-SA
  4.0, pending the institutional decision on the script's final licence** —
  so it can be published, revised, and redistributed as part of the script.

If the institution settles on a different licence, contributors will be
asked to re-confirm before relicensing anything they authored.

> ⚠️ Note: the repository's `LICENSE` file currently contains **CC0 1.0**
> (the default it was created with). It does not yet reflect the intended
> script licence above — replace it once the institutional decision is made.
