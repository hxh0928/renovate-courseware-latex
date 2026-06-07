# Courseware Renovation Rules

## Content Mapping

Create a private mapping from old material to new frames:

| Source | Old title/content | New section/frame | Action |
|---|---|---|---|
| slide/page 1 | ... | section/frame | keep / split / merge / omit |

Use the mapping to ensure no important teaching unit silently disappears.

## What To Preserve

- Definitions, theorem statements, assumptions, formulas, derivations.
- Worked examples, data tables, exercise prompts, answer hints.
- Teacher-specific warnings, common mistakes, and interpretation notes.
- Diagrams that carry real meaning.
- Original software/system output language and wording, including code output headings, prompts, warnings, result tables, variable names, function names, and package messages.

## Metadata

- Infer the course name and instructor/teacher name from the source or conversation when possible. Tell the user they can provide or override either field. Use neutral placeholders only when the values cannot be inferred.
- Put the instructor/teacher name in `\author{...}`.
- Put the course name in the title-page metadata where it best fits the deck, usually `\institute{...}` for a course label or `\subtitle{...}` when the subtitle is intended to carry the course name.

## What To Improve

- Courseware language: keep the source courseware's primary language by default; change the explanatory slide language only when the user explicitly specifies a target language.
- Long bullet lists: split into concept + example + summary.
- Dense paragraphs: convert to concise text, equation, table, columns, or flow diagram. Use `block` only when a formal definition, theorem, conclusion, or warning needs visual separation.
- Screenshot charts: recreate with PGFPlots if data are readable.
- Low-resolution diagrams: redraw with TikZ if geometry is simple.
- Mixed notation: standardize symbols and define them once.
- Old visual clutter: remove decorations, clip art, and redundant logos unless required.
- Process or casual teaching labels: remove visible wording such as “翻新课件”, “旧课件”, “课堂提示”, “教学提醒”, “课堂讨论”, and “这里要注意”. Use formal labels such as “说明”, “注意”, “结论”, or omit the label.

## Frame Types

### Concept frame
Use for definitions, properties, assumptions, and interpretation.

Recommended elements:
- One concise title.
- A short lead sentence with `\key{}` when useful.
- 3-5 bullets maximum.
- Optional `\smallnote{}` for caveats.

Use `block`/`alertblock` sparingly. Most concept frames should remain unboxed; too many boxes make the deck visually heavy and reduce contrast when a truly important definition appears.

### Derivation frame
Use for formulas that need sequential explanation.

Recommended elements:
- Keep derivation vertical and sparse.
- Highlight the key transformation with `\key{}`.
- Split across frames if there are more than 4 displayed equations.

### Example frame
Use for worked examples and class exercises.

Recommended elements:
- Put known data on the left and solution logic on the right.
- Use `columns` for side-by-side layout.
- Keep numerical calculation steps readable.

### Table frame
Use `booktabs` and `tabularx`; avoid full grid borders.

Default two-column explanatory table pattern:

```latex
\begin{tabularx}{\linewidth}{>{\bfseries\color{MainBlue}}p{2.7cm}Y}
  \toprule
  项目 & 说明 \\
  \midrule
  ... & ... \\
  \bottomrule
\end{tabularx}
```

The template must define:

```latex
\newcolumntype{Y}{>{\vspace{0.35ex}\raggedright\arraybackslash}X}
```

Use `\linewidth` for Beamer tables, especially inside frames or columns. Adjust the first-column width only when needed for alignment.

For wide tables:
- abbreviate headers,
- split into two frames,
- or show only teaching-relevant rows/columns.

### Diagram frame
Prefer TikZ for concept maps, timelines, process flows, sampling diagrams,
probability trees, and hypothesis-testing decision flows.

Keep arrows meaningful. Do not use decorative arrows.

### Code frame
Use `[fragile]` and `lstlisting[style=rcode]`.

If old code is too long, show the core snippet and move full code to notes or an appendix frame.

Software output shown in code frames or reconstructed result tables must remain in the software's original language. Do not translate output labels such as `Call`, `Residuals`, `Coefficients`, `Estimate`, `Std. Error`, or `Pr(>|t|)`.

## Compilation Guidance

Preferred commands:

```bash
latexmk -xelatex -interaction=nonstopmode main.tex
```

Fallback:

```bash
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

If compilation fails:

1. Read the first real LaTeX error, not only the final fatal line.
2. Check unescaped special characters from extracted text.
3. Check missing figure paths and file names with spaces.
4. Check `fragile` frames for listings.
5. Check unmatched braces in formulas copied from old slides.

## Final Review

Inspect the generated PDF for:

- Instructor/teacher metadata matches the user-provided or inferred name, or uses a neutral placeholder when unavailable.
- Course name metadata matches the user-provided or inferred course name, or uses a neutral placeholder when unavailable.
- Chinese glyph rendering.
- Formula baseline and symbol consistency.
- Table overflow.
- Figure legibility.
- Overcrowded frames.
- Section divider placement.
- Broken hyperlinks or missing references.
