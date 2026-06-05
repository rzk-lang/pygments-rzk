# -*- coding: utf-8 -*-
"""
    Rzk lexer
    ~~~~~~~~~

    Pygments lexer for Rzk language (of proof assistant for synthetic ∞-categories).

    :copyright: Copyright 2023-2026 Nikolai Kudasov
    :license: BSD 3, see LICENSE for details.
"""

import pygments.lexer
from pygments.lexer import bygroups
from pygments.token import *

__all__ = ["RzkLexer"]

class RzkLexer(pygments.lexer.RegexLexer):
    name = 'Rzk'
    aliases = ['rzk']
    filenames = ['*.rzk']
    url = 'https://github.com/rzk-lang/rzk'
    KEYWORDS = [] # ['as', 'uses']
    def get_tokens_unprocessed(self, text):
        for index, token, value in super(RzkLexer,self).get_tokens_unprocessed(text):
            if token is Name and value in self.KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
    tokens = {
        'root': [
            (r'--.*\n', Comment),
            (r'\{-', Comment.Multiline, 'block-comment'),
            (r'^(#lang)(\s+)((?![-?!.])[^.\\;,#"\]\[)(}{><|\s]*)(?=$|[.\\;,#"\]\[)(}{><|\s])\s*$',
             bygroups(Name.Decorator, Punctuation, String)),
            (r'^(#check|#compute(-whnf|-nf)?|#set-option|#unset-option)(?=$|[.\\;,#"\]\[)(}{><|\s-])',
             bygroups(Name.Decorator)),
            (r'^(#section|#end)(\s+(?![-?!.])[^.\\;,#"\]\[)(}{><|\s]*)?(?=$|[.\\;,#"\]\[)(}{><|\s])',
             bygroups(Name.Decorator, Name)),
            (r'^(#assume|#variable|#variables)(\s+)((?![-?!.])[^.\\;,#"\]\[)(}{><|:]*)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             bygroups(Keyword.Reserved, Punctuation, Text)),
            (r'^(#def|#define|#postulate)(\s+)((?![-?!.])[^.\\;,#"\]\[)(}{><|\s]*)(?=$|[.\\;,#"\]\[)(}{><|\s])((\s+)(uses)(\s+\()((?![-?!.])[^.\\;,#"\]\[)(}{><|]*)(\)))?',
             bygroups(Keyword.Reserved, Punctuation, Name.Function, None, Punctuation, Keyword, Punctuation, Text, Punctuation)),

            (r'\blet\s+mod\b', Keyword),
            (r'\bmod\b', Name.Function),

            # Special internal syntax: not for use in user code.
            (r'\$extract\$', Generic.Error),

            # builtins
            (r'(^|(?<=[.\\;,#"\]\[)(}{><|\s]))(CUBE|TOPE|U(nit)?|𝒰)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Keyword.Type),
            (r'(^|(?<=[.\\;,#"\]\[)(}{><|\s]))(1|2|II|𝕀|Sigma|∑|Σ)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Keyword.Type),
            (r'(===|≡|<=|≤|\\/|∨|/\\|∧)',
             String.Other),
            (r'(⊤|⊥|\*_1|\*₁|⋆)|(?<=[.\\;,#"\]\[)(}{><|\s])(0_2|0₂|1_2|1₂|0_I|0ᵢ|1_I|1ᵢ|TOP|BOT)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Number),
            (r'(^|(?<=[.\\;,#"\]\[)(}{><|\s]))(recOR|recBOT|idJ|refl|first|second|π₁|π₂|unit|uninvᵒᵖ|invᵒᵖ|unflipᵒᵖ|flipᵒᵖ|uninv_op|inv_op|unflip_op|flip_op)((?=$|[.\\;,#"\]\[)(}{><|\s])|(?=_{))',
             String),
            (r'(^|(?<=[.\\;,#"\]\[)(}{><|\s]))as(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Keyword.Reserved),
            (r'\blet\b', Keyword),
            (r'\bin\b', Keyword),

            # modal bindings: colon fused with modality (e.g. :♭, :_b)
            (r':(_b|_#|_op|_id|♭|♯|ᵒᵖ)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Name.Decorator),

            # modalities (Unicode + ASCII forms)
            (r'(^|(?<=[.\\;,#"\]\[)(}{><|\s]))(_b|_#|_op|_id|♭|♯|ᵒᵖ)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Name.Decorator),

            # parameters
            (r'(\(\s*)([^{:\)]+\s*)(:)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             bygroups(Punctuation, Text, Punctuation)),

            (r'"', String, 'string'),

            (r'(\\\s*)((([^→\t\n\r !"#\(\),-\.;:\\\/=<>\?\[\\\]\{\|\}][^\t\n\r !"#\(\),\.;:<>\?\[\\\]\{\|\}]*)\s*)+)',
                bygroups(Punctuation, Text)),

            # Hole identifier (placeholder term).
            (r'\?', Name.Builtin.Pseudo),

            # Temporary catch-all: anything not matched above renders as plain
            # text instead of being tagged as Error (which Pygments styles
            # draw as a red box). Remove once the rules above cover the full
            # surface syntax.
            (r'\s+', Text),
            (r'.', Text),
        ],
        'string': [
            (r'[^"]+', String),
            (r'"', String, '#pop'),
        ],
        # Non-nested block comments: `{- ... -}`.
        'block-comment': [
            (r'[^-}]+', Comment.Multiline),
            (r'-\}', Comment.Multiline, '#pop'),
            (r'[-}]', Comment.Multiline),
        ],
    }
