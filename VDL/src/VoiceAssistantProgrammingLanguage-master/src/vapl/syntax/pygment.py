"""Pygments lexer for vapl."""

from pygments.lexers.python import PythonLexer

class vaplLexer(PythonLexer):
    """Lexer for vapl code. Currently just uses the Python lexer."""
    name = 'vapl'
    aliases = ['vapl']
    filenames = ['*.vapl', '*.sc']
