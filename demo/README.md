# Demo

Two small demos showing the Rzk lexer in use:

- `demo.tex` — a one-slide Beamer presentation that highlights Rzk code via the
  `minted` LaTeX package.
- `mkdocs/` — a minimal MkDocs site with a single page that highlights the same
  Rzk snippet inside a fenced code block.
- `demo.rzk` — the same code as a standalone source file, useful for testing
  the lexer directly with `pygmentize`.

## Common prerequisite

Install this repository's lexer so Pygments can find it:

```sh
pip install -e .          # run from the repo root
```

This registers `rzk` as a Pygments lexer alias via the `pygments.lexers` entry
point in `setup.py`. Every demo below relies on it.

## LaTeX demo (`demo.tex`)

Additional prerequisites: a TeX distribution (TeX Live or MacTeX) with the
`minted` package and the `moloch` theme (usually in standard shipping).

`minted` shells out to Pygments, so LaTeX must be run with `-shell-escape`:

```sh
pdflatex -shell-escape demo.tex
```

The output is `demo.pdf`.

## MkDocs demo (`mkdocs/`)

Additional prerequisite:

```sh
pip install mkdocs
```

Then, from `demo/mkdocs/`:

```sh
mkdocs serve              # live preview at http://127.0.0.1:8000
mkdocs build              # static site in ./site
```

The `rzk` fenced code block in `mkdocs/docs/index.md` is highlighted by
Pygments through the `codehilite` Markdown extension configured in
`mkdocs/mkdocs.yml`.

## Test the lexer without LaTeX or MkDocs

```sh
pygmentize -l rzk demo.rzk
```
