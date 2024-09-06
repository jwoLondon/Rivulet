# pylint: skip-file
"""
Test appropriate responses for Syntax Errors
"""
import copy
import pytest
from interpreter import Interpreter
from riv_exceptions import InternalError, RivuletSyntaxError

no_glyph = """
╰─╮
  │
  ╰─╮
   ─┘
"""

def test_missing_glyph_markers():
    intr = Interpreter()
    gl = copy.deepcopy(no_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        intr.parse_program(gl)       

    assert "No start" in str(err.value)

hooks_both_ends_glyph = """
╵╰─╮
   │
   ╰─╮
   ╰─┘╷
"""

def test_hooks_both_ends():
    intr = Interpreter()
    gl = copy.deepcopy(hooks_both_ends_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        intr.parse_program(gl)

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
    intr = Interpreter()
    gl = copy.deepcopy(bad_start)
    with pytest.raises(RivuletSyntaxError) as err:
        intr.parse_program(gl)

    assert "No start found" in str(err.value)