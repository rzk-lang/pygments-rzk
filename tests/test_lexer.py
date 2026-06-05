"""Tests that each Rzk syntax feature gets the expected Pygments token.

Each test lexes a small hand-written snippet and asserts that a specific
(token-type, value) pair appears in the output. The final two tests run the
lexer over fixture files extracted from sHoTT (regular + lishy2/diruniv modal
branch) and check that no Error tokens are produced and that the expected
feature tokens are present.
"""

from pathlib import Path

import pytest
from pygments.token import (
    Comment,
    Generic,
    Keyword,
    Name,
    Number,
    Punctuation,
    String,
    Text,
    Token,
)

from pygments_rzk import RzkLexer


FIXTURES = Path(__file__).parent / "fixtures"


def lex(src):
    """Tokenise `src` and return a list of (token-type, value) pairs."""
    return list(RzkLexer().get_tokens(src))


# ---------------------------------------------------------------------------
# Comments
# ---------------------------------------------------------------------------

def test_line_comment():
    assert (Comment, "-- a line comment\n") in lex("-- a line comment\n")


def _comment_text(tokens):
    """The block-comment rule emits open/body/close as separate tokens; this
    joins all consecutive Comment.Multiline tokens back into one string."""
    return "".join(v for t, v in tokens if t is Comment.Multiline)


def test_block_comment_single_line():
    assert _comment_text(lex("{- hello -}\n")) == "{- hello -}"


def test_block_comment_multi_line():
    src = "{- line one\nline two -}\n"
    assert _comment_text(lex(src)) == "{- line one\nline two -}"


def test_block_comment_with_inner_braces():
    src = "{- with {nested braces} inside -}\n"
    assert _comment_text(lex(src)) == "{- with {nested braces} inside -}"


# ---------------------------------------------------------------------------
# Top-level directives
# ---------------------------------------------------------------------------

def test_lang_directive():
    tokens = lex("#lang rzk-1\n")
    assert (Name.Decorator, "#lang") in tokens
    assert (String, "rzk-1") in tokens


@pytest.mark.parametrize(
    "directive",
    ["#check", "#compute", "#compute-whnf", "#compute-nf", "#set-option", "#unset-option"],
)
def test_check_compute_set_option_directives(directive):
    assert (Name.Decorator, directive) in lex(f"{directive} foo\n")


def test_section_and_end():
    tokens = lex("#section foo\n#end foo\n")
    assert (Name.Decorator, "#section") in tokens
    assert (Name.Decorator, "#end") in tokens


@pytest.mark.parametrize("directive", ["#assume", "#variable", "#variables"])
def test_assume_variable_directives(directive):
    assert (Keyword.Reserved, directive) in lex(f"{directive} x y : A\n")


@pytest.mark.parametrize("directive", ["#def", "#define", "#postulate"])
def test_def_define_postulate(directive):
    tokens = lex(f"{directive} foo : U\n")
    assert (Keyword.Reserved, directive) in tokens
    assert (Name.Function, "foo") in tokens


def test_define_with_uses_clause():
    tokens = lex("#define foo uses (A x) : U\n")
    assert (Keyword.Reserved, "#define") in tokens
    assert (Name.Function, "foo") in tokens
    assert (Keyword, "uses") in tokens


# ---------------------------------------------------------------------------
# Built-in types and constants
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kw", ["CUBE", "TOPE", "U", "Unit", "𝒰"])
def test_universe_types(kw):
    assert (Keyword.Type, kw) in lex(f"foo : {kw}\n")


@pytest.mark.parametrize("kw", ["1", "2", "II", "𝕀", "Sigma", "∑", "Σ"])
def test_cube_and_sigma_types(kw):
    assert (Keyword.Type, kw) in lex(f"foo : {kw} bar\n")


@pytest.mark.parametrize("op", ["===", "≡", "<=", "≤", r"\/", "∨", r"/\\".replace("\\\\", "\\"), "∧"])
def test_tope_operators(op):
    assert (String.Other, op) in lex(f"x {op} y\n")


@pytest.mark.parametrize(
    "const", ["⊤", "⊥", "*_1", "*₁", "⋆", "0_2", "0₂", "1_2", "1₂", "0_I", "0ᵢ", "1_I", "1ᵢ", "TOP", "BOT"]
)
def test_constants(const):
    assert (Number, const) in lex(f" {const} \n")


@pytest.mark.parametrize(
    "fn",
    [
        "recOR", "recBOT", "idJ", "refl", "first", "second", "π₁", "π₂", "unit",
        "invᵒᵖ", "uninvᵒᵖ", "flipᵒᵖ", "unflipᵒᵖ",
        "inv_op", "uninv_op", "flip_op", "unflip_op",
    ],
)
def test_builtin_functions(fn):
    assert (String, fn) in lex(f"foo := {fn} x\n")


def test_as_keyword():
    assert (Keyword.Reserved, "as") in lex("foo as bar\n")


# ---------------------------------------------------------------------------
# Modal extensions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("m", ["♭", "♯", "ᵒᵖ"])
def test_modalities_unicode(m):
    assert (Name.Decorator, m) in lex(f"foo : {m} A\n")


@pytest.mark.parametrize("m", ["_b", "_#", "_op", "_id"])
def test_modalities_ascii(m):
    assert (Name.Decorator, m) in lex(f"foo : {m} A\n")


@pytest.mark.parametrize("m", [":♭", ":♯", ":ᵒᵖ"])
def test_modal_bindings_unicode(m):
    assert (Name.Decorator, m) in lex(f"(x {m} A)\n")


@pytest.mark.parametrize("m", [":_b", ":_#", ":_op", ":_id"])
def test_modal_bindings_ascii(m):
    assert (Name.Decorator, m) in lex(f"(x {m} A)\n")


def test_mod_application():
    assert (Name.Function, "mod") in lex("foo := mod ♭ x\n")


def test_let_mod():
    assert (Keyword, "let mod") in lex("foo := let mod ♭ x := y in z\n")


# ---------------------------------------------------------------------------
# Other special syntax
# ---------------------------------------------------------------------------

def test_let_and_in_keywords():
    tokens = lex("foo := let x := y in z\n")
    assert (Keyword, "let") in tokens
    assert (Keyword, "in") in tokens


def test_extract_is_flagged_as_warning():
    """$extract$ is internal; the lexer marks it Generic.Error so themes warn."""
    assert (Generic.Error, "$extract$") in lex("foo := $extract$ ♭ x\n")


def test_hole():
    assert (Name.Builtin.Pseudo, "?") in lex("foo := ?\n")


def test_string_literal():
    tokens = lex('#set-option "name" = "value"\n')
    assert (String, '"') in tokens
    assert (String, "name") in tokens


def test_lambda_abstraction():
    """Lambdas: the leading `\\` and the parameter list should be tokenised."""
    tokens = lex("foo := \\ x y -> z\n")
    # The lambda rule emits Punctuation for `\\` plus optional whitespace.
    assert any(t == Punctuation and "\\" in v for t, v in tokens)


# ---------------------------------------------------------------------------
# Regression against real-world fixtures from sHoTT
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("fixture", ["common.rzk", "modalities.rzk", "block-comments.rzk"])
def test_fixture_produces_no_error_tokens(fixture):
    """Catch-all guarantees no Token.Error tokens are emitted."""
    src = (FIXTURES / fixture).read_text()
    error_tokens = [(t, v) for t, v in lex(src) if t is Token.Error]
    assert error_tokens == [], f"unexpected Error tokens: {error_tokens!r}"


def test_block_comments_swallow_tricky_content():
    """Block comments must hide all interior would-be tokens.

    The fixture has many directive-, keyword-, modality- and operator-shaped
    fragments inside `{- ... -}` blocks and exactly one real piece of code
    outside any comment (`#define real-define : U := refl`). For each token
    that *only* appears inside a block comment, the lexer must report zero
    occurrences; for the positive control, exactly one.
    """
    src = (FIXTURES / "block-comments.rzk").read_text()
    tokens = lex(src)

    def count(tok_type, value):
        return sum(1 for t, v in tokens if t is tok_type and v == value)

    inside_only = [
        # directives
        (Name.Decorator, "#lang"),
        (Name.Decorator, "#section"),
        (Name.Decorator, "#end"),
        (Name.Decorator, "#check"),
        # modal-area keywords
        (Keyword, "let mod"),
        (Name.Function, "mod"),
        (Generic.Error, "$extract$"),
        # modal bindings (colon fused with modality)
        (Name.Decorator, ":♭"),
        (Name.Decorator, ":_b"),
        (Name.Decorator, ":ᵒᵖ"),
        (Name.Decorator, ":_op"),
        # builtin types
        (Keyword.Type, "CUBE"),
        (Keyword.Type, "TOPE"),
        (Keyword.Type, "Unit"),
        (Keyword.Type, "𝒰"),
        (Keyword.Type, "Sigma"),
        (Keyword.Type, "∑"),
        (Keyword.Type, "Σ"),
        # builtin functions (incl. modal inversions)
        (String, "recOR"),
        (String, "recBOT"),
        (String, "idJ"),
        (String, "invᵒᵖ"),
        (String, "flip_op"),
        # modalities
        (Name.Decorator, "♭"),
        (Name.Decorator, "♯"),
        (Name.Decorator, "ᵒᵖ"),
        (Name.Decorator, "_b"),
        (Name.Decorator, "_op"),
        # tope operators
        (String.Other, "==="),
        (String.Other, "≡"),
        # misc
        (Keyword.Reserved, "as"),
        (Name.Builtin.Pseudo, "?"),
    ]
    leaked = [(t, v) for (t, v) in inside_only if count(t, v) > 0]
    assert leaked == [], f"leaked from block comments: {leaked!r}"

    # Positive control: the one real piece of code must still be tokenised.
    assert count(Keyword.Reserved, "#define") == 1
    assert count(Name.Function, "real-define") == 1
    assert count(Keyword.Type, "U") == 1
    assert count(String, "refl") == 1


def test_modal_fixture_exercises_modal_features():
    """The diruniv fixture must light up the modal-specific rules."""
    src = (FIXTURES / "modalities.rzk").read_text()
    tokens = lex(src)
    types_and_values = set(tokens)

    # Modal bindings (colon fused with modality)
    assert (Name.Decorator, ":♭") in types_and_values
    assert (Name.Decorator, ":♯") in types_and_values
    assert (Name.Decorator, ":ᵒᵖ") in types_and_values
    assert (Name.Decorator, ":_b") in types_and_values
    assert (Name.Decorator, ":_op") in types_and_values
    # Unicode modalities used in the fixture
    assert (Name.Decorator, "♭") in types_and_values
    assert (Name.Decorator, "♯") in types_and_values
    assert (Name.Decorator, "ᵒᵖ") in types_and_values
    # mod application and let mod
    assert (Name.Function, "mod") in types_and_values
    assert (Keyword, "let mod") in types_and_values
    # `in` (paired with let mod) appears in this file
    assert (Keyword, "in") in types_and_values
