# pylint: skip-file
"""
Test appropriate responses for Syntax Errors
"""
import copy
import pytest
from lexer import Lexer
from riv_exceptions import InternalError, RivuletSyntaxError

no_glyph = """
╰─╮
  │
  ╰─╮
   ─┘
"""

def test_missing_glyph_markers():
    lexr = Lexer()
    gl = copy.deepcopy(no_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.lex_program(gl)       

    assert "No glyph" in str(err.value)

hooks_both_ends_glyph = """
╵╰─╮
   │
   ╰─╮
   ╰─┘╷
"""

def test_hooks_both_ends():
    lexr = Lexer()
    gl = copy.deepcopy(hooks_both_ends_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.lex_program(gl)

    assert "char 3, 2" in str(err.value)

bad_start = """
╵
╰─╮
  │
  ╰─╮
   ─┘╷
"""

def test_bad_start():
    "where a Glyph Start looks ambiguously like a ref marker"
    lexr = Lexer()
    gl = copy.deepcopy(bad_start)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.lex_program(gl)

    assert "No glyph" in str(err.value)
