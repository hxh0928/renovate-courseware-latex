---
name: renovate-courseware-latex
description: Convert and renovate old courseware into a new LaTeX ctexbeamer slide deck, including Chinese courseware that must compile with Chinese text. Use when the user asks to 翻新课件, renovate old slides, convert PPT/PPTX/PDF/DOCX/images/Markdown/HTML course materials into LaTeX Beamer, rebuild lecture notes as a modern ctexbeamer deck, or preserve an old lesson's knowledge structure while producing a compilable Chinese/English .tex/.pdf slide deck using the bundled template.
---

# Renovate Courseware To LaTeX

## Goal

Transform old courseware of any reasonable format into a polished, compilable `ctexbeamer` deck. Preserve the teaching intent and knowledge sequence, but rewrite the slides as a cleaner LaTeX version using the required template in `assets/ctexbeamer-template.tex`. Chinese decks must compile and render Chinese glyphs correctly.

## Inputs

Require at least one source courseware artifact from the user. Accept PPT/PPTX, PDF, DOCX, images, Markdown, HTML, LaTeX, plain text, spreadsheets used as teaching material, or a folder of mixed assets.

If the user gives no source file, ask for it. Infer course name, instructor/teacher name, title, school, audience, and chapter range from the source or conversation when possible. Tell the user they can provide or override the course name and instructor/teacher name. If a field cannot be inferred, use neutral placeholders such as `课程名称` and `授课教师` rather than blocking.

## Output Contract

Produce a folder containing:

- `main.tex`: the renovated Beamer deck.
- `figures/`: extracted or recreated figures used by the deck, when needed.
- `main.pdf`: compiled PDF preview, when a LaTeX engine is available.
- optional `build.log`: only if compilation fails or warnings matter.

Final response should link to `main.tex` and, when compiled, `main.pdf`. Mention any source content that could not be recovered.

## Mandatory Workflow

1. **Inspect the source**
   - Identify course title, chapter, sections, slide count, formulas, diagrams, tables, code, examples, and exercises.
   - Identify the primary language of the source courseware and any user-specified target language.
   - Check whether the course name and instructor/teacher name can be inferred from the source or conversation. If inferred values are uncertain, use neutral placeholders and mention that the user can provide exact values.
   - Extract all readable text and list images/diagrams that need preservation or recreation.
   - For PPTX/PDF, render or preview pages/slides when possible; text extraction alone is not enough for layout-sensitive material.

2. **Build a teaching outline**
   - Convert old slide order into a concise lecture structure: sections, subsections, concept slides, example slides, exercise slides, summary slides.
   - Remove duplicate, outdated, or purely decorative content.
   - Preserve definitions, assumptions, formulas, theorem statements, examples, dataset descriptions, and exercise prompts.
   - Do not invent domain facts. If a formula or table is unreadable, mark it for review in the deck with a short `\smallnote{...}`.

3. **Create the LaTeX deck**
   - Start from `assets/ctexbeamer-template.tex`; do not use another preamble unless the user explicitly asks.
   - Keep the exact document class and style system unless the source requires a package addition.
   - Set course metadata from user-provided or inferred values: use the course name in the title page metadata, usually `\institute{...}` or `\subtitle{...}` depending on the deck structure, and use `\author{...}` for the instructor/teacher name. If either value is unavailable, use a neutral placeholder and tell the user they can replace it.
   - Use the source courseware's primary language by default. If the user specifies a target language, use that language for explanatory slide text.
   - Preserve software, code, console, statistical package, and system outputs exactly as shown by the software. Do not translate, paraphrase, localize, or "clean up" output labels, variable names, function names, warnings, prompts, or result tables.
   - Use `\section{}` and `\subsection{}` to create a coherent lecture flow.
   - Use Beamer frames with short, claim-like titles.
   - Use `block`, `alertblock`, and other boxed environments sparingly. Default to clean text, equations, tables, columns, and diagrams; reserve boxes for formal definitions, theorems, key conclusions, or warnings that need strong visual separation.
   - Prefer native LaTeX/TikZ/PGFPlots/table code over raster screenshots for diagrams, charts, and tables when reconstruction is practical.
   - Preserve original source images only when they are inspectable visual subjects or too costly to recreate accurately.

4. **Renovate rather than transcribe**
   - Split overcrowded old slides into multiple clean frames.
   - Combine slides that only contain fragments of one concept.
   - Convert paragraphs into definitions, bullets, equations, tables, or diagrams according to teaching function.
   - Avoid wrapping ordinary bullet lists in `block`; it makes renovated decks look heavy and repetitive.
   - Add short transition or summary frames only when they clarify the lesson.
   - Keep mathematical notation consistent across the deck.

5. **Compile and verify**
   - Compile with `xelatex` or `latexmk -xelatex` when available. Never use `pdflatex` for Chinese courseware.
   - Fix LaTeX errors, overfull/underfull boxes that affect readability, missing images, broken references, and unreadable tables.
   - Render/inspect the PDF visually when possible. Check Chinese text, formulas, tables, TikZ diagrams, PGFPlots charts, code blocks, and page breaks.
   - If no LaTeX engine is available, still produce `main.tex` and state that compilation was not run.

## Chinese Compilation Requirements

- The deck must remain based on `ctexbeamer` and should be compiled with XeLaTeX.
- Preserve Chinese text as UTF-8. Do not convert Chinese punctuation or section titles to escaped glyph codes.
- If Chinese text fails to render, first switch the compile command to `latexmk -xelatex`; then check the available CJK fonts before editing the preamble.
- When a fontset is needed, prefer portable `ctex` options or installed system fonts:
  - TeX Live default/Fandol: keep `\documentclass[aspectratio=169,11pt]{ctexbeamer}`.
  - macOS: use `fontset=mac` only if the local TeX installation supports it.
  - Windows: use `fontset=windows` only if compiling on Windows.
  - Custom fonts: add `\setCJKmainfont{...}` only after confirming the font exists.
- Font warnings such as missing `Script "CJK"` are not fatal if Chinese glyphs render correctly. Missing glyph boxes, blank Chinese text, or tofu symbols must be fixed before delivery.
- For older TeX Live installations, `\pgfplotsset{compat=1.18}` may fail. Use the highest supported compatibility value, such as `compat=1.16`, and mention the environment-specific change in the final response.

## Conversion Standards

Read `references/renovation-rules.md` before working on a substantial deck or when the source is messy.

Use these frame patterns. Prefer the unboxed pattern first; use `block` only when the teaching object is truly a formal definition, theorem, conclusion, or warning.

```latex
\begin{frame}{核心概念}
  \key{一句话结论：}...

  \begin{itemize}
    \item ...
  \end{itemize}
\end{frame}
```

```latex
\begin{frame}{必要时使用定义框}
  \begin{block}{定义}
    仅用于正式定义、定理或需要突出边界的关键结论。
  \end{block}

  \begin{itemize}
    \item ...
  \end{itemize}
\end{frame}
```

```latex
\begin{frame}{例题：从样本均值到区间估计}
  \begin{columns}[T,onlytextwidth]
    \begin{column}{0.48\textwidth}
      ...
    \end{column}
    \begin{column}{0.48\textwidth}
      ...
    \end{column}
  \end{columns}
\end{frame}
```

```latex
\begin{frame}[fragile]{R 代码示例}
\begin{lstlisting}[style=rcode]
...
\end{lstlisting}
\end{frame}
```

## LaTeX Rules

- Match the source courseware language by default; use a user-specified language only when the user explicitly asks. For Chinese courseware, use Chinese punctuation and Chinese section titles. For English courseware, keep English punctuation and section titles.
- Keep all Chinese courseware source files saved as UTF-8.
- Use `\key{}`, `\warn{}`, `\good{}`, and `\smallnote{}` for emphasis.
- Minimize `block` environments. In a typical lecture deck, many frames should have no boxes at all.
- Keep the final deck formal. Do not include renovation-process labels or casual teaching prompts such as “翻新课件”, “旧课件”, “课堂提示”, “教学提醒”, “课堂讨论”, “这里要注意”, or similar meta-instructional wording in visible slide text. Replace them with formal labels such as “说明”, “注意”, “结论”, “例”, or remove the label entirely.
- Use `\[` `\]` for displayed equations; avoid raw `$$`.
- Use `booktabs` tables. For two-column explanatory tables, use this exact alignment pattern unless there is a clear reason not to:

```latex
\newcolumntype{Y}{>{\vspace{0.35ex}\raggedright\arraybackslash}X}

\begin{tabularx}{\linewidth}{>{\bfseries\color{MainBlue}}p{2.7cm}Y}
  \toprule
  项目 & 说明 \\
  \midrule
  ... & ... \\
  \bottomrule
\end{tabularx}
```

  Adjust `p{2.7cm}` only when the first column is visibly too wide or too narrow. Prefer `\linewidth` rather than `\textwidth` inside frames or columns.
- Use `[fragile]` on frames containing `lstlisting` or verbatim-like code.
- In `lstlisting`, verbatim output blocks, screenshots of software output, and reconstructed output tables, keep the software's original language and wording. For example, R output headings such as `Call`, `Residuals`, `Coefficients`, `Estimate`, `Std. Error`, `Pr(>|t|)`, and warning messages must remain as produced by R.
- Escape LaTeX special characters in extracted text: `# $ % & _ { } ~ ^ \`.
- Keep slide content sparse enough for 16:9 projection. If a frame needs font sizes below `\scriptsize`, split it.

## File Hygiene

Create outputs in a task-specific folder, not inside the skill directory. Copy the template into the output folder as `main.tex` and edit that copy.

Do not overwrite the user's old courseware. Preserve extracted figures with stable names such as `figures/ch02-fig03.png`.

## Quality Checklist

Before final delivery:

- Source structure was inspected, not guessed.
- Course name metadata uses the user-specified or inferred course name, or a neutral placeholder when unavailable.
- `\author{...}` uses the user-specified or inferred instructor/teacher name, or a neutral placeholder when unavailable.
- Deck language follows the source courseware or the user's explicit target language.
- Software and system outputs preserve the original output language and wording.
- `main.tex` uses the bundled template style.
- Every old section has a mapped destination or an explicit omission reason.
- Visible slide text is formal and does not mention renovation process labels such as “翻新课件” or casual prompts such as “课堂提示/教学提醒/课堂讨论”.
- Equations and symbols compile and render correctly.
- Tables use the standard `tabularx` alignment pattern where applicable and fit within slide margins.
- Figures are legible and referenced.
- Section divider frames appear through the template's `\AtBeginSection`.
- PDF compiled successfully, or the final response clearly says why it could not be compiled.
