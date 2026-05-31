# Demo

A one-slide Beamer presentation (`demo.tex`) showing the Rzk lexer used through
the `minted` LaTeX package. `demo.rzk` is the same code as a standalone source
file for testing the lexer directly with `pygmentize`.

## Prerequisites

- A TeX distribution (TeX Live or MacTeX) with the `minted` package and the
  `moloch` theme (usually in standard shipping).
- Python with Pygments and this repository's lexer installed. From the repo
  root:

  ```sh
  pip install -e .
  ```

  This registers `rzk` as a Pygments lexer alias via the
  `pygments.lexers` entry point in `setup.py`, which `minted` will then find.

## Build

`minted` shells out to Pygments, so LaTeX must be run with `-shell-escape`:

```sh
pdflatex -shell-escape demo.tex
```

The output is `demo.pdf`.

## Test the lexer without LaTeX

```sh
pygmentize -l rzk demo.rzk
```
