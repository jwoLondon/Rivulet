# pylint: skip-file
"""
Test appropriate responses for Syntax Errors
"""
import copy
import pytest
from riv_parser import Parser
from riv_exceptions import InternalError, RivuletSyntaxError

no_glyph = """
╰─╮
  │
  ╰─╮
   ─┘
"""

def test_missing_glyph_markers():
    lexr = Parser()
    gl = copy.deepcopy(no_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)       

    assert "No glyph" in str(err.value)

hooks_both_ends_glyph = """
╵╰─╮
   │
   ╰─╮
   ╰─┘╷
"""

def test_hooks_both_ends():
    lexr = Parser()
    gl = copy.deepcopy(hooks_both_ends_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

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
    lexr = Parser()
    gl = copy.deepcopy(bad_start)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "corresponding Start" in str(err.value)
    assert "5, 4" in str(err.value)

empty_col_mid_glyph = """
 1 ╵╵ ╭──╮ ───╮ ───╮
 2   ╶╯ ─╯  ╭─╯ ╶╮ │ ╭─╶ ╭─╶
 3         ╶╯    └─╯╶╯   │
 5                   ╭╴ ╶╯
 7                 │ │
11                 └─╯     ╷


"""

def test_empty_col_mid_glyph():
    "glyph with blank col in middle is rejected"
    lexr = Parser()
    gl = copy.deepcopy(empty_col_mid_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "Start glyph at 4, 0" in str(err.value)

empty_col_mid_glyph_bottom = """
 1 ╵╵ ╭──╮ ───╮ ───╮
 2   ╶╯ ─╯  ╭─╯ ╶╮ │ ╭─╶ ╭─╶
 3         ╶╯    └─╯╶╯   │
 5                   ╭╴ ╶╯
 7                 │ │
11                 └─╯     ╷
"""

def test_empty_col_mid_glyph_bottom():
    "glyph with blank col in middle is rejected, even if at bottom of program"
    lexr = Parser()
    gl = copy.deepcopy(empty_col_mid_glyph_bottom)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "Start glyph at 4, 0" in str(err.value)

whitespace_in_middle = """
 ╵╭─╶ ╮  ╭─┘╭─╶ 
  │   │╭─┘╭─╯  
  │╶╮ │╰─ │ 
  ╰─┘ ╰───┘   ╷
  """
def test_another_whitespace():
    "glyph with blank col in middle is rejected, even if at bottom of program"
    lexr = Parser()
    gl = copy.deepcopy(whitespace_in_middle)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "Start glyph" in str(err.value)