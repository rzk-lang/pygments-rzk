# Changelog for `pygments-rzk`

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## v0.1.6 — 2026-05-31

Major changes:

- Add a pytest test suite covering every syntax feature plus regression
  fixtures extracted from sHoTT (`rzk-lang/sHoTT` and the modal `diruniv`
  branch of `lishy2/sHoTT`); CI now runs `pytest tests/`.
- Add a MkDocs demo under `demo/mkdocs/` with documentation on how to build
  it, and complete the LaTeX `minted` demo into a full Beamer slide.

Lexer additions:

- Support block comments `{- ... -}`;
- Support hole identifiers `?`;
- Support the `in` keyword paired with `let`;
- Support ASCII modalities `_b`, `_#`, `_op`, `_id` alongside the existing
  Unicode forms `♭`, `♯`, `ᵒᵖ`;
- Support tope/cube inversions `invᵒᵖ`, `uninvᵒᵖ`, `flipᵒᵖ`, `unflipᵒᵖ` and
  their ASCII variants `inv_op`, `uninv_op`, `flip_op`, `unflip_op`;
- Add the Unicode universe symbol `𝒰` and the `⋆` constant to bring the
  lexer in line with the `vscode-rzk` TextMate grammar
  ([rzk-lang/vscode-rzk@353a5fd](https://github.com/rzk-lang/vscode-rzk/commit/353a5fd));
- Highlight the special internal `$extract$` keyword with `Generic.Error` so
  themes render it warning-coloured (it is not for use in user code).

Lexer fixes:

- Fix a typo in the `CUBE|TOPE|U|𝒰` rule's lookbehind (negated character class
  `[^...]` should have been positive `[...]`), which made `U` fail to
  highlight in the common `: U` position;
- Add a temporary catch-all (`\s+` and `.`) to the root state so unmatched
  characters render as plain text instead of being tagged as `Error`, which
  Pygments styles draw as red boxes. The catch-all should be removed once the
  lexer rules cover the full surface syntax.

Other:

- Rewrite relative image URLs in `README.md` to absolute
  `raw.githubusercontent.com` URLs at PyPI-publish time, so PyPI renders the
  screenshots; the README on GitHub keeps the relative paths it prefers
  (drop `include images/*.png` from `MANIFEST.in` accordingly).

## v0.1.5 — 2026-05-31

Major changes:

- Modal syntax support contributed by [Islam Talipov](https://github.com/LIshy2)
  (see [#2](https://github.com/rzk-lang/pygments-rzk/pull/2)):
  - Modal type bracketing `<| ... |>` (Punctuation);
  - `mod` application (Name.Function) and `let mod` (Keyword);
  - Modalities `♭`, `♯`, `ᵒᵖ` (Name.Decorator).
- Highlight the ordinary `let` keyword.

## v0.1.4 — 2023-09-07

- Allow highlighting some reserved symbols at the start of a line
  (see [`7ef5ead`](https://github.com/rzk-lang/pygments-rzk/commit/7ef5ead6)).

## v0.1.3 — 2023-07-11

- Support Unicode syntax and fix some token types
  (see [#1](https://github.com/rzk-lang/pygments-rzk/pull/1)):
  - Sigma alternatives `∑`/`Σ`;
  - Subscript constants `0₂`, `1₂`, `*₁`;
  - Unicode tope operators `≡`, `≤`, `∨`, `∧`;
  - Greek/subscript builtins `π₁`, `π₂`.

## v0.1.2 — 2023-07-01

- Fix some regexes (see [`37cf840`](https://github.com/rzk-lang/pygments-rzk/commit/37cf840b)).

## v0.1.1 — 2023-06-29

- Include images in the source distribution
  (see [`3999b36`](https://github.com/rzk-lang/pygments-rzk/commit/3999b36)).

## v0.1.0 — 2023-06-29

- Initial release: extract the Rzk Pygments lexer into its own package
  (previously bundled in `fizruk/rzk`)
  (see [`6c42b5c`](https://github.com/rzk-lang/pygments-rzk/commit/6c42b5c)).
